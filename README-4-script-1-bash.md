### Как сдавать задания

Вы уже изучили блок «Системы управления версиями», и начиная с этого занятия все ваши работы будут приниматься ссылками на .md-файлы, размещённые в вашем публичном репозитории.

Скопируйте в свой .md-файл содержимое этого файла; исходники можно посмотреть [здесь](https://raw.githubusercontent.com/netology-code/sysadm-homeworks/devsys10/04-script-01-bash/README.md). Заполните недостающие части документа решением задач (заменяйте `???`, ОСТАЛЬНОЕ В ШАБЛОНЕ НЕ ТРОГАЙТЕ чтобы не сломать форматирование текста, подсветку синтаксиса и прочее, иначе можно отправиться на доработку) и отправляйте на проверку. Вместо логов можно вставить скриншоты по желани.

---


# Домашнее задание к занятию "4.1. Командная оболочка Bash: Практические навыки"

## Обязательная задача 1

Есть скрипт:
```bash
a=1
b=2
c=a+b
d=$a+$b
e=$(($a+$b))
```

Какие значения переменным c,d,e будут присвоены? Почему?

| Переменная  | Значение | Обоснование |
| ------------- | ------------- | ------------- |
| `c`  | a+c  | вызывались без $, обращения к значениям переменных не было |
| `d`  | 1+2  | вычисление не произошло, только конкатенация символов, значения переменных представлены как символы |
| `e`  | 3  | производилось вычисление с переменными, так как заключено в двойные скобки - выражение |


## Обязательная задача Ж2
На нашем локальном сервере упал сервис и мы написали скрипт, который постоянно проверяет его доступность, записывая дату проверок до тех пор, пока сервис не станет доступным (после чего скрипт должен завершиться). В скрипте допущена ошибка, из-за которой выполнение не может завершиться, при этом место на Жёстком Диске постоянно уменьшается. Что необходимо сделать, чтобы его исправить:
```bash
while ((1==1)
do
	curl https://localhost:4757
	if (($? != 0))
	then
		date >> curl.log
	fi
done
```

### Ваш скрипт:
```bash


while  ((1==1))
do
        curl http://localhost:4757
        if (( $? == 0 )) 
                then date >> curl.log
                else echo $?
        fi
done

```

## Обязательная задача 3
Необходимо написать скрипт, который проверяет доступность трёх IP: `192.168.0.1`, `173.194.222.113`, `87.250.250.242` по `80` порту и записывает результат в файл `log`. Проверять доступность необходимо пять раз для каждого узла.

### Ваш скрипт:
```bash


log="curl2.log"
declare -i n=5
declare -a a=("192.168.0.1" "173.194.222.113" "87.250.250.242")

if [ -f $log ] 
        then
        /usr/bin/rm $log
fi

touch $log

for i in ${a[@]} 
do
        declare -i j=1
        while  ((j<=$n)) 
        do
                        echo $i 
                        if nc -w1 -z $i 80; 
                                then date >> $log; echo "connected to $i tcp 80"  >> $log
                                else date >> $log; echo "failed to connnect to $i tcp 80" >> $log
                        fi
                let "j += 1"
        done
done



```

## Обязательная задача 4
Необходимо дописать скрипт из предыдущего задания так, чтобы он выполнялся до тех пор, пока один из узлов не окажется недоступным. Если любой из узлов недоступен - IP этого узла пишется в файл error, скрипт прерывается.

### Ваш скрипт:
```bash


root@dev1-10:/home/demi/netol_do/devops-netology#  cat ./curl_test3.sh 
#!/bin/bash
log="curl3.log"
log_err="curl3_err.log"
declare -i n=5
declare -a a=("173.194.222.113" "87.250.250.242")

if [ -f $log ] 
        then
        /usr/bin/rm $log
fi
if [ -f $log_err ]
        then
        /usr/bin/rm $log_err
fi

touch $log
touch $log_err

for i in ${a[@]} 
do
        declare -i j=1
        while  ((j<=$n)) 
        do

                nc -w1 -z $i 80; 

                if (($? != 0))
                        then 
                                echo $?
                                date >> $log_err; echo "failed to connnect to $i tcp 80" >> $log_err
                                exit
                        else

                        echo $i 
                        date >> $log; echo "connected to $i tcp 80"  >> $log

                fi


                let "j += 1"
        done

done
root@dev1-10:/home/demi/netol_do/devops-netology# ./curl_test3.sh 
173.194.222.113
173.194.222.113
173.194.222.113
173.194.222.113
173.194.222.113
0
root@dev1-10:/home/demi/netol_do/devops-netology# cat ./curl3.log 
Thu 17 Mar 2022 10:47:41 AM MSK
connected to 173.194.222.113 tcp 80
Thu 17 Mar 2022 10:47:41 AM MSK
connected to 173.194.222.113 tcp 80
Thu 17 Mar 2022 10:47:41 AM MSK
connected to 173.194.222.113 tcp 80
Thu 17 Mar 2022 10:47:41 AM MSK
connected to 173.194.222.113 tcp 80
Thu 17 Mar 2022 10:47:41 AM MSK
connected to 173.194.222.113 tcp 80
root@dev1-10:/home/demi/netol_do/devops-netology# cat ./curl3_err.log 
Thu 17 Mar 2022 10:47:42 AM MSK
failed to connnect to 192.168.0.1 tcp 80
root@dev1-10:/home/demi/netol_do/devops-netology# 

```

## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Мы хотим, чтобы у нас были красивые сообщения для коммитов в репозиторий. Для этого нужно написать локальный хук для git, который будет проверять, что сообщение в коммите содержит код текущего задания в квадратных скобках и количество символов в сообщении не превышает 30. Пример сообщения: \[04-script-01-bash\] сломал хук.



>Не взлетел скрипт. Хорошо бы понять почему ...
### Ваш скрипт:
```bash



root@dev1-10:/home/demi/netol_do/devops-netology# git --version
git version 2.30.2
root@dev1-10:/home/demi/netol_do/devops-netology# git config --list --global
user.email=demi@corp.linkintel.ru
user.name=Denis
core.hookspath=/usr/local/etc/my_hooks/
root@dev1-10:/home/demi/netol_do/devops-netology# ls -la /usr/local/etc/my_hooks/
total 12
drwxr-xr-x 2 root root 4096 Mar 17 18:35 .
drwxr-xr-x 3 root root 4096 Mar 17 18:02 ..
-rwxr-xr-x 1 root root  749 Mar 17 18:33 prepare-commit-msg
root@dev1-10:/home/demi/netol_do/devops-netology# which python3
/usr/bin/python3
root@dev1-10:/home/demi/netol_do/devops-netology# git commit 
On branch main
Your branch is up to date with 'gitlab/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   README-4-script-1-bash.md
        modified:   curl3.log
        modified:   curl3_err.log
        modified:   curl_test3.sh

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .README-3.4-OS-2.md.swp
        .README-3.5-fs.md.swm
        .README-3.5-fs.md.swn
        .README-3.5-fs.md.swo
        .README-3.6-net.md.swp
        .README-3.6-net_2.md.swh
        .README-3.6-net_2.md.swn
        .README-3.6-net_2.md.swo
        .README-3.6-net_2.md.swp
        .README-3.7-net-part2.md.swl
        .README-3.7-net-part2.md.swn
        .README-3.7-net-part2.md.swo
        .README-3.7-net-part2.md.swp
        .curl_test2.sh.swm
        .curl_test2.sh.swn
        .curl_test2.sh.swp
        .strace.olg.swo
        .strace.olg.swp

no changes added to commit (use "git add" and/or "git commit -a")
root@dev1-10:/home/demi/netol_do/devops-netology# git config --list --global
user.email=demi@corp.linkintel.ru
user.name=Denis
core.hookspath=/usr/local/etc/my_hooks/
root@dev1-10:/home/demi/netol_do/devops-netology# which python3
/usr/bin/python3
root@dev1-10:/home/demi/netol_do/devops-netology# ls -la /usr/local/etc/my_hooks/
total 12
drwxr-xr-x 2 root root 4096 Mar 17 18:35 .
drwxr-xr-x 3 root root 4096 Mar 17 18:02 ..
-rwxr-xr-x 1 root root  749 Mar 17 18:33 prepare-commit-msg
root@dev1-10:/home/demi/netol_do/devops-netology# vim /usr/local/etc/my_hooks/prepare-commit-msg
root@dev1-10:/home/demi/netol_do/devops-netology# man /usr/bin/python3 
root@dev1-10:/home/demi/netol_do/devops-netology# 
root@dev1-10:/home/demi/netol_do/devops-netology# /usr/bin/python3 -m py_compile /usr/local/etc/my_hooks/prepare-commit-msg 
root@dev1-10:/home/demi/netol_do/devops-netology# cat  /usr/local/etc/my_hooks/prepare-commit-msg 
#!/usr/bin/python3

import re
import sys



print(1111111111111111111111)









green_color = "\033[1;32m"
red_color = "\033[1;31m"
color_off = "\033[0m"
blue_color = "\033[1;34m"
yellow_color = "\033[1;33m"
commit_msg_filepath = sys.argv[1]


regex = r"^\[.+\]$"

with open(commit_msg_filepath, "r+") as file:
        commit_msg=file.read()
        if re.search(regex, commit_msg) or len(commit_msg)<30:
                print(green_color + "Good Commit " + collor_off) 
        else:
                print(red_color + "Bad commit " + blue_color + commit_msg )
                print(yellow_color + error_msg )
                print("commit-msg hook faile (add --no-verify to bypass)")
                sys.exit(1)
root@dev1-10:/home/demi/netol_do/devops-netology# git commit -m '123'
On branch main
Your branch is up to date with 'gitlab/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   README-4-script-1-bash.md
        modified:   curl3.log
        modified:   curl3_err.log
        modified:   curl_test3.sh

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .README-3.4-OS-2.md.swp
        .README-3.5-fs.md.swm
        .README-3.5-fs.md.swn
        .README-3.5-fs.md.swo
        .README-3.6-net.md.swp
        .README-3.6-net_2.md.swh
        .README-3.6-net_2.md.swn
        .README-3.6-net_2.md.swo
        .README-3.6-net_2.md.swp
        .README-3.7-net-part2.md.swl
        .README-3.7-net-part2.md.swn
        .README-3.7-net-part2.md.swo
        .README-3.7-net-part2.md.swp
        .curl_test2.sh.swm
        .curl_test2.sh.swn
        .curl_test2.sh.swp
        .strace.olg.swo
        .strace.olg.swp

no changes added to commit (use "git add" and/or "git commit -a")
root@dev1-10:/home/demi/netol_do/devops-netology# 


```
