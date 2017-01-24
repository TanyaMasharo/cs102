import requests
import datetime
import math

DOMAIN = "https://api.vk.com/method"
ACCESS_TOKEN = ""


def predict_age(user_id):
    """ Returns a list of user IDs or detailed information about a user's friends """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    query_params = {
        'domain': DOMAIN,
        'access_token': ACCESS_TOKEN,
        'user_id': user_id,
        'fields': 'bdate'
    }

    query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v=5.53".format(**query_params)
    response = requests.get(query)

    json = response.json()['response']

    total_age = 0
    total_processed = 0

    items = json['items']
    for i in range(0, json["count"]):
        try:

            birthday = items[i]['bdate']
            if not birthday or birthday.count('.') != 2:
                continue

            total_age += datetime.datetime.now().year - datetime.datetime.strptime(birthday, '%d.%m.%Y').year
            total_processed += 1

        except:
            pass

    return math.floor(0 if total_processed == 0 else total_age / total_processed)


print(predict_age(25492120))