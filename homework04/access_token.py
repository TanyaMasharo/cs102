import requests
import plotly
import datetime
from collections import defaultdict
import plotly.plotly as py
import plotly.graph_objs as go

DOMAIN = "https://api.vk.com/method"
ACCESS_TOKEN = ""


def messages_get_history(user_id, peer_id, offset=0, count=20):
    assert isinstance(user_id, int), "user_id must be integer"
    assert user_id > 0, "user_id must be positive"
    assert isinstance(offset, int), "offset must be integer"
    assert offset >= 0, "offset must be positive"
    assert count >= 0, "count must be positive integer"
    assert count <= 200, "count must be less than or equal to 200"

    query_params = {
        'domain': DOMAIN,
        'access_token': ACCESS_TOKEN,
        'user_id': user_id,
        'peer_id': peer_id,
        'fields': 'date',
        'offset': offset,
        'count': count
    }

    query = "{domain}/messages.getHistory" \
            "?access_token={access_token}" \
            "&user_id={user_id}" \
            "&peer_id={peer_id}" \
            "&fields={fields}" \
            "&offset={offset}" \
            "&count={count}" \
            "&v=5.53"\
        .format(**query_params)

    return requests.get(query).json()['response']['items']

def messages_get_full_history(user_id, peer_id, count=20):
    offset = 0
    rest_count = count

    messages = []
    while rest_count > 0:
        if rest_count < 200:
            messages += messages_get_history(user_id, peer_id, offset, rest_count)
            break

        messages += messages_get_history(user_id, peer_id, offset, 200)

        offset += 200
        rest_count -= 200

    return messages


def message_frequency(messages):
    mapped = defaultdict(lambda: 0)
    for i in range(0, len(messages)):
        date = datetime.datetime.fromtimestamp(messages[i]['date'])
        date = date.replace(hour=0, minute=0, second=0, microsecond=0)

        mapped[date] += 1

    x = []
    y = []
    for k, v in sorted(mapped.items()):
        x.append(k)
        y.append(v)

    return x, y


plotly.tools.set_credentials_file(username='5818366', api_key='xYvUAK78nhZ40YlnKa8m')

x, y = message_frequency(messages_get_full_history(36494153, 25492120, 260))

data = [go.Scatter(x = x, y = y)]
py.plot(data)