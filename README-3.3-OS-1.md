# Домашнее задание к занятию "3.3. Операционные системы, лекция 1"

1. Какой системный вызов делает команда `cd`? В прошлом ДЗ мы выяснили, что `cd` не является самостоятельной  программой, это `shell builtin`, поэтому запустить `strace` непосредственно на `cd` не получится. Тем не менее, вы можете запустить `strace` на `/bin/bash -c 'cd /tmp'`. В этом случае вы увидите полный список системных вызовов, которые делает сам `bash` при старте. Вам нужно найти тот единственный, который относится именно к `cd`.


	execve("/bin/bash", ["/bin/bash", "-c", "cd /tmp"], 0x7ffdaa82d0a0 /* 25 vars */) = 0


2. Попробуйте использовать команду `file` на объекты разных типов на файловой системе. Например:
    ```bash
    vagrant@netology1:~$ file /dev/tty
    /dev/tty: character special (5/0)
    vagrant@netology1:~$ file /dev/sda
    /dev/sda: block special (8/0)
    vagrant@netology1:~$ file /bin/bash
    /bin/bash: ELF 64-bit LSB shared object, x86-64
    ```
    Используя `strace` выясните, где находится база данных `file` на основании которой она делает свои догадки.

> Похоже тут ```openat(AT_FDCWD, "/usr/lib/x86_64-linux-gnu/gconv/gconv-modules.cache", O_RDONLY) = 3``` так как все три раза последним сисвызовом mmap до вывода результата был этот файл:


	root@dev1-10:/home/demi/netol_do/devops-netology# grep -B 10 "+++ exited with 0 +++" strace.olg 
	mmap(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f0517fcd000
	openat(AT_FDCWD, "/usr/lib/locale/locale-archive", O_RDONLY|O_CLOEXEC) = 3
	mmap(NULL, 3041456, PROT_READ, MAP_PRIVATE, 3, 0) = 0x7f0517ce6000
	openat(AT_FDCWD, "/etc/magic.mgc", O_RDONLY) = -1 ENOENT (No such file or directory)
	openat(AT_FDCWD, "/etc/magic", O_RDONLY) = 3
	openat(AT_FDCWD, "/usr/share/misc/magic.mgc", O_RDONLY) = 3
	mmap(NULL, 6645048, PROT_READ|PROT_WRITE, MAP_PRIVATE, 3, 0) = 0x7f051768f000
	openat(AT_FDCWD, "/usr/lib/x86_64-linux-gnu/gconv/gconv-modules.cache", O_RDONLY) = 3
	mmap(NULL, 27002, PROT_READ, MAP_SHARED, 3, 0) = 0x7f0518201000
	mmap(NULL, 1052672, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f051758e000
	+++ exited with 0 +++
	root@dev1-10:/home/demi/netol_do/devops-netology# strace -e openat,mmap -o strace.olg file /bin/bash
	/bin/bash: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=3313b4cb119dcce16927a9b6cc61dcd97dfc4d59, for GNU/Linux 3.2.0, stripped
	root@dev1-10:/home/demi/netol_do/devops-netology# grep -B 10 "+++ exited with 0 +++" strace.olg 
	openat(AT_FDCWD, "/etc/magic.mgc", O_RDONLY) = -1 ENOENT (No such file or directory)
	openat(AT_FDCWD, "/etc/magic", O_RDONLY) = 3
	openat(AT_FDCWD, "/usr/share/misc/magic.mgc", O_RDONLY) = 3
	mmap(NULL, 6645048, PROT_READ|PROT_WRITE, MAP_PRIVATE, 3, 0) = 0x7f1f19b15000
	openat(AT_FDCWD, "/usr/lib/x86_64-linux-gnu/gconv/gconv-modules.cache", O_RDONLY) = 3
	mmap(NULL, 27002, PROT_READ, MAP_SHARED, 3, 0) = 0x7f1f1a687000
	mmap(NULL, 1052672, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f1f19a14000
	openat(AT_FDCWD, "/bin/bash", O_RDONLY|O_NONBLOCK) = 3
	mmap(NULL, 8392704, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f1f19213000
	mmap(NULL, 1052672, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7f1f19112000
	+++ exited with 0 +++
	root@dev1-10:/home/demi/netol_do/devops-netology# 

> Ну если это нет так, то вилимо, что mmap читает БД прямо из памяти, т.е. из области 0х7f688aadd000

> Найдем все открытые фалй процесса с pid $pid, полчим их дескрипторы и запишем с пом. конструкции-перенаправления : > туда, освободив таким образом области памяти.
> Возможно, это нужно будет делать перодически, если дескриптооры будут наполнятся и далее процессом. 



4. Занимают ли зомби-процессы какие-то ресурсы в ОС (CPU, RAM, IO)?

> Нет, если они не осиротевшие, т.е. они просто Zombie, доч. процесс для которого не выполнен wait() родителем, а родитель с pid 1 еще не выполнил усыновление. Осиротевший или Orphan становится, например, во время оборванного удаленного сеанса, но осиротевший успел зааллокейтить ресурсов. С зомби таких проблем нет. Сиротский процесс - это пользовательский процесс, родительский процесс которого имеет init (идентификатор процесса - 1).
> Если с зомби понятно как находить (по Z в колонки STAT bsd-ого формата вывода ps, то orphan найти потруднее: кто-то предлагает отфильтровывть все процессы с ppid = 1 и пользователем != root, дополнительно можно фильтровать по CMD подстроке процесса, например:

```bash
	ps -elf | head -1; ps -elf | awk '{if ($5 == 1 && $3 != "root" && match($15,'winexe-1.00')) {print $0}}' | head
```

> Так можно получить список pid:

```bash
	ps -elf | head -1; ps -elf | awk '{if ($5 == 1 && $3 != "root") {print $0}}' | head
```



5. В iovisor BCC есть утилита `opensnoop`:
    ```bash
    root@vagrant:~# dpkg -L bpfcc-tools | grep sbin/opensnoop
    /usr/sbin/opensnoop-bpfcc
   ```
    На какие файлы вы увидели вызовы группы `open` за первую секунду работы утилиты? Воспользуйтесь пакетом `bpfcc-tools` для Ubuntu 20.04. Дополнительные [сведения по установке](https://github.com/iovisor/bcc/blob/master/INSTALL.md).


```bash
	root@dev1-10:~# opensnoop-bpfcc -ed 1
	PID    COMM               FD ERR FLAGS    PATH
	2340   watchdog            4   0 00000000 /proc/uptime
	2340   watchdog            4   0 00000000 /proc/uptime
```

6. Какой системный вызов использует `uname -a`? Приведите цитату из man по этому системному вызову, где описывается альтернативное местоположение в `/proc`, где можно узнать версию ядра и релиз ОС.

```bash
	root@dev1-10:/home/demi/netol_do/devops-netology# strace --trace='uname' uname -a
	uname({sysname="Linux", nodename="dev1-10", ...}) = 0
	Linux dev1-10 5.10.0-9-amd64 #1 SMP Debian 5.10.70-1 (2021-09-30) x86_64 GNU/Linux
	+++ exited with 0 +++
	root@dev1-10:/home/demi/netol_do/devops-netology# 
	[0] 1:bash*                                                                                                                                "dev1-10" 19:20 26-Jan-22
```

> Использует одноименный вызов uname

```bash
	NOTES       This  is  a  system call, and the operating system presumably knows its name, release and version.  It also knows what hardware it runs on.  So, four of       the fields of the struct are meaningful.  On the other hand, the field nodename is meaningless: it gives the name of the present machine in  some  unde‐       fined  network,  but  typically  machines  are  in  more than one network and have several names.  Moreover, the kernel has no way of knowing about such       things, so it has to be told what to answer here.  The same holds for the additional domainname field.       To this end, Linux uses the system calls sethostname(2) and setdomainname(2).  Note that there is no  standard  that  says  that  the  hostname  set  by       sethostname(2)  is the same string as the nodename field of the struct returned by uname() (indeed, some systems allow a 256-byte hostname and an 8-byte       nodename), but this is true on Linux.  The same holds for setdomainname(2) and the domainname field.
	       The length of the fields in the struct varies.  Some operating systems or libraries use a hardcoded 9 or 33 or 65 or 257.  Other systems use SYS_NMLN or       _SYS_NMLN or UTSLEN or _UTSNAME_LENGTH.  Clearly, it is a bad idea to use any of these constants; just use sizeof(...).  Often 257 is chosen in order to       have room for an internet hostname.
	       Part of the utsname information is also accessible via /proc/sys/kernel/{ostype, hostname, osrelease, version, domainname}.
```

```bash
	root@dev1-10:/home/demi/netol_do/devops-netology# cat /proc/sys/kernel/ostype 
	Linux
	root@dev1-10:/home/demi/netol_do/devops-netology# cat /proc/sys/kernel/hostname
	dev1-10
	root@dev1-10:/home/demi/netol_do/devops-netology# cat /proc/sys/kernel/osrelease
	5.10.0-9-amd64
	root@dev1-10:/home/demi/netol_do/devops-netology# cat /proc/sys/kernel/version
	#1 SMP Debian 5.10.70-1 (2021-09-30)
	root@dev1-10:/home/demi/netol_do/devops-netology# cat /proc/sys/kernel/domainname
	(none)
	root@dev1-10:/home/demi/netol_do/devops-netology# cat /etc/os-release 
	PRETTY_NAME="Debian GNU/Linux 11 (bullseye)"
	NAME="Debian GNU/Linux"
	VERSION_ID="11"
	VERSION="11 (bullseye)"
	VERSION_CODENAME=bullseye
	ID=debian
	HOME_URL="https://www.debian.org/"
	SUPPORT_URL="https://www.debian.org/support"
	BUG_REPORT_URL="https://bugs.debian.org/"
```



7. Чем отличается последовательность команд через `;` и через `&&` в bash? Например:

    ```bash
    root@netology1:~# test -d /tmp/some_dir; echo Hi
    Hi
	```
> В любом случае echo выведет строку 'Hi'.

	```bash
    root@netology1:~# test -d /tmp/some_dir && echo Hi
    root@netology1:~#
    ```
> Если существует файл /tmp/some_dir И он директория, то echo выведет строку 'Hi'

    Есть ли смысл использовать в bash `&&`, если применить `set -e`?


> Смысл есть. && или AND используется в списках явл. оператором сравнения  или контрольным оператором проверки усл. и возвр. true (0) если все эл./операции списка возвр. true (0). Т.к. set -e немедленно выйдет из shell, если простая команда, составляющая пайпллайн, список, или составную команду (команды разделенныя переходом символом новой строки или семиколоном) вернет false (1), за искл. случаев, когда команда следует за ключевыми словами  while, until;  являются частями зарез. слов if, elif - выполняемыми в списках || или &&, если не следуют за завершающим || (&&)  в списке (в том. числе инвертир. с пом. !). 
Т.е. в случае, если && следуют завершающими в списке или не следуют сразу за while until или if elif.


8. Из каких опций состоит режим bash `set -euxo pipefail` и почему его хорошо было бы использовать в сценариях?

> Попорядку, pipefail - если установлена, то возвращаемое значение пайплайна будет значением последней справа комнанды с не нулевым статусом либо нулевым, если статус возвращаемых значений всех команд в списке пайплайн нулевой (true). Вероятно, применяется, для того чтобы поочереди проверить всю пайплайн последовательность, выполняемую поочередно слева направо.
> Ключ -euxo - добавит, к pipefail следующее: немедленно выйдет по условиям в предыдущем вопросе, а так же выведет в stderr сообщение если произойдет немедленный выход из shell (оболочки или подоболочки), выведет текущие настройки в stdout в некотором формате. 


> Несколько проверок, весь список пайплан выполнился, вывелись тек. настройки в нек. формате (-x) и stderr сообщение:  

```bash
	root@dev1-10:~# if (set -euxo pipefail && true | ls \tmp\non_exist | true ); then echo "pipline is true!"; else echo "pipline is false \;("; fi;
	+ true
	+ ls tmpnon_exist
	+ true
	ls: cannot access 'tmpnon_exist': No such file or directory
	pipline is false \;(
```
	
> Тоже, и немедленного выхода из подоболочки не произошло:

```bash
	root@dev1-10:~# if (set -xo pipefail && true | ls \tmp\non_exist | true ); then echo "pipline is true!"; else echo "pipline is false \;("; fi;
	+ true
	+ ls tmpnon_exist
	+ true
	ls: cannot access 'tmpnon_exist': No such file or directory
	pipline is false \;(
```

> Тоже поведение даже, если последним выражением в пайплайн возвр. >0 :

```bash
	root@dev1-10:~# if (set -xo pipefail && true | ls \tmp\non_exist | false ); then echo "pipline is true!"; else echo "pipline is false \;("; fi;
	+ true
	+ ls tmpnon_exist
	+ false
	ls: cannot access 'tmpnon_exist': No such file or directory
	pipline is false \;(
```

> Тоже, не смотря на присутствие -e немедл. выхода, но с присутствием -x -o его не произошло: 

```bash
	root@dev1-10:~# if (set -exo pipefail && true | ls \tmp\non_exist | false ); then echo "pipline is true!"; else echo "pipline is false \;("; fi;
	+ true
	+ ls tmpnon_exist
	+ false
	ls: cannot access 'tmpnon_exist': No such file or directory
	pipline is false \;(
```

> Тоже, даже если добавился -u :

```bash
	root@dev1-10:~# if (set -euxo pipefail && true | ls \tmp\non_exist | false ); then echo "pipline is true!"; else echo "pipline is false \;("; fi;
	+ true
	+ ls tmpnon_exist
	+ false
	ls: cannot access 'tmpnon_exist': No such file or directory
	pipline is false \;(
```

> А вот здесь, произошол выход из подоболочки (но не оболочки!), видимо, потому что, только -e задан:

```bash
	root@dev1-10:~# if (set -e pipefail && true | ls \tmp\non_exist | false ); then echo "pipline is true!"; else echo "pipline is false \;("; fi;
	ls: cannot access 'tmpnon_exist': No such file or directory
	pipline is false \;(
	root@dev1-10:~# 
```

> Резюмируем: хорошо его использовать в сценариях, т.к. он покажет нам всех возвращаемые значения, настройки ив stdin и в stderr, для пайплан последовательности подоболочки! Хорошо для целей понимания условия, оператора условия в конкретном примере.






9. Используя `-o stat` для `ps`, определите, какой наиболее часто встречающийся статус у процессов в системе. В `man ps` ознакомьтесь (`/PROCESS STATE CODES`) что значат дополнительные к основной заглавной буквы статуса процессов. Его можно не учитывать при расчете (считать S, Ss или Ssl равнозначными).




> Больше всего процессов со статусом Sl т.е. многопоточных (l) спящих (S) с возможностью прерывания (interruptable): 

```bash
	root@dev1-10:~# ps ao stat | sort | grep Ss | wc -l
	9
	root@dev1-10:~# ps ao stat | sort | grep Sl+ | wc -l
	22
	root@dev1-10:~# ps ao stat | sort | grep Ssl+ | wc -l
	1
	root@dev1-10:~# ps ao stat | sort | grep Sl | wc -l
	27
	root@dev1-10:~# ps ao stat | sort | grep S+ | wc -l
	15
	root@dev1-10:~# ps ao stat | sort | grep R+ | wc -l
	1
```


 ```bash

	Here are the different values that the s, stat and state output specifiers (header "STAT" or "S") will display to describe the state of a process:
	               D    uninterruptible sleep (usually IO)               I    Idle kernel thread               R    running or runnable (on run queue)
	               S    interruptible sleep (waiting for an event to complete)
	               T    stopped by job control signal
	               t    stopped by debugger during the tracing
	               W    paging (not valid since the 2.6.xx kernel)
	               X    dead (should never be seen)
	               Z    defunct ("zombie") process, terminated but not reaped by its parent
	
	For BSD formats and when the stat keyword is used, additional characters may be displayed:

			<    high-priority (not nice to other users)
			N    low-priority (nice to other users)
			L    has pages locked into memory (for real-time and custom IO)
			s    is a session leader
			l    is multi-threaded (using CLONE_THREAD, like NPTL pthreads do)
			+    is in the foreground process group

```


 
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
