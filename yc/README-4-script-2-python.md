# Домашнее задание к занятию "4.2. Использование Python для решения типовых DevOps задач"

## Обязательные задания

1. Есть скрипт:
```python
    #!/usr/bin/env python3
	a = 1
	b = '2'
	c = a + b
```
	* Какое значение будет присвоено переменной c?
		
> При исплнении скрипта произойдет Несовместимость типом при вычислении 
	
	* Как получить для переменной c значение 12?

> Для этого переопределить в коде a = '1', т.е. a  - это строка

	* Как получить для переменной c значение 3?

> Для этого переопределить в коде a = 1 и b =2 - т.е. a и b - целочисленные

2. Мы устроились на работу в компанию, где раньше уже был DevOps Engineer. Он написал скрипт, позволяющий узнать, какие файлы модифицированы в репозитории, относительно локальных изменений. Этим скриптом недовольно начальство, потому что в его выводе есть не все изменённые файлы, а также непонятен полный путь к директории, где они находятся. Как можно доработать скрипт ниже, чтобы он исполнял требования вашего руководителя?



```python
    #!/usr/bin/env python3

    import os

	bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
	result_os = os.popen(' && '.join(bash_command)).read()
    is_change = False
	for result in result_os.split('\n'):
        if result.find('modified') != -1:
            prepare_result = result.replace('\tmodified:   ', '')
            print(prepare_result)
            break

```


> Вывод измененного скрипта для Руководителя:

```bash



root@dev1-10:/home/demi/netol_do/devops-netology# ./test_4.2_2.py 
Добавлен_файл/переменная:  README-4-script-2-python.md
Путь местонахождения: 
/home/demi/netol_do/devops-netology/README-4-script-2-python.md
---------------------------------------
Изменен_файл/переменная:  a
Путь местонахождения: 
/home/demi/netol_do/devops-netology/a
---------------------------------------
Добавлен_файл/переменная:  b
Путь местонахождения: 
/home/demi/netol_do/devops-netology/b
---------------------------------------
Добавлен_файл/переменная:  test_4.2_1.py
Путь местонахождения: 
/home/demi/netol_do/devops-netology/test_4.2_1.py
---------------------------------------
Добавлен/Изменен_файл/переменная: test_4.2_2.py
Путь местонахождения: 
/home/demi/netol_do/devops-netology/test_4.2_2.py
---------------------------------------

```



> Измененный скрипт для Руководителя:

```python
root@dev1-10:/home/demi/netol_do/devops-netology# cat test_4.2_2.py
#!/usr/bin/env python3

import os

bash_command = ["cd /home/demi/netol_do/devops-netology", "git status --porcelain --ignored -uno "]
result_os = os.popen(' && '.join(bash_command)).read()
    

is_change = False

        
for result in result_os.split('\n'):

    if result.find('AM',0,2) != -1:
        prepare_result = result.replace('AM ', 'Добавлен/Изменен_файл/переменная: ')
        print(prepare_result)

    elif result.find('M',0,2) != -1:
        prepare_result = result.replace('M ', 'Изменен_файл/переменная: ')
        print(prepare_result)

    elif result.find('A',0,2) != -1:
        prepare_result = result.replace('A ', 'Добавлен_файл/переменная: ')
        print(prepare_result)

    else: break
    
    b=prepare_result.split(' ')
    if b != '':
        print('Путь местонахождения: ')
        bash_2='realpath '+b[-1]
        os.system(bash_2)
        print('---------------------------------------')
root@dev1-10:/home/demi/netol_do/devops-netology# 


```







3. Доработать скрипт выше так, чтобы он мог проверять не только локальный репозиторий в текущей директории, а также умел воспринимать путь к репозиторию, который мы передаём как входной параметр. Мы точно знаем, что начальство коварное и будет проверять работу этого скрипта в директориях, которые не являются локальными репозиториями.


> Вывод доработаннного скрипта:

```bash

root@dev1-10:/home/demi/netol_do/devops-netology# ./test_4.2_3.py /home/demi/netol_do/devops-netology

Path exists!

|████████████████████████████████████████| 5/5 [100%] in 5.0s (0.99/s) 


Результаты поиска в /home/demi/netol_do/devops-netology:

---------------------------------------
Добавлен/Изменен_файл/переменная: README-4-script-2-python.md
Путь местонахождения: 
/home/demi/netol_do/devops-netology/README-4-script-2-python.md

---------------------------------------
Изменен_файл/переменная:  a
Путь местонахождения: 
/home/demi/netol_do/devops-netology/a

---------------------------------------
Добавлен_файл/переменная:  b
Путь местонахождения: 
/home/demi/netol_do/devops-netology/b

---------------------------------------
Добавлен_файл/переменная:  test_4.2_1.py
Путь местонахождения: 
/home/demi/netol_do/devops-netology/test_4.2_1.py

---------------------------------------
Добавлен/Изменен_файл/переменная: test_4.2_2.py
Путь местонахождения: 
/home/demi/netol_do/devops-netology/test_4.2_2.py

---------------------------------------

root@dev1-10:/home/demi/netol_do/devops-netology# ./test_4.2_3.py /home/demi/netol_do/

Path exists!

This is not git Repository! Please, choose another one!

root@dev1-10:/home/demi/netol_do/devops-netology# ./test_4.2_3.py /home/demi/netol
Path or file does not exist!

root@dev1-10:/home/demi/netol_do/devops-netology# ./test_4.2_3.py

Please use: Path (str) to Repository where search updates!

```





>  Доработанный Скрипт:

```bash

root@dev1-10:/home/demi/netol_do/devops-netology# cat ./test_4.2_3.py 
#!/usr/bin/env python3

import os
import sys
import time

A = sys.argv
if len(A) <= 1: 
    print('\nPlease use: Path (str) to Repository where search updates!\n')
    sys.exit()
elif type(A[1])==str:
    check_path=os.path.exists(A[1])
    if check_path:
        print('\nPath exists!\n')
        check_path=os.path.exists(A[1]+'/.git')
        if check_path==False:
            print('This is not git Repository! Please, choose another one!\n');
            sys.exit()
    else:
        print('Path or file does not exist!\n')
        sys.exit()
else: 
    print('Wrong argument type!\n')
    sys.exit()

bash_command = ["cd /home/demi/netol_do/devops-netology", "git status --porcelain --ignored -uno "]
result_os = os.popen(' && '.join(bash_command)).read()
    

from alive_progress import alive_bar

l = len(result_os.split('\n'))-1
mylist=range(0,l,1)

#print(list(mylist))

P="\n\nРезультаты поиска в "+A[1]+":\n\n---------------------------------------\n"

with alive_bar(l) as bar:
        
    for result in result_os.split('\n'):


        if result.find('AM',0,2) != -1:
            prepare_result = result.replace('AM ', 'Добавлен/Изменен_файл/переменная: ')
            P=P+prepare_result+'\n'

        elif result.find('M',0,2) != -1:
            prepare_result = result.replace('M ', 'Изменен_файл/переменная: ')
            P=P+prepare_result+'\n'

        elif result.find('A',0,2) != -1:
            prepare_result = result.replace('A ', 'Добавлен_файл/переменная: ')
            P=P+prepare_result+'\n'
        

        else: break
        
        b=prepare_result.split(' ')
        if b != '':
            P=P+'Путь местонахождения: \n'
            bash_2='realpath '+b[-1]
            bash_2_res=os.popen(bash_2).read()
    #        print(bash_2_res)
            P=P+bash_2_res+'\n'
            P=P+'---------------------------------------\n'

        bar()
        time.sleep(1)

print(P)
root@dev1-10:/home/demi/netol_do/devops-netology#

```


4. Наша команда разрабатывает несколько веб-сервисов, доступных по http. Мы точно знаем, что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, где установлен сервис. Проблема в том, что отдел, занимающийся нашей инфраструктурой очень часто меняет нам сервера, поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за собой DNS имена. Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали в такой сегмент сети нашей компании, который недоступен для разработчиков. Мы хотим написать скрипт, который опрашивает веб-сервисы, получает их IP, выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>. Будем считать, что наша разработка реализовала сервисы: drive.google.com, mail.google.com, google.com.


> Вывод прелагаемого скрипта для проверки IP по доменам:

```bash


root@dev1-10:/home/demi/netol_do/devops-netology# ./test_4.2_4.py
drive.google.com

[OK] ips equals each other!

Press any key!
drive.google.com

[OK] ips equals each other!

mail.google.com

[ERROR] ip mismath: Old ip list-> [{'ipv4_0': '173.194.73.83', 'ipv4_1': '173.194.73.18', 'ipv4_2': '173.194.73.19', 'ipv4_3': '173.194.73.17'}] New ip list-> [{'ipv4_0': '173.194.73.19', 'ipv4_1': '173.194.73.17', 'ipv4_2': '173.194.73.83', 'ipv4_3': '173.194.73.18'}]

Press any key!
drive.google.com

[OK] ips equals each other!

mail.google.com

[ERROR] ip mismath: Old ip list-> [{'ipv4_0': '173.194.73.83', 'ipv4_1': '173.194.73.18', 'ipv4_2': '173.194.73.19', 'ipv4_3': '173.194.73.17'}] New ip list-> [{'ipv4_0': '173.194.73.19', 'ipv4_1': '173.194.73.17', 'ipv4_2': '173.194.73.83', 'ipv4_3': '173.194.73.18'}]

google.com

[ERROR] ip mismath: Old ip list-> [{'ipv4_0': '173.194.222.113', 'ipv4_1': '173.194.222.138', 'ipv4_2': '173.194.222.101', 'ipv4_3': '173.194.222.139', 'ipv4_4': '173.194.222.102', 'ipv4_5': '173.194.222.100'}] New ip list-> [{'ipv4_0': '173.194.222.138', 'ipv4_1': '173.194.222.101', 'ipv4_2': '173.194.222.139', 'ipv4_3': '173.194.222.102', 'ipv4_4': '173.194.222.100', 'ipv4_5': '173.194.222.113'}]

Press any key!

Whole dictionary listing: 

{'drive.google.com': [{'ipv4_0': '142.251.1.194', 'ipv4_1': '108.177.14.194', 'ipv4_2': '64.233.165.194'}], 'mail.google.com': [{'ipv4_0': '173.194.73.19', 'ipv4_1': '173.194.73.17', 'ipv4_2': '173.194.73.83', 'ipv4_3': '173.194.73.18'}], 'google.com': [{'ipv4_0': '173.194.222.138', 'ipv4_1': '173.194.222.101', 'ipv4_2': '173.194.222.139', 'ipv4_3': '173.194.222.102', 'ipv4_4': '173.194.222.100', 'ipv4_5': '173.194.222.113'}]}
root@dev1-10:/home/demi/netol_do/devops-netology# 
root@dev1-10:/home/demi/netol_do/devops-netology# 
root@dev1-10:/home/demi/netol_do/devops-netology# cat last_dig.log 
{"drive.google.com": [{"ipv4_0": "142.251.1.194", "ipv4_1": "108.177.14.194", "ipv4_2": "64.233.165.194"}], "mail.google.com": [{"ipv4_0": "173.194.73.19", "ipv4_1": "173.194.73.17", "ipv4_2": "173.194.73.83", "ipv4_3": "173.194.73.18"}], "google.com": [{"ipv4_0": "173.194.222.138", "ipv4_1": "173.194.222.101", "ipv4_2": "173.194.222.139", "ipv4_3": "173.194.222.102", "ipv4_4": "173.194.222.100", "ipv4_5": "173.194.222.113"}]}


```

> Предлагаемый скрипт для проверки IP по доменам :

```python



root@dev1-10:/home/demi/netol_do/devops-netology# cat ./test_4.2_4.py 
#!/usr/bin/env python3

import os
import json

log='last_dig.log'
log_err=False

#Если существует лог, прчитать структуру JSON dict из него
last_dig_json={}

if not os.access(log, os.R_OK):
    print("\nFailed to open log-file - does not exist!\n")
    log_err=True
elif os.stat(log).st_size != 0:
    with open(log) as f:
        last_dig_json = json.load(f)
else:
    print("\nFailed to open log-file - empty!\n")
    log_err=True


#Сервисы для проверки
Srvs=('drive.google.com','mail.google.com','google.com')

bash_command="dig +short  "
bash_command2=" | grep '^[.0-9]*$'"


dig_res_prn=''
dig_res=''
dig_json={}

f=open(log,'w')

for i in Srvs:

    j=os.popen(bash_command + i + bash_command2).read()
    j_split=j.split('\n')
    del j_split[-1]
    #print(j_split)

    dig_json[i]=[]

    json_inner_dict = {}
    num = 0
    for k in j_split:
        dig_res_prn=dig_res_prn+i+' - '+k+'\n'
        dig_res=dig_res+' '+k

        st1="ipv4_"+str(num)
        st2=k
        
        json_inner_dict.update({st1 : st2})
        num+=1
           
    dig_json[i].append(json_inner_dict)

#Проверка текущего резолва и резолва из лога

    d=dig_json.get(i)
        
    if not log_err:
        dl=last_dig_json.get(i)
            
        for j in dig_json:

            print(j)

            if (j in last_dig_json) and (dig_json[j] != last_dig_json[j]):
                print('\n[ERROR] ip mismath: Old ip list-> '+str(last_dig_json[j])+' New ip list-> '+str(dig_json[j])+'\n')
            else:
                print('\n[OK] ips equals each other!\n')

    input('Press any key!')



st=str(dig_json)
st = st.replace('\'','\"')


f.write(st)


dig_res_splt=dig_res.split(' ')
del dig_res_splt[0]

print('\nWhole dictionary listing: \n')

print(dig_json)

root@dev1-10:/home/demi/netol_do/devops-netology#


```





## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так получилось, что мы очень часто вносим правки в конфигурацию своей системы прямо на сервере. Но так как вся наша команда разработки держит файлы конфигурации в github и пользуется gitflow, то нам приходится каждый раз переносить архив с нашими изменениями с сервера на наш локальный компьютер, формировать новую ветку, коммитить в неё изменения, создавать pull request (PR) и только после выполнения Merge мы наконец можем официально подтвердить, что новая конфигурация применена. Мы хотим максимально автоматизировать всю цепочку действий. Для этого нам нужно написать скрипт, который будет в директории с локальным репозиторием обращаться по API к github, создавать PR для вливания текущей выбранной ветки в master с сообщением, которое мы вписываем в первый параметр при обращении к py-файлу (сообщение не может быть пустым). При желании, можно добавить к указанному функционалу создание новой ветки, commit и push в неё изменений конфигурации. С директорией локального репозитория можно делать всё, что угодно. Также, принимаем во внимание, что Merge Conflict у нас отсутствуют и их точно не будет при push, как в свою ветку, так и при слиянии в master. Важно получить конечный результат с созданным PR, в котором применяются наши изменения. 


> Скрипт *:

```python

root@dev1-10:/home/demi/netol_do/devops-netology# cat ./pr_gh/venv/pr-gh.py 
#!/bin/env python3

import sys
import os
import subprocess as sp
import requests

# Модель разработки - Магистральная, т.е. нужны частые изменения - в виде PR, желательно не реже 1 раза в сутки 


login_name='demiof'
master_branch_name = 'main'
new_branch_name = 'branch_api'

auto_commit_message = 'autocommit'
github_base_url='https://api.github.com/'

help_message = """
pr-gh <branch> <message>

Создаст Pull-Request для текущего репозитория. 

Параметры для передачи:
    branch - выбранная ветка
    message - сообщение для PR
"""
help_message_wrong_type="""

Не верный тип аргумента(ов)!

"""

help_message_not_git="""

Это не git репозиторий!

"""

help_message_no_PAT_within_env="""

Не найден PAT  в переменых окружения!

"""

help_message_curepo_isouton_gh="""

Текущий репозиторий не найден на GitHub!

"""


def repo_name() -> str:
    return os.path.basename(os.getcwd())

def fatal(message: str) -> None:
    print(message)
    sys.exit(1)

def is_git_repo() -> bool:
    if os.path.isdir(".git"):
        return True
    return False

def get_current_branch() -> str:
    f = open('.git/HEAD')
    s = f.read().strip()
    return s.split('/')[-1]

class GithubClient():
    def __init__(self, gh_user: str, token: str) -> None:
        s = requests.Session()
        s.auth = (gh_user,token)

        self.session = s
        self.gh_url = github_base_url
    
    def is_github_repo(self, repo_name: str) -> bool:
       
        resp = self.session.get(f"{self.gh_url}repos/{login_name}/{repo_name}")
        if resp.status_code == 200:
            return True
        return False 
    def create_pr(self, repo_name: str, branch_name: str, message: str) -> str:
        resp = self.session.post(
                    f"{self.gh_url}repos/{login_name}/{repo_name}/pulls",
                    json={
                        "title": message,
                        "head": branch_name,
                        "base": "main"
                    },
                )

        if not resp.ok:
            raise Exception(resp.json())
        
        data=resp.json()
        return data["html_url"]

if __name__ == "__main__":

    # Определяем имя репозитория, проверяем в его ли папке и сущ-е .git

    A = sys.argv
    if len(A) <= 2: 
        fatal(help_message)
    elif A[1]=='-h' or A[1]=='--help':
        fatal(help_message)
    elif type(A[1])==str and type(A[2])==str:
        
        remote_name=A[1]
        pr_message=A[2]

        if not is_git_repo():
            fatal(help_message_not_git)
        else:
            print('\nИмя удаленного репозитория - '+str(remote_name)+'\n'+'Сообщение для pull request - '+A[2]+'\n')
    else: 
        fatal(help_message_wrong_type)

    if os.environ.get('PAT_git_bash', None) is None:
        fatal(help_message_no_PAT_within_env)
    else:
        PAT_name = os.environ.get('PAT_git_bash', None)

    gh_client = GithubClient(login_name,PAT_name)
    if not gh_client.is_github_repo(repo_name()):
        fatal(help_message_curepo_isouton_gh)


    branch_name = get_current_branch()
    print(branch_name)
    try:
        url = gh_client.create_pr(repo_name(), branch_name, pr_message)
    except Exception as e:
        fatal(f"{str(e)}")
    print(f"Ссылка на PR: {url}")


```

> Вывод скрипта *:

```bash

root@dev1-10:/home/demi/netol_do/devops-netology# pr-gh origin '123'

Имя удаленного репозитория - origin
Сообщение для pull request - 123

branch_api
Ссылка на PR: https://github.com/demiof/devops-netology/pull/2

```
