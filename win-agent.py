import os
from os import path

def chck_status():
    data = os.popen('curl -u<user>:<password> <curl>').read()
    if '"offline":true' in data:
        print("ok")
    else:
        print("no")
    
def new_agent():
    url_config = input("Enter agent url: ") #= http://192.168.1.167:8080/computer/win/jenkins-agent.jnlp
    secret_config = input("Enter agent secret: ") #=288758c8463a3d2e9f96918dc75f45004c7b90dab86c4b5ab294c9a694437037
    workdir_config = input("Enter agent workdir: ") #=D:\\agent
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
    os.system('cmd /c "java -jar agent.jar -jnlpUrl {} -secret {} -workDir "{}""'.format(url, secret, workdir))


if __name__ == '__main__':

    if not path.exists("config"):
        new_agent()
        start_agent()
    else:
        start_agent()
