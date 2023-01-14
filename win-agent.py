import os
from os import path
import subprocess
import time
import datetime


def time_now():
    now = datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')
    return now


def check_offline():
    data = os.popen('curl --silent -u<user>:<password> <url>/computer/<agent_name>/api/json').read()
    if '"offline":true' in data:
        return "offline"
    else:
        return "online"

def new_agent():
    url_config = input("Enter agent url: ") #= <url>/computer/<agent_name>/jenkins-agent.jnlp
    secret_config = input("Enter agent secret: ") #= <secret>
    workdir_config = input("Enter agent workdir: ") #= <workdir>
    with open('config', 'w') as conf:
        conf.write(url_config + '\n' + secret_config + '\n' + workdir_config + '\n')


def start_agent():
    f = open("config", "r")
    list = []
    for x in f:
        list.append(x)
    url = str(list[0].replace('\n', ""))
    secret = str(list[1].replace('\n', ""))
    workdir = str(list[2].replace('\n', ""))
    subprocess.Popen(["start", "cmd", "/k", 'java -jar C:\\agent\\agent.jar -jnlpUrl {} -secret {} -workDir {}'.format(url, secret, workdir)], shell = True)


if __name__ == '__main__':
    while True:
        if check_offline() == "offline":
            print("Agent start in few seconds")
            if not path.exists("config"):
                new_agent()
                start_agent()
                time.sleep(10)
                print("Connected " + time_now())
                time.sleep(30)
            else:
                start_agent()
                time.sleep(10)
                print("Connected " + time_now())
                time.sleep(30)
        elif check_offline() == "online":
            print("Connected " + time_now())
            time.sleep(30)
        else:
            print("Error " + time_now())
            break
