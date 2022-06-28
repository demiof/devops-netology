
# Домашнее задание к занятию "5.2. Применение принципов IaaC в работе с виртуальными машинами"

## Как сдавать задания

Обязательными к выполнению являются задачи без указания звездочки. Их выполнение необходимо для получения зачета и диплома о профессиональной переподготовке.

Задачи со звездочкой (*) являются дополнительными задачами и/или задачами повышенной сложности. Они не являются обязательными к выполнению, но помогут вам глубже понять тему.

Домашнее задание выполните в файле readme.md в github репозитории. В личном кабинете отправьте на проверку ссылку на .md-файл в вашем репозитории.

Любые вопросы по решению задач задавайте в чате учебной группы.

---

## Задача 1

- Опишите своими словами основные преимущества применения на практике IaaC паттернов.

> Достижение быстрого развертывания, настройки, однообразной (идемпотентной) среды.

- Какой из принципов IaaC является основополагающим?

> Ценности: 3 кита. 1) Ускорение производства, 2) Стабильность среды, 3) Более быстрая и эффективная разработка. Идемпотентнотсть - однообразное исполнение при неограниченном повторении. Как результат модель CI + CD + (CD).  Непрерывное интегрирование, доставка и деплоймент (на послежнем этапе, на практике, процедура требует ручного вмешательства). 

## Задача 2

- Чем Ansible выгодно отличается от других систем управление конфигурациями?

> Она единственная использует ssh-инфраструктуру и не требует поддержки PKI-инфраструктуры.

- Какой, на ваш взгляд, метод работы систем конфигурации более надёжный push или pull?

> Зависит от масштаба, для порядка десятков и сотен серверов вполне приемлема push, иначе pull.

## Задача 3

Установить на личный компьютер:

- VirtualBox

```bash
root@dev1-10:~# vboxmanage -v
6.1.32r149290

```


- Vagrant

```bash

root@dev1-10:~# vagrant -v
Vagrant 2.2.14

```

- Ansible

```bash

root@dev1-10:~# ansible --version
ansible 2.10.8
  config file = None
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3/dist-packages/ansible
  executable location = /usr/bin/ansible
  python version = 3.9.2 (default, Feb 28 2021, 17:03:44) [GCC 10.2.1 20210110]


```
*Приложить вывод команд установленных версий каждой из программ, оформленный в markdown.*



## Задача 4 (*)

Воспроизвести практическую часть лекции самостоятельно.

- Создать виртуальную машину.


```bash


root@dev1-10:~/vagrant# vagrant up
Bringing machine 'servers1.netology' up with 'virtualbox' provider...
==> servers1.netology: You assigned a static IP ending in ".1" to this machine.
==> servers1.netology: This is very often used by the router and can cause the
==> servers1.netology: network to not work properly. If the network doesn't work
==> servers1.netology: properly, try changing this IP.
==> servers1.netology: Importing base box 'bento/ubuntu-20.04'...
==> servers1.netology: Matching MAC address for NAT networking...
==> servers1.netology: You assigned a static IP ending in ".1" to this machine.
==> servers1.netology: This is very often used by the router and can cause the
==> servers1.netology: network to not work properly. If the network doesn't work
==> servers1.netology: properly, try changing this IP.
==> servers1.netology: Checking if box 'bento/ubuntu-20.04' version '202112.19.0' is up to date...
==> servers1.netology: There was a problem while downloading the metadata for your box
==> servers1.netology: to check for updates. This is not an error, since it is usually due
==> servers1.netology: to temporary network problems. This is just a warning. The problem
==> servers1.netology: encountered was:
==> servers1.netology: 
==> servers1.netology: The requested URL returned error: 404 Not Found
==> servers1.netology: 
==> servers1.netology: If you want to check for box updates, verify your network connection
==> servers1.netology: is valid and try again.
==> servers1.netology: Setting the name of the VM: servers1.netology
==> servers1.netology: Clearing any previously set network interfaces...
==> servers1.netology: Preparing network interfaces based on configuration...
    servers1.netology: Adapter 1: nat
    servers1.netology: Adapter 2: hostonly
==> servers1.netology: Forwarding ports...
    servers1.netology: 22 (guest) => 20011 (host) (adapter 1)
    servers1.netology: 22 (guest) => 2222 (host) (adapter 1)
==> servers1.netology: Running 'pre-boot' VM customizations...
==> servers1.netology: Booting VM...
==> servers1.netology: Waiting for machine to boot. This may take a few minutes...
    servers1.netology: SSH address: 127.0.0.1:2222
    servers1.netology: SSH username: vagrant
    servers1.netology: SSH auth method: private key
    servers1.netology: Warning: Connection reset. Retrying...
    servers1.netology: Warning: Remote connection disconnect. Retrying...
    servers1.netology: 
    servers1.netology: Vagrant insecure key detected. Vagrant will automatically replace
    servers1.netology: this with a newly generated keypair for better security.
    servers1.netology: 
    servers1.netology: Inserting generated public key within guest...
    servers1.netology: Removing insecure key from the guest if it's present...
    servers1.netology: Key inserted! Disconnecting and reconnecting using new SSH key...
==> servers1.netology: Machine booted and ready!
==> servers1.netology: Checking for guest additions in VM...
==> servers1.netology: Setting hostname...
==> servers1.netology: Configuring and enabling network interfaces...
==> servers1.netology: Mounting shared folders...
    servers1.netology: /root/vagrant => /root/vagrant
root@dev1-10:~/vagrant# vboxmanage list hostonlyifs
Name:            vboxnet0
GUID:            786f6276-656e-4074-8000-0a0027000000
DHCP:            Disabled
IPAddress:       192.168.56.1
NetworkMask:     255.255.255.0
IPV6Address:     fe80::800:27ff:fe00:0
IPV6NetworkMaskPrefixLength: 64
HardwareAddress: 0a:00:27:00:00:00
MediumType:      Ethernet
Wireless:        No
Status:          Up
VBoxNetworkName: HostInterfaceNetworking-vboxnet0

root@dev1-10:~/vagrant# vboxmanage list vms
"vagrant_default_1644337144761_97437" {61cc9233-1dcd-4f53-8661-eaa6e432e543}
"servers1.netology" {2f3db7ef-7215-4ef6-92c9-220ae8ce91d5}
root@dev1-10:~/vagrant# vagrant ssh servers1.netology
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-91-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

 System information disabled due to load higher than 1.0


This system is built by the Bento project by Chef Software
More information can be found at https://github.com/chef/bento
vagrant@servers1:~$ ip a | grep inet | grep 192
    inet 192.168.56.1/24 brd 192.168.56.255 scope global eth1
vagrant@servers1:~$ hostname -f
servers1.netology
vagrant@servers1:~$ free
              total        used        free      shared  buff/cache   available
Mem:        1004800      194500       71940         936      738360      660552
Swap:       2009084         268     2008816
vagrant@servers1:~$ free -h
              total        used        free      shared  buff/cache   available
Mem:          981Mi       135Mi       123Mi       0.0Ki       722Mi       698Mi
Swap:         1.9Gi       0.0Ki       1.9Gi
vagrant@servers1:~$ exit
logout
Connection to 127.0.0.1 closed.
root@dev1-10:~/vagrant# vagrant halt servers1.netology
==> servers1.netology: Attempting graceful shutdown of VM...
root@dev1-10:~/vagrant# vagrant status
Current machine states:

servers1.netology         poweroff (virtualbox)

The VM is powered off. To restart the VM, simply run `vagrant up`
root@dev1-10:~/vagrant# vagrant destroy 
    servers1.netology: Are you sure you want to destroy the 'servers1.netology' VM? [y/N] y
==> servers1.netology: You assigned a static IP ending in ".1" to this machine.
==> servers1.netology: This is very often used by the router and can cause the
==> servers1.netology: network to not work properly. If the network doesn't work
==> servers1.netology: properly, try changing this IP.
==> servers1.netology: Destroying VM and associated drives...
root@dev1-10:~/vagrant# vagrant status
Current machine states:

servers1.netology         not created (virtualbox)

The environment has not yet been created. Run `vagrant up` to
create the environment. If a machine is not created, only the
default provider will be shown. So if a provider is not listed,
then the machine is not created for that environment.
root@dev1-10:~/vagrant# 


```


- Зайти внутрь ВМ, убедиться, что Docker установлен с помощью команды
```
docker ps
```


```bash

root@dev1-10:~/vagrant# vagrant up
Bringing machine 'server1.netology' up with 'virtualbox' provider...
==> server1.netology: Importing base box 'bento/ubuntu-20.04'...
==> server1.netology: Matching MAC address for NAT networking...
==> server1.netology: Checking if box 'bento/ubuntu-20.04' version '202112.19.0' is up to date...
==> server1.netology: Setting the name of the VM: server1.netology
==> server1.netology: Clearing any previously set network interfaces...
==> server1.netology: Preparing network interfaces based on configuration...
    server1.netology: Adapter 1: nat
    server1.netology: Adapter 2: hostonly
==> server1.netology: Forwarding ports...
    server1.netology: 22 (guest) => 20011 (host) (adapter 1)
    server1.netology: 22 (guest) => 2222 (host) (adapter 1)
==> server1.netology: Running 'pre-boot' VM customizations...
==> server1.netology: Booting VM...
==> server1.netology: Waiting for machine to boot. This may take a few minutes...
    server1.netology: SSH address: 127.0.0.1:2222
    server1.netology: SSH username: vagrant
    server1.netology: SSH auth method: private key
    server1.netology: 
    server1.netology: Vagrant insecure key detected. Vagrant will automatically replace
    server1.netology: this with a newly generated keypair for better security.
    server1.netology: 
    server1.netology: Inserting generated public key within guest...
    server1.netology: Removing insecure key from the guest if it's present...
    server1.netology: Key inserted! Disconnecting and reconnecting using new SSH key...
==> server1.netology: Machine booted and ready!
==> server1.netology: Checking for guest additions in VM...
==> server1.netology: Setting hostname...
==> server1.netology: Configuring and enabling network interfaces...
==> server1.netology: Mounting shared folders...
    server1.netology: /root/vagrant => /root/vagrant
==> server1.netology: Running provisioner: ansible...
    server1.netology: Running ansible-playbook...

PLAY [nodes] *******************************************************************

TASK [Gathering Facts] *********************************************************
ok: [server1.netology]

TASK [Create directory for ssh-keys] *******************************************
ok: [server1.netology]

TASK [Adding rsa-key in /root/.ssh/authorized_keys] ****************************
changed: [server1.netology]

TASK [Checking DNS] ************************************************************
changed: [server1.netology]

TASK [Installing tools] ********************************************************
ok: [server1.netology] => (item=['git', 'curl'])

TASK [Installing Docker] *******************************************************
changed: [server1.netology]

TASK [Add current user to Docker group] ****************************************
changed: [server1.netology]

PLAY RECAP *********************************************************************
server1.netology           : ok=7    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

==> server1.netology: Running provisioner: ansible...
    server1.netology: Running ansible-playbook...

PLAY [nodes] *******************************************************************

TASK [Gathering Facts] *********************************************************
ok: [server1.netology]

TASK [Create directory for ssh-keys] *******************************************
ok: [server1.netology]

TASK [Adding rsa-key in /root/.ssh/authorized_keys] ****************************
ok: [server1.netology]

TASK [Checking DNS] ************************************************************
changed: [server1.netology]

TASK [Installing tools] ********************************************************
ok: [server1.netology] => (item=['git', 'curl'])

TASK [Installing Docker] *******************************************************
changed: [server1.netology]

TASK [Add current user to Docker group] ****************************************
ok: [server1.netology]

PLAY RECAP *********************************************************************
server1.netology           : ok=7    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

==> server1.netology: Running provisioner: ansible...
    server1.netology: Running ansible-playbook...

PLAY [nodes] *******************************************************************

TASK [Gathering Facts] *********************************************************
ok: [server1.netology]

TASK [Create directory for ssh-keys] *******************************************
ok: [server1.netology]

TASK [Adding rsa-key in /root/.ssh/authorized_keys] ****************************
ok: [server1.netology]

TASK [Checking DNS] ************************************************************
changed: [server1.netology]

TASK [Installing tools] ********************************************************
ok: [server1.netology] => (item=['git', 'curl'])

TASK [Installing Docker] *******************************************************
changed: [server1.netology]

TASK [Add current user to Docker group] ****************************************
ok: [server1.netology]

PLAY RECAP *********************************************************************
server1.netology           : ok=7    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

==> server1.netology: Running provisioner: ansible...
    server1.netology: Running ansible-playbook...

PLAY [nodes] *******************************************************************

TASK [Gathering Facts] *********************************************************
ok: [server1.netology]

TASK [Create directory for ssh-keys] *******************************************
ok: [server1.netology]

TASK [Adding rsa-key in /root/.ssh/authorized_keys] ****************************
ok: [server1.netology]

TASK [Checking DNS] ************************************************************
changed: [server1.netology]

TASK [Installing tools] ********************************************************
ok: [server1.netology] => (item=['git', 'curl'])

TASK [Installing Docker] *******************************************************
changed: [server1.netology]

TASK [Add current user to Docker group] ****************************************
ok: [server1.netology]

PLAY RECAP *********************************************************************
server1.netology           : ok=7    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

root@dev1-10:~/vagrant# vagrant ssh
Welcome to Ubuntu 20.04.3 LTS (GNU/Linux 5.4.0-91-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Sun 08 May 2022 11:04:24 AM UTC

  System load:  0.5                Users logged in:          0
  Usage of /:   13.6% of 30.88GB   IPv4 address for docker0: 172.17.0.1
  Memory usage: 24%                IPv4 address for eth0:    10.0.2.15
  Swap usage:   0%                 IPv4 address for eth1:    192.168.56.11
  Processes:    117


This system is built by the Bento project by Chef Software
More information can be found at https://github.com/chef/bento
Last login: Sun May  8 11:04:00 2022 from 10.0.2.2
vagrant@server1:~$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
vagrant@server1:~$ 

```