import os
from os import path, system, name
import subprocess
import time
import datetime
import re


def clear_screen():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def time_now():
    now = datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')
    return now


def check_offline():
    data = os.popen('curl --silent -uyoas1:Aa5589aa http://192.168.1.88:8080/computer/windows/api/json').read()
    if '"offline":true' in data:
        return "offline"
    if '"offline":false' in data:
        return "online"
    else:
        return "Error"


def new_agent():
    url_config = input("Enter agent url: ") #= http://192.168.1.88:8080/computer/windows/jenkins-agent.jnlp
    secret_config = input("Enter agent secret: ") #= e14177823181b19597a08c974eb74e453f117e9a8089c842633e0e4208f4c43e
    workdir_config = input("Enter agent workdir: ") #= D:\\agent
    with open('config', 'w') as conf:
        conf.write(url_config + '\n' + secret_config + '\n' + workdir_config + '\n')


def start_agent():
    global agent_name
    f = open("config", "r")
    list_file = []
    for x in f:
        list_file.append(x)
    url = str(list_file[0].replace('\n', ""))
    secret = str(list_file[1].replace('\n', ""))
    workdir = str(list_file[2].replace('\n', ""))
    agent_name = re.sub(r'^.*?computer/', '', url)
    agent_name = agent_name.replace("/jenkins-agent.jnlp", "")
    subprocess.Popen(["start", "cmd", "/k", 'java -jar C:\\agent\\agent.jar -jnlpUrl {} -secret {} -workDir {}'.format(url, secret, workdir)], shell = True)


if __name__ == '__main__':
    global agent_name
    while True:
        if check_offline() == "offline":
            print("Agent start in few seconds")
            if not path.exists("config"):
                new_agent()
                start_agent()
                time.sleep(10)
                print(agent_name + " Connected " + time_now())
                time.sleep(30)
            else:
                start_agent()
                time.sleep(10)
                print(agent_name + " Connected " + time_now())
                time.sleep(30)
        elif check_offline() == "online":
            print(agent_name + " Connected " + time_now())
            time.sleep(30)
        else:
            print("Error the user not exists " + time_now())
            break
        clear_screen()
