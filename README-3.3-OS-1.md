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

> Похоже тут ```/etc/ld.so.preload``` так как все три раза последним сисвызовом access до read был этот файл:

	root@dev1-10:~# strace -o /home/demi/netol_do/devops-netology/strace.olg file /dev/tty
	/dev/tty: character special (5/0)
	root@dev1-10:~# grep -A 3 /dev/tty  /home/demi/netol_do/devops-netology/strace.olg
	execve("/usr/bin/file", ["file", "/dev/tty"], 0x7ffd3ce988b8 /* 25 vars */) = 0
	brk(NULL)                               = 0x55d570ba0000
	access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
	openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
	--
	lstat("/dev/tty", {st_mode=S_IFCHR|0666, st_rdev=makedev(0x5, 0), ...}) = 0
	munmap(0x7f9145fba000, 1052672)         = 0
	write(1, "/dev/tty: character special (5/0"..., 34) = 34
	munmap(0x7f91460bb000, 6645048)         = 0
	exit_group(0)                           = ?
	+++ exited with 0 +++
	
	root@dev1-10:~# strace -o /home/demi/netol_do/devops-netology/strace.olg file /bin/bash
	/bin/bash: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=3313b4cb119dcce16927a9b6cc61dcd97dfc4d59, for GNU/Linux 3.2.0, stripped
	root@dev1-10:~# grep -A 3 /bin/bash  /home/demi/netol_do/devops-netology/strace.olg
	execve("/usr/bin/file", ["file", "/bin/bash"], 0x7ffc22dad618 /* 25 vars */) = 0
	brk(NULL)                               = 0x5641237fb000
	access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
	openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
	--
	lstat("/bin/bash", {st_mode=S_IFREG|0755, st_size=1234376, ...}) = 0
	openat(AT_FDCWD, "/bin/bash", O_RDONLY|O_NONBLOCK) = 3
	fstat(3, {st_mode=S_IFREG|0755, st_size=1234376, ...}) = 0
	read(3, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0\200\6\3\0\0\0\0\0"..., 1048576) = 1048576
	mmap(NULL, 8392704, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7fa85aa45000
	--
	write(1, "/bin/bash: ELF 64-bit LSB pie ex"..., 215) = 215
	munmap(0x7fa85b347000, 6645048)         = 0
	exit_group(0)                           = ?
	+++ exited with 0 +++
	root@dev1-10:~# 



3. Предположим, приложение пишет лог в текстовый файл. Этот файл оказался удален (deleted в lsof), однако возможности сигналом сказать приложению переоткрыть файлы или просто перезапустить приложение – нет. Так как приложение продолжает писать в удаленный файл, место на диске постепенно заканчивается. Основываясь на знаниях о перенаправлении потоков предложите способ обнуления открытого удаленного файла (чтобы освободить место на файловой системе).
1. Занимают ли зомби-процессы какие-то ресурсы в ОС (CPU, RAM, IO)?
1. В iovisor BCC есть утилита `opensnoop`:
    ```bash
    root@vagrant:~# dpkg -L bpfcc-tools | grep sbin/opensnoop
    /usr/sbin/opensnoop-bpfcc
    ```
    На какие файлы вы увидели вызовы группы `open` за первую секунду работы утилиты? Воспользуйтесь пакетом `bpfcc-tools` для Ubuntu 20.04. Дополнительные [сведения по установке](https://github.com/iovisor/bcc/blob/master/INSTALL.md).
1. Какой системный вызов использует `uname -a`? Приведите цитату из man по этому системному вызову, где описывается альтернативное местоположение в `/proc`, где можно узнать версию ядра и релиз ОС.
1. Чем отличается последовательность команд через `;` и через `&&` в bash? Например:
    ```bash
    root@netology1:~# test -d /tmp/some_dir; echo Hi
    Hi
    root@netology1:~# test -d /tmp/some_dir && echo Hi
    root@netology1:~#
    ```
    Есть ли смысл использовать в bash `&&`, если применить `set -e`?
1. Из каких опций состоит режим bash `set -euxo pipefail` и почему его хорошо было бы использовать в сценариях?
1. Используя `-o stat` для `ps`, определите, какой наиболее часто встречающийся статус у процессов в системе. В `man ps` ознакомьтесь (`/PROCESS STATE CODES`) что значат дополнительные к основной заглавной буквы статуса процессов. Его можно не учитывать при расчете (считать S, Ss или Ssl равнозначными).

 
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
