import requests
import sys
from secrets import bbtmvbot_url, influxdb_db_url

response = requests.get(bbtmvbot_url)
commands = response.text.split("\n")[:-1]
for command in commands:
    print('Writing ' + command + '... ', end = '')
    try:
        response = requests.post(influxdb_db_url, data = command)
        if response.ok:
            print("OK")
        else:
            print('Request failed: ' + response.text)
    except Exception as e:
        print(e)
