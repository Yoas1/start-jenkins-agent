import re
import time
import datetime
from os import system, name, popen


def clear_screen():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def time_now():
    now = datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')
    return now


while True:
    print(time_now())
    urls_file = open('agents_config', 'r')
    urls_data = urls_file.read()
    urls = urls_data.split('\n')
    urls_file.close()
    conf_len = len(urls)
    for t in range(conf_len - (conf_len - 1)):
        interval = int(urls[t])
    for i in range(conf_len - 1):
        agent = urls[i + 1]
        agent_name = re.sub(r'^.*?computer/', '', agent)
        url_check = agent + '/api/json'
        data = popen('curl --silent -u<user>:<password> {}'.format(url_check)).read()
        if '"offline":true' in data:
            print(agent_name + " offline")
        elif '"offline":false' in data:
            print(agent_name + " online")
        else:
            print("Error")
    time.sleep(interval)
    clear_screen()
