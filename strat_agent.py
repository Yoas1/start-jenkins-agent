import os
from os import path, system, name
import subprocess
import time
import datetime
import re
global system_os
global agent_name


def check_os():
    global system_os
    if name == 'nt':
        system_os = "windows"
    else:
        system_os = "linux"


def clear_screen():
    global system_os
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


def time_now():
    now = datetime.datetime.now().strftime('%H:%M:%S %d-%m-%Y')
    return now


def read_config():
    f = open("config", "r")
    list_file = []
    for x in f:
        list_file.append(x)
    r_url = str(list_file[0].replace('\n', ""))
    r_secret = str(list_file[1].replace('\n', ""))
    r_workdir = str(list_file[2].replace('\n', ""))
    r_agent_name = re.sub(r'^.*?computer/', '', r_url).replace("/jenkins-agent.jnlp", "")
    return r_url, r_secret, r_workdir, r_agent_name


def check_offline():
    data = os.popen('curl --silent -u<user>:<password> <url>/<agent_name>/api/json').read()
    if '"offline":true' in data:
        return "offline"
    if '"offline":false' in data:
        return "online"
    else:
        return "Error"


def new_agent():
    global agent_name
    url_config = input("Enter agent url: ") #= <url>/<agent_name>/jenkins-agent.jnlp
    secret_config = input("Enter agent secret: ") #= <secret>
    workdir_config = input("Enter agent workdir: ") #= <workdir>
    with open('config', 'w') as conf:
        conf.write(url_config + '\n' + secret_config + '\n' + workdir_config + '\n')


def start_agent():
    global agent_name
    check_os()
    url, secret, workdir, agent_name = read_config()
    if system_os == "windows":
        subprocess.Popen(["start", "cmd", "/k", 'java -jar C:\\agent\\agent.jar -jnlpUrl {} -secret {} -workDir {}'
                         .format(url, secret, workdir)], shell=True)
    elif system_os == "linux":
        os.system('java -jar agent.jar -jnlpUrl {} -secret {} -workDir {} &'.format(url, secret, workdir))


if __name__ == '__main__':
    url, secret, workdir, agent_name = read_config()
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
