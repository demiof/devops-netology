# Домашнее задание к занятию "3.2. Работа в терминале, лекция 2"

1. Какого типа команда `cd`? Попробуйте объяснить, почему она именно такого типа; опишите ход своих мыслей, если считаете что она могла бы быть другого типа.

> Так как мы знаем, что дескриптор файла привязан к идентификатору процесса, и, проверив, что при выполнении cd /home/demi появляется запись вида:
 
 root@dev1-10:/home/demi# lsof -p $$
 COMMAND    PID USER   FD   TYPE DEVICE SIZE/OFF   NODE NAME
 bash    561632 root  cwd    DIR  254,4     4096 131073 /home/demi

> то можно сказать, что:
> 1. Выполняется открытие файла и ОС создает запись-дескриптор CWD с типом DIR для представления этого файла и сохраняет информацию об этом открытом файле. 
> 1. Хотя в данная команда без дополнительных опций, и не выводит ничего в поток ошибок stderr - 2, и не выводит ничего в stdout - 1, за исключением изменения пути текущей дериктории в подписи приветствия терминала, ПРОИСХОДИТ запись информации в дескриптор cwd - current working directory.
> 1. FD означает cwd  т.е. - current working directory - имеющий тип файла DIR, и хотя это и не тип файла символьного устройства - CHR, который непосредственно является типом фаловых дескрипторов, все они хранятся в памяти.  
> 1. Именно такого типа, т.е. типа CWD, вероятно, потому-что текущая дериктория для процесса терминальной сессии может быть только одна.


 

2. Какая альтернатива без pipe команде `grep <some_string> <some_file> | wc -l`? `man grep` поможет в ответе на этот вопрос. Ознакомьтесь с [документом](http://www.smallo.ruhr.de/award.html) о других подобных некорректных вариантах использования pipe.

 grep -c cwd README-3.2-WORKING_WITHIN_TERMINAL-2.md 

> аналогично 

 root@dev1-10:/home/demi/netol_do/devops-netology# grep cwd README-3.2-WORKING_WITHIN_TERMINAL-2.md  | wc -l
 3
 root@dev1-10:/home/demi/netol_do/devops-netology# grep -c cwd README-3.2-WORKING_WITHIN_TERMINAL-2.md
 3

3. Какой процесс с PID `1` является родителем для всех процессов в вашей виртуальной машине Ubuntu 20.04?

 root@dev1-10:/home/demi/netol_do/devops-netology# ps aux -q 1
 USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
 root           1  0.0  0.2 167592  9480 ?        Ss    2021   1:59 /sbin/init

4. Как будет выглядеть команда, которая перенаправит вывод stderr `ls` на другую сессию терминала?

 root@dev1-10:/home/demi/netol_do/devops-netology# tty
 /dev/pts/0
 root@dev1-10:/home/demi/netol_do/devops-netology# ls 2>/dev/pts/1


5. Получится ли одновременно передать команде файл на stdin и вывести ее stdout в другой файл? Приведите работающий пример.



 root@dev1-10:/home/demi/netol_do/devops-netology# tty
 /dev/pts/0
 root@dev1-10:/home/demi/netol_do/devops-netology# touch test
 root@dev1-10:/home/demi/netol_do/devops-netology# echo cwd > test
 root@dev1-10:/home/demi/netol_do/devops-netology# read a < test | grep -c $a README-3.2-WORKING_WITHIN_TERMINAL-2.md > /dev/pts/1


6. Получится ли вывести находясь в графическом режиме данные из PTY в какой-либо из эмуляторов TTY? Сможете ли вы наблюдать выводимые данные?

> Да. Находясь в приложении Terminal, можно выполнить:

 root@dev1-10:/home/demi/netol_do/devops-netology# echo 123 > /dev/pts/0
 root@dev1-10:/home/demi/netol_do/devops-netology# tty
 /dev/pts/3

> В эммулированном tty 0 увидим вывод:

 root@dev1-10:/home/demi/netol_do/devops-netology# tty
 /dev/pts/0
 root@dev1-10:/home/demi/netol_do/devops-netology# 123
 
 root@dev1-10:/home/demi/netol_do/devops-netology# 





7. Выполните команду `bash 5>&1`. К чему она приведет? Что будет, если вы выполните `echo netology > /proc/$$/fd/5`? Почему так происходит?




 root@dev1-10:/home/demi/netol_do/devops-netology# bash 5>&1

> Приведет к созданию нового файлового дескриптора 5, который увидим тут:

	root@dev1-10:/home/demi/netol_do/devops-netology# ls -la /proc/$$/fd/
	total 0
	dr-x------ 2 root root  0 Jan 19 12:51 .
	dr-xr-xr-x 9 root root  0 Jan 19 12:50 ..
	lrwx------ 1 root root 64 Jan 19 12:51 0 -> /dev/pts/0
	lrwx------ 1 root root 64 Jan 19 12:51 1 -> /dev/pts/0
	lrwx------ 1 root root 64 Jan 19 12:51 2 -> /dev/pts/0
	lrwx------ 1 root root 64 Jan 19 12:51 255 -> /dev/pts/0
	lrwx------ 1 root root 64 Jan 19 12:51 5 -> /dev/pts/0
	root@dev1-10:/home/demi/netol_do/devops-netology# 

> Ниже приведет к перенаправлению 5 в stdout: 

 root@dev1-10:/home/demi/netol_do/devops-netology# echo netology > /proc/$$/fd/5
 netology
 root@dev1-10:/home/demi/netol_do/devops-netology# 

> И при попытке записи в /proc/$$/fd/5 в терминал получим 'netology'




8. Получится ли в качестве входного потока для pipe использовать только stderr команды, не потеряв при этом отображение stdout на pty? Напоминаем: по умолчанию через pipe передается только stdout команды слева от `|` на stdin команды справа.
Это можно сделать, поменяв стандартные потоки местами через промежуточный новый дескриптор, который вы научились создавать в предыдущем вопросе.



	root@dev1-10:/home/demi/netol_do/devops-netology# ./test_1_2.sh | sudo tee test_tee >2
	./test_1_2.sh: line 4: cd: 444: No such file or directory
	root@dev1-10:/home/demi/netol_do/devops-netology# cat test_tee 
	555
	root@dev1-10:/home/demi/netol_do/devops-netology# cat ./test_1_2.sh
	#! /bin/bash


	cd 444 #makes error stderr
	echo 555 #makes stdout`
	root@dev1-10:/home/demi/netol_do/devops-netology# 






9. Что выведет команда `cat /proc/$$/environ`? Как еще можно получить аналогичный по содержанию вывод?

	root@dev1-10:/home/demi/netol_do/devops-netology# cat /proc/$$/environ
	USER=rootLOGNAME=rootHOME=/rootPATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/binSHELL=/bin/bashTERM=xtermXDG_SESSION_ID=4931XDG_RUNTIME_DIR=/run/user/0DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/0/busXDG_SESSION_TYPE=ttyXDG_SESSION_CLASS=userMOTD_SHOWN=pamLANG=en_US.UTF-8SSH_CLIENT=192.168.30.218 4676 22SSH_CONNECTION=192.168.30.218 4676 192.168.1.117 22SSH_TTY=/dev/pts/8root@dev1-10:/home/demi/netol_do/devops-netology# 


	root@dev1-10:/home/demi/netol_do/devops-netology# env
	SHELL=/bin/bash
	HISTCONTROL=ignoreboth:erasedups
	HISTSIZE=10000
	HISTTIMEFORMAT=%d.%m.%Y %H:%M:%S: 
	PWD=/home/demi/netol_do/devops-netology
	LOGNAME=root
	XDG_SESSION_TYPE=tty
	MOTD_SHOWN=pam
	HOME=/root
	LANG=en_US.UTF-8
	SSH_CONNECTION=192.168.30.218 4676 192.168.1.117 22
	PROMT_COMMAND=history -a
	XDG_SESSION_CLASS=user
	TERM=xterm
	USER=root
	SHLVL=1
	XDG_SESSION_ID=4931
	XDG_RUNTIME_DIR=/run/user/0
	SSH_CLIENT=192.168.30.218 4676 22
	XDG_DATA_DIRS=/usr/local/share:/usr/share:/var/lib/snapd/desktop
	PATH=pycharm-community-2021.2.3:pycharm-community-2021.2.3/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin
	HISTFILESIZE=10000
	DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/0/bus
	SSH_TTY=/dev/pts/8
	_=/usr/bin/env
	OLDPWD=/root
	root@dev1-10:/home/demi/netol_do/devops-netology# 





10. Используя `man`, опишите что доступно по адресам `/proc/<PID>/cmdline`, `/proc/<PID>/exe`.

> `/proc/<PID>/cmdline`

> В данном файле, доступном только для чтения, содержится полная коммандная строка процесса, в противном случае, процесс является zombie. 
> В случае zombie этот доступный для чтения файл вернет 0. Аргументы коммандной строки представляются как список, разделенный пустыми байтами ('\0'), с последующим пустым (null) байтом после последней строки.
> Изменения будут показаны в данном файле, если после execve процесс изменит строку параметров. Это не идентичное (одинаковое) поведение, если прсто менять массив параметров. 
> Более того, процесс может изменить местонахождение в памяти, на который ссылается этот файл посредством prctl операциями, такими как PR_SET_MM_ARG_START.
> Файл понимается как командная строка, которой представлен (вызван) конкретный процесс под PID с номером <PID>.

> `/proc/<PID>/exe`

> В дистр. Linux с ядром 2.2 и более свежих, этот файл является символической ссылкой содержащей действ-ый путь выполненной команды.
> Например:

	root@dev1-10:~# ls -la  /proc/522803/exe
	lrwxrwxrwx 1 root root 0 Jan 20 13:09 /proc/522803/exe -> /usr/sbin/apache2
	root@dev1-10:~# pstree -p | grep apache
		   |-apache2(522803)-+-apache2(565664)
		   |                 |-apache2(565665)
		   |                 |-apache2(565667)
		   |                 |-apache2(565669)
		   |                 |-apache2(567798)
		   |                 |-apache2(567800)
		   |                 |-apache2(568249)
		   |                 |-apache2(568250)
		   |                 |-apache2(569074)
		   |                 |-apache2(569090)
		   |                 `-apache2(570930)
	root@dev1-10:~# 


> Можно по ссылке этого файла (путь на который указывает символическая ссылка) определить местонахождение исполняемой команды (процесса). Припопытке вызова этого пути, будет вызван исполняемая программа. Можно даже вызвать еще одну копию этой же программы, которая обрабатывается процессом с искомым PID. 
> Символическая станет содержать строку '(deleted)', добавленной к оригинальному пути, если имя пути будет отвязано от ссылки. В многопоточных процессах, сожержание символической ссылки не доступно, если главный поток уже был терминирован (обычно с помощью pthread_exti(3)).
> Права на отвязку ссылки или чтение обслуживается проверкой режима доступа PTRACE_MODE_READ_FSCREDS ptrace. 

> В дистр. Linux 2.0 и более старых, /proc/[pid]/exe является символической ссылкой и указателем на исполяемый бинарник. При вызове readlink, последняя вернет строку в формате:

	[device]:inode
> Например, 

	[0301]:1502 будет представлять inode 1502 на устройстве -> первые две цифры -> 03 (IDE, MFM, etc. drives) и вторые две цифры 01 (первый раздел на перовм диске).
> При помощи find с параметром -inum можно найти данный файл.

11. Узнайте, какую наиболее старшую версию набора инструкций SSE поддерживает ваш процессор с помощью `/proc/cpuinfo`.



	root@dev1-10:/home/demi/netol_do/devops-netology# cat /proc/cpuinfo | grep sse
	flags    : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx lm constant_tsc nopl xtopology cpuid tsc_known_freq pni cx16 x2apic hypervisor lahf_lm cpuid_fault pti
	flags    : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx lm constant_tsc nopl xtopology cpuid tsc_known_freq pni cx16 x2apic hypervisor lahf_lm cpuid_fault pti
	flags    : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx lm constant_tsc nopl xtopology cpuid tsc_known_freq pni cx16 x2apic hypervisor lahf_lm cpuid_fault pti
	flags    : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx lm constant_tsc nopl xtopology cpuid tsc_known_freq pni cx16 x2apic hypervisor lahf_lm cpuid_fault pti
	flags    : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx lm constant_tsc nopl xtopology cpuid tsc_known_freq pni cx16 x2apic hypervisor lahf_lm cpuid_fault pti
	flags    : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx lm constant_tsc nopl xtopology cpuid tsc_known_freq pni cx16 x2apic hypervisor lahf_lm cpuid_fault pti
	flags    : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx lm constant_tsc nopl xtopology cpuid tsc_known_freq pni cx16 x2apic hypervisor lahf_lm cpuid_fault pti
	flags    : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush mmx fxsr sse sse2 ht syscall nx lm constant_tsc nopl xtopology cpuid tsc_known_freq pni cx16 x2apic hypervisor lahf_lm cpuid_fault pti
	root@dev1-10:/home/demi/netol_do/devops-netology#






12. При открытии нового окна терминала и `vagrant ssh` создается новая сессия и выделяется pty. Это можно подтвердить командой `tty`, которая упоминалась в лекции 3.2. Однако:

    ```bash
	vagrant@netology1:~$ ssh localhost 'tty'
	not a tty
    ```

	Почитайте, почему так происходит, и как изменить поведение.

> Так происходит потому что мы запускаем ssh внутри ssh, что бы работало надо форсироват ь использование Pty на внутреннем ssh с помощью опции -t т.е.:


	vagrant@netodo-3:~$ ssh vagrant@localhost -t 'tty'
	/dev/pts/1


13. Бывает, что есть необходимость переместить запущенный процесс из одной сессии в другую. Попробуйте сделать это, воспользовавшись `reptyr`. Например, так можно перенести в `screen` процесс, который вы запустили по ошибке в обычной SSH-сессии.


> ok, reptyr 456789 перетащит выполняющийся скрипт в открытый терминал.

14. `sudo echo string > /root/new_file` не даст выполнить перенаправление под обычным пользователем, так как перенаправлением занимается процесс shell'а, который запущен без `sudo` под вашим пользователем. Для решения данной проблемы можно использовать конструкцию `echo string | sudo tee /root/new_file`. Узнайте что делает команда `tee` и почему в отличие от `sudo echo` команда с `sudo tee` будет работать.

> sudo echo работает под правами текущего пользователя и это не позводит поменять рутовые файлы. sudo tee наоборот имеет такую возможность, так же как изменять сразу несколько файлов одним вызовом. 
> sudo tee выведет в консоль добавленную в файл строку.

 ---

## Как сдавать задания

Обязательными к выполнению являются задачи без указания звездочки. Их выполнение необходимо для получения зачета и диплома о профессиональной переподготовке.

Задачи со звездочкой (*) являются дополнительными задачами и/или задачами повышенной сложности. Они не являются обязательными к выполнению, но помогут вам глубже понять тему.

Домашнее задание выполните в файле readme.md в github репозитории. В личном кабинете отправьте на проверку ссылку на .md-файл в вашем репозитории.

Также вы можете выполнить задание в [Google Docs](https://docs.google.com/document/u/0/?tgif=d) и отправить в личном кабинете на проверку ссылку на ваш документ.
Название файла Google Docs должно содержать номер лекции и фамилию студента. Пример названия: "1.1. Введение в DevOps — Сусанна Алиева".

Если необходимо прикрепить дополнительные ссылки, просто добавьте их в свой Google Docs.

Перед тем как выслать ссылку, убедитесь, что ее содержимое не является приватным (открыто на комментирование всем, у кого есть ссылка), иначе преподаватель не сможет проверить работу. Чтобы это проверить, откройте ссылку в браузере в режиме инкогнито.

[Как предоставить доступ к файлам и папкам на Google Диске](https://support.google.com/docs/answer/2494822?hl=ru&co=GENIE.Platform%3DDesktop)

[Как запустить chrome в режиме инкогнито ](https://support.google.com/chrome/answer/95464?co=GENIE.Platform%3DDesktop&hl=ru)

[Как запустить  Safari в режиме инкогнито ](https://support.apple.com/ru-ru/guide/safari/ibrw1069/mac)

Любые вопросы по решению задач задавайте в чате Slack.

---
