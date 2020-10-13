import requests
import sys
from secrets import bbtmvbot_url, influxdb_db_url

def create_db(db_name):
    params = {'q': 'CREATE DATABASE ' + db_name}
    try:
        return requests.post(influxdb_query_url, data=params)
    except Exception as e:
        print(e)

def send_command(command, create_db_if_not_exists):
    print('Writing ' + command + '... ', end='')
    
    response = requests.post(influxdb_write_url, data = command)
    if response.ok:
        print("OK")
    else:
        response_dict = response.json()

        if response_dict['error'] == 'database not found: "' + db_name + '"' and create_db_if_not_exists:
            print("Database not found, attempting to create... ", end='')
            create_db_response = create_db(db_name)
            if create_db_response.ok:
                print("OK, retrying command...")
                send_command(command, False)
            else:
                print("Fail: " + str(create_db_response.json()))
        else:
            print('Fail: ' + str(response_dict))

db_name = 'bbtmvbot'
influxdb_write_url = influxdb_db_url + '/write?db=' + db_name
influxdb_query_url = influxdb_db_url + '/query'

response = requests.get(bbtmvbot_url)
commands = response.text.split("\n")[:-1]

for command in commands:
    try:
        send_command(command, True)
    except Exception as e:
        print(e)
