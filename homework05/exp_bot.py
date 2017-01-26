import requests
import datetime
import telebot

from bs4 import BeautifulSoup
from collections import defaultdict


DOMAIN = "http://www.ifmo.ru/ru/schedule"

SCHEDULE_CACHE = {}

EVEN = 'четная неделя'
NOT_EVEN = 'нечетная неделя'

DAYS_STR = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
DAYS = ['1day', '2day', '3day', '4day', '5day', '6day']


class Lesson:
    def __init__(self, name, time, location, room, week):
        self.name = name.replace('\n', '').replace('\t', '')
        self.location = location
        self.room = room

        if EVEN == week:
            self.week = '1'
        elif NOT_EVEN == week:
            self.week = '2'
        else:
            self.week = '0'

        chunks = time.split('-')
        self.time_start = datetime.datetime.strptime(chunks[0], '%H:%M')
        self.time_end = datetime.datetime.strptime(chunks[1], '%H:%M')

    def __str__(self):
        return self.name + ' ' + self.time_as_string() + ' ' + self.location + ' ' + self.room

    def time_as_string(self):
        return '(' + str(self.time_start.hour) + ':' + str(self.time_start.minute) + '-' \
               + str(self.time_end.hour) + ':' + str(self.time_end.minute) + ')'


class Schedule:
    def __init__(self):
        self.days = defaultdict(lambda: [])

    def add_lesson(self, day, lesson):
        self.days[day].append(lesson)

    def get_filtered_day(self, week, day):
        lessons = []
        if day in self.days:
            [lessons.append(lesson) for lesson in self.days[day] if '0' == lesson.week or week == lesson.week]

        return lessons

    def get_filtered_schedule(self, week):
        schedule = Schedule()
        for day in DAYS:
            schedule.add_lesson(day, self.get_filtered_day(week, day))

        return schedule

    def __str__(self):
        result = ''
        for day in DAYS:
            if day in self.days and len(self.days[day]) > 0:
                result += day + '\n'
                for lessons in self.days[day]:
                    for lesson in lessons:
                        result += lesson.__str__() + '\n'

        return result


def get_page(group, week='0'):
    url = '{domain}/{week}/{group}/raspisanie_zanyatiy_{group}.htm'.format(domain=DOMAIN, week=week, group=group)
    response = requests.get(url)

    return response.text


def parse_day_schedule(web_page, day):
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": day})
    if not schedule_table:
        raise Exception('no schedule for that day')

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Неделя (четная\не четная) проведения занятий
    weeks_list = []

    temp_list = schedule_table.find_all("td", attrs={"class": "time"})
    for temp in temp_list:
        tags = temp.find_all('dt')
        for tag in tags:
            try:
                tag.attrs['class']
            except:
                weeks_list.append(tag.text)

    # Аудитория
    rooms_list = schedule_table.find_all("td", attrs={"class": "room"})
    rooms_list = [room.dd.text for room in rooms_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, rooms_list, lessons_list, weeks_list


def parse_schedule(web_page):
    schedule = Schedule()
    for day in DAYS:
        try:

            times, locations, rooms, lessons, weeks = parse_day_schedule(web_page, day)

            for i in range(0, len(times)):
                lesson = Lesson(lessons[i], times[i], locations[i], rooms[i], weeks[i])
                schedule.add_lesson(day, lesson)

        except:
            pass

    return schedule


def get_schedule(group):
    if group not in SCHEDULE_CACHE:
        SCHEDULE_CACHE[group] = parse_schedule(get_page(group))

    return SCHEDULE_CACHE[group]


def get_nearest_lesson(group):
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute

    day = now.weekday() + 1
    day = 1 if day == 7 else day
    week = str(now.isocalendar()[1] % 2 + 1)

    counter = 0
    lessons = None
    while counter < 7:
        lessons = get_schedule(group).get_filtered_day(week, str(day) + 'day')
        if len(lessons):
            break

        counter += 1
        day += 1
        day = 1 if day == 7 else day

    if not lessons:
        return None

    for lesson in lessons:
        if lesson.time_start.hour > hour or (lesson.time_start.hour == hour and lesson.time_start.minute == minute):
            return lesson

    return None


def get_lessons_for_day(day, week, group):
    return get_schedule(group).get_filtered_day(week, day)


def get_all_lessons_for_a_week(week, group):
    return get_schedule(group).get_filtered_schedule(week)


bot = telebot.TeleBot('')


@bot.message_handler(commands=DAYS_STR)
def get_monday(message):
    day, week, group = message.text.split()

    day = day[1:len(day)]
    if day not in DAYS_STR:
        return "Bad day"

    lessons = get_lessons_for_day(DAYS[DAYS_STR.index(day)], week, group)

    resp = ''
    for lesson in lessons:
        resp += str(lesson) + '\n'

    if len(resp) == 0:
        resp = 'nothing to show'

    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands='near_lesson')
def get_monday(message):
    _, group = message.text.split()

    lesson = get_nearest_lesson(group)

    resp = 'nothing to show' if not lesson else str(lesson)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands='all')
def get_monday(message):
    _, week, group = message.text.split()

    schedule = get_all_lessons_for_a_week(week, group)

    resp = 'nothing to show' if not schedule else str(schedule)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


bot.polling(none_stop=True)