# Домашнее задание к занятию "3.1. Работа в терминале, лекция 1"

### Установите средство виртуализации Oracle VirtualBox.

> Готово.

### Установите средство автоматизации Hashicorp Vagrant.

> Готово.

# В вашем основном окружении подготовьте удобный для дальнейшей работы терминал. Можно предложить:

### iTerm2 в Mac OS Windows Terminal в Windows выбрать цветовую схему, размер окна, шрифтов и т.д. почитать о кастомизации PS1/применить при желании.

> Готово. Работал в WinPS для этого установил менеджер пакетов choco:

 choco install vim

> Преимуество относительно графической установки - отсутствие необходимости прописывать Set-Alias в $profile

### Несколько популярных проблем:

### Добавьте Vagrant в правила исключения перехватывающих трафик для анализа антивирусов, таких как Kaspersky, если у вас возникают связанные с SSL/TLS ошибки, MobaXterm может конфликтовать с Vagrant в Windows, Vagrant плохо работает с директориями с кириллицей (может быть вашей домашней директорией), тогда можно либо изменить VAGRANT_HOME, либо создать в системе профиль пользователя с английским именем, VirtualBox конфликтует с Windows Hyper-V и его необходимо отключить, WSL2 использует Hyper-V, поэтому с ним VirtualBox также несовместим, аппаратная виртуализация (Intel VT-x, AMD-V) должна быть активна в BIOS, в Linux при установке VirtualBox может дополнительно потребоваться пакет linux-headers-generic (debian-based) / kernel-devel (rhel-based). С помощью базового файла конфигурации запустите Ubuntu 20.04 в VirtualBox посредством Vagrant:

# Создайте директорию, в которой будут храниться конфигурационные файлы Vagrant. В ней выполните vagrant init. Замените содержимое Vagrantfile по умолчанию следующим:


 Vagrant.configure("2") do |config|
 	config.vm.box = "bento/ubuntu-20.04"
 end


> Готово.

# Выполнение в этой директории vagrant up установит провайдер VirtualBox для Vagrant, скачает необходимый образ и запустит виртуальную машину.

> В цикле создадим три контейнера, сконфигурим для каждого ресурсы: 

 PS C:\Users\demi\VirtualBox VMs\Vagrant> cat .\Vagrantfile
 Vagrant.configure("2") do |config|
 =begin
          config.vm.box = "bento/ubuntu-20.04"
  
          config.vm.provider "virtualbox" do |v|
                  v.name = "netodo"
                  v.linked_clone = true
          end
  =end
  
  
  
  #=begin
  (1..3).each do |i|
  
  
          config.vm.provider "virtualbox" do |v|
                  v.name = "netodo-#{i}"
          end
  
  
  end
  
  
  config.vm.define "netodo-1" do |netodo1|
          netodo1.vm.box = "gusztavvargadr/visual-studio"
          netodo1.vm.provider "virtualbox" do |v|
                  v.name = "netodo1"
                  v.gui = true
                          v.memory = 1024
                          v.cpus = 2
                          v.default_nic_type = "virtio"
                          v.linked_clone = true
          end
          netodo1.vm.network "public_network", ip: "172.16.0.1", hostname: true
          netodo1.vm.network "private_network", ip: "172.16.1.1"
          netodo1.vm.network "forwarded_port", guest: 80, host: 8080
          netodo1.vm.hostname = "netodo1"
  end

  config.vm.define "netodo-2" do |netodo2|
          netodo2.vm.box = "gusztavvargadr/windows-10"
          netodo2.vm.provider "virtualbox" do |v|
                  v.name = "netodo2"
                          v.gui = true
                          v.memory = 2048
                          v.cpus = 2
                          v.default_nic_type = "virtio"
                          v.linked_clone = true
          end
          netodo2.vm.network "public_network", ip: "172.16.0.2", hostname: true
          netodo2.vm.network "private_network", ip: "172.16.1.2"
          netodo2.vm.network "forwarded_port", guest: 80, host: 8080
          netodo2.vm.hostname = "netodo2"
  end
  
  config.vm.define "netodo-3" do |netodo3|
          netodo3.vm.box = "bento/ubuntu-20.04"
          netodo3.vm.provider "virtualbox" do |v|
                  v.name = "netodo3"
                  v.gui = true
                  v.memory = 512
                  v.cpus = 2
                  v.default_nic_type = "virtio"
                  v.linked_clone = true
          end
          netodo3.vm.network "public_network", ip: "172.16.0.3", hostname: true
          netodo3.vm.network "private_network", ip: "172.16.1.3"
          netodo3.vm.network "forwarded_port", guest: 80, host: 8080
          netodo3.vm.hostname = "netodo3"
  
  end
  
  end
  
  #=end





> В цикле создадим машины и назначи им ресурсы.



### vagrant suspend выключит виртуальную машину с сохранением ее состояния (т.е., при следующем vagrant up будут запущены все процессы внутри, которые работали на момент вызова suspend), vagrant halt выключит виртуальную машину штатным образом.

> Готово.

# Ознакомьтесь с графическим интерфейсом VirtualBox, посмотрите как выглядит виртуальная машина, которую создал для вас Vagrant, какие аппаратные ресурсы ей выделены. Какие ресурсы выделены по-умолчанию?

> CPUx1, CORESx2, RAMx1024MB, VHDDx64G (real 1,99G)

# Ознакомьтесь с возможностями конфигурации VirtualBox через Vagrantfile: документация. Как добавить оперативной памяти или ресурсов процессора виртуальной машине?



> Команда vagrant ssh из директории, в которой содержится Vagrantfile, позволит вам оказаться внутри виртуальной машины без каких-либо дополнительных настроек. Попрактикуйтесь в выполнении обсуждаемых команд в терминале Ubuntu.

# Ознакомиться с разделами man bash, почитать о настройках самого bash:

### какой переменной можно задать длину журнала history, и на какой строчке manual это описывается?

> HISTSIZE на 734 строке man - количество комманд для запоминания в истории и HISTFILESIZE на 722-й строке - максимальное количество строк содержащееся в файле ~/bash_history

### что делает директива ignoreboth в bash?

> Директива для переменной оболочки параметров bash применяет опции HISTCONTROL способ отображения историии в ~/bash_history. Одновременно применяет действие обеих директив ignorespace (не сохранять строки, начинающиеся с символа пробел) и ignoredups - не сохранять строки, совпадающие с последней выполненной коммандой.
> Например, действенно:

 export HISTSIZE=10000
 export HISTFILESIZE=10000
 export HISTCONTROL=ignoreboth:erasedups
 export PROMT_COMMAND='history -a'
 export HISTTIMEFORMAT='%d.%m.%Y %H:%M:%S: '
 
 source ~/.bashrc

> Директива erasedups - удалит все дубликаты. source ~/.bashrc применит введенные переменные оболочки, среди которых PROMT_COMMAND будет применять в ~/.bash_historyвведенное сразу, а не по завершению терминальной сессии, которая может порваться например, а HISTTIMEFORMAT установит таймстамп для каждого ввода. 
> Далее можно сохранить все в файл с помощью:
 
 cat <<EOT >> ~/.bashrc
 export HISTSIZE=10000
 export HISTFILESIZE=10000
 export HISTCONTROL=ignoreboth:erasedups
 export PROMT_COMMAND='history -a'
 export HISTTIMEFORMAT='%d.%m.%Y %H:%M:%S: '
 EOT

 source ~/.bashrc

> И отправить и применить файл на все машины. Timestamp хранится в ~/.bash_history в кол-ве сек с эпохи Юникса, но выполнение history даст то, что хотели с человекочитаемым timestamp.


### В каких сценариях использования применимы скобки {} и на какой строчке man bash это описано?

> В описании сложных комманд compound-commands, в том числе в сценариях с использованием объявления функций. В man описано, как Shell function definition на 343-й строке.
> С использованием зарезервированного слова (Rezerved words) { } (на 158-й строке) и в определении списков (lists на 227-й строке).

### С учётом ответа на предыдущий вопрос, как создать однократным вызовом touch 100000 файлов? Получится ли аналогичным образом создать 300000? Если нет, то почему?

    23  26.12.2021 15:16:47: mkdir test
    24  26.12.2021 15:16:51: cd test/
    25  26.12.2021 15:20:34: pwd
    26  26.12.2021 15:21:21: chmod 755 test.sh 
    27  26.12.2021 15:21:22: ls -la
    28  26.12.2021 15:22:15: vim test.sh
    29  26.12.2021 15:22:30: ./test.sh 
    30  26.12.2021 15:24:47: ls
    31  26.12.2021 15:24:57: ls -la ./123/
    32  26.12.2021 15:25:25: vim ./test.sh 
    33  26.12.2021 15:27:13: tail -n 20 ~/.bash_history 
    34  26.12.2021 15:27:36: history
 root@dev1-10:~/test# 
 root@dev1-10:~/test# 
 root@dev1-10:~/test# cat ./test.sh 
 #!/bin/bash
 mkdir 123
 cd 123
 for ((i=0; i<100000; i++))
         {
                 touch $i;
 
 
         }

 root@dev1-10:~/test# ls -lah ./123/ | wc -l
 100003
 root@dev1-10:~/test# 

> В данном случае, созданные файлы имеют нулевой размер, с использванием зарезвервировнанной {, поэтому 300000 не должно быть проблемой.


### В man bash поищите по /\[\[. Что делает конструкция [[ -d /tmp ]]

> Поиск с экранированием.  [[Здесь выражение и true, если /tmp существует]].  



### Основываясь на знаниях о просмотре текущих (например, PATH) и установке новых переменных; командах, которые мы рассматривали, добейтесь в выводе type -a bash в виртуальной машине наличия первым пунктом в списке:

 bash is /tmp/new_path_directory/bash
 bash is /usr/local/bin/bash
 bash is /bin/bash
### (прочие строки могут отличаться содержимым и порядком) В качестве ответа приведите команды, которые позволили вам добиться указанного вывода или соответствующие скриншоты.


 62  26.12.2021 16:14:01: export PATH=$PATH:/tmp/new_path/directory/bash/
 63  26.12.2021 16:14:02: export
 64  26.12.2021 16:16:42: ln -s /tmp/new_path/directory/bash/bash /bin/bash
 65  26.12.2021 16:17:05: ln -s /bin/bash /tmp/new_path/directory/bash/bash
 66  26.12.2021 16:17:13: ls -la /tmp/new_path/directory/bash/bash
 67  26.12.2021 16:17:22: type -a bash


 root@dev1-10:~# type -a bash
 bash is /usr/bin/bash
 bash is /bin/bash
 bash is /tmp/new_path/directory/bash/bash
 root@dev1-10:~# 

### Чем отличается планирование команд с помощью batch и at?

> Тогда как cron используется для назначения повторяющихся задач, команда at используется для назначения одноразового задания на заданное время, а команда batch — для назначения одноразовых задач, которые должны выполняться, когда загрузка системы становится меньше 0,8.

### Завершите работу виртуальной машины чтобы не расходовать ресурсы компьютера и/или батарею ноутбука.

> Готово.

 vagrant suspend -a
