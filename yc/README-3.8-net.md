# Домашнее задание к занятию "3.8. Компьютерные сети, лекция 3"

1. Подключитесь к публичному маршрутизатору в интернет. Найдите маршрут к вашему публичному IP
```
telnet route-views.routeviews.org
Username: rviews
show ip route x.x.x.x/32
show bgp x.x.x.x/32
```


```bash


route-views>sh ip route 176.111.72.0 255.255.248.0
Routing entry for 176.111.72.0/21
  Known via "bgp 6447", distance 20, metric 0
  Tag 6939, type external
  Last update from 64.71.137.241 3w0d ago
  Routing Descriptor Blocks:
  * 64.71.137.241, from 64.71.137.241, 3w0d ago
      Route metric is 0, traffic share count is 1
      AS Hops 4
      Route tag 6939
      MPLS label: none
route-views>


route-views>sh bgp 176.111.72.0/21
BGP routing table entry for 176.111.72.0/21, version 292880996
Paths: (23 available, best #16, table default)
  Not advertised to any peer
  Refresh Epoch 1
  8283 1299 47655 47655 47655 47655 47655
    94.142.247.3 from 94.142.247.3 (94.142.247.3)
      Origin IGP, metric 0, localpref 100, valid, external
      Community: 1299:30000 8283:1 8283:101 8283:103
      unknown transitive attribute: flag 0xE0 type 0x20 length 0x24
        value 0000 205B 0000 0000 0000 0001 0000 205B
              0000 0005 0000 0001 0000 205B 0000 0005
              0000 0003 
      path 7FE163557FE8 RPKI State valid
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  57866 9002 47655 47655 47655 47655
    37.139.139.17 from 37.139.139.17 (37.139.139.17)
      Origin IGP, metric 0, localpref 100, valid, external
      Community: 9002:0 9002:64667
      path 7FE09B509118 RPKI State valid
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  3333 9002 47655 47655 47655 47655
    193.0.0.56 from 193.0.0.56 (193.0.0.56)
      Origin IGP, localpref 100, valid, external
      path 7FE14513AD10 RPKI State valid
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  852 3356 9002 47655 47655 47655 47655
    154.11.12.212 from 154.11.12.212 (96.1.209.43)
      Origin IGP, metric 0, localpref 100, valid, external
      path 7FE0B2C65BD0 RPKI State valid
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  1351 8359 29076 47655 47655 47655 47655 47655
    132.198.255.253 from 132.198.255.253 (132.198.255.253)
      Origin IGP, localpref 100, valid, external
      path 7FE054769008 RPKI State valid
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  20130 6939 47655 47655 47655
    140.192.8.16 from 140.192.8.16 (140.192.8.16)
      Origin IGP, localpref 100, valid, external
      path 7FE030493950 RPKI State valid
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  701 1273 12389 29076 47655 47655 47655 47655 47655
    137.39.3.55 from 137.39.3.55 (137.39.3.55)
      Origin IGP, localpref 100, valid, external
      path 7FE0AD85DCE0 RPKI State valid
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  3549 3356 9002 47655 47655 47655 47655
    208.51.134.254 from 208.51.134.254 (67.16.168.191)
      Origin IGP, metric 0, localpref 100, valid, external
      Community: 3356:2 3356:22 3356:100 3356:123 3356:503 3356:901 3356:2067 3549:2581 3549:30840
      path 7FE0EE258DC8 RPKI State valid
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  53767 174 3216 3216 3216 3216 3216 3216 3216 29076 47655 47655 47655 47655 47655
    162.251.163.2 from 162.251.163.2 (162.251.162.3)
      Origin IGP, localpref 100, valid, external
      Community: 174:21101 174:22010 53767:5000
      path 7FE0CB414E90 RPKI State valid
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  3356 9002 47655 47655 47655 47655
    4.68.4.46 from 4.68.4.46 (4.69.184.201)
      Origin IGP, metric 0, localpref 100, valid, external
      Community: 3356:2 3356:22 3356:100 3356:123 3356:503 3356:901 3356:2067
      path 7FE12C803070 RPKI State valid
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  4901 6079 9002 47655 47655 47655 47655
    162.250.137.254 from 162.250.137.254 (162.250.137.254)
      Origin IGP, localpref 100, valid, external
      Community: 65000:10100 65000:10300 65000:10400
      path 7FE02697A5C8 RPKI State valid
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  20912 3257 9002 47655 47655 47655 47655
    212.66.96.126 from 212.66.96.126 (212.66.96.126)
      Origin IGP, localpref 100, valid, external
      Community: 3257:8052 3257:50001 3257:54900 3257:54901 20912:65004 65535:65284
      path 7FE11E1FC378 RPKI State valid
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  3303 6939 47655 47655 47655
    217.192.89.50 from 217.192.89.50 (138.187.128.158)
      Origin IGP, localpref 100, valid, external
      Community: 3303:1006 3303:1021 3303:1030 3303:3067 6939:7154 6939:8233 6939:9002
      path 7FE1366BEA50 RPKI State valid
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  7018 1299 47655 47655 47655 47655 47655
    12.0.1.63 from 12.0.1.63 (12.0.1.63)
      Origin IGP, localpref 100, valid, external
      Community: 7018:5000 7018:37232
      path 7FE118DAF798 RPKI State valid
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  3561 3910 3356 9002 47655 47655 47655 47655
    206.24.210.80 from 206.24.210.80 (206.24.210.80)
      Origin IGP, localpref 100, valid, external
      path 7FE07F33EF28 RPKI State valid
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  6939 47655 47655 47655
    64.71.137.241 from 64.71.137.241 (216.218.252.164)
      Origin IGP, localpref 100, valid, external, best
      unknown transitive attribute: flag 0xE0 type 0x20 length 0xC
        value 0000 21B7 0000 0777 0000 21B7 
      path 7FE0B8DBE030 RPKI State valid
      rx pathid: 0, tx pathid: 0x0
  Refresh Epoch 1
  101 3356 9002 47655 47655 47655 47655
    209.124.176.223 from 209.124.176.223 (209.124.176.223)
      Origin IGP, localpref 100, valid, external
      Community: 101:20100 101:20110 101:22100 3356:2 3356:22 3356:100 3356:123 3356:503 3356:901 3356:2067
      Extended Community: RT:101:22100
      path 7FE132330640 RPKI State valid
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 2
  2497 1299 47655 47655 47655 47655 47655
    202.232.0.2 from 202.232.0.2 (58.138.96.254)
      Origin IGP, localpref 100, valid, external
      path 7FE0F83989C8 RPKI State valid
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  7660 2516 41095 47655 47655 47655 47655 47655
    203.181.248.168 from 203.181.248.168 (203.181.248.168)
      Origin IGP, localpref 100, valid, external
      Community: 2516:1030 7660:9001
      path 7FE08938A540 RPKI State valid
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  49788 1299 47655 47655 47655 47655 47655
    91.218.184.60 from 91.218.184.60 (91.218.184.60)
      Origin IGP, localpref 100, valid, external
      Community: 1299:30000
      Extended Community: 0x43:100:1
      path 7FE02A661D80 RPKI State valid
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  1221 4637 9002 47655 47655 47655 47655
    203.62.252.83 from 203.62.252.83 (203.62.252.83)
      Origin IGP, localpref 100, valid, external
      path 7FE0F4B66398 RPKI State valid
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  3257 9002 47655 47655 47655 47655
    89.149.178.10 from 89.149.178.10 (213.200.83.26)
      Origin IGP, metric 10, localpref 100, valid, external
      Community: 3257:8052 3257:50001 3257:54900 3257:54901 65535:65284
      path 7FE179236EB8 RPKI State valid
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  19214 3257 9002 47655 47655 47655 47655
    208.74.64.40 from 208.74.64.40 (208.74.64.40)
      Origin IGP, localpref 100, valid, external
      Community: 3257:8791 3257:50001 3257:53100 3257:53101 65535:65284
      path 7FE0BDD665F0 RPKI State valid
      rx pathid: 0, tx pathid: 0
route-views> 

```



2. Создайте dummy0 интерфейс в Ubuntu. Добавьте несколько статических маршрутов. Проверьте таблицу маршрутизации.

```bash
root@dev1-10:~# systemctl restart networking.service 
root@dev1-10:~# ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: ens18: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP mode DEFAULT group default qlen 1000
    link/ether 08:00:27:d6:7b:61 brd ff:ff:ff:ff:ff:ff
    altname enp0s18
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default 
    link/ether 02:42:f3:73:db:b0 brd ff:ff:ff:ff:ff:ff
28: dummy0: <BROADCAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/ether 8a:ca:9a:2e:b0:4d brd ff:ff:ff:ff:ff:ff
root@dev1-10:~# cat /etc/network/interfaces
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

auto dummy0
iface dummy0 inet static
        address 10.2.2.2/32
        pre-up ip link add dummy0 type dummy
        post-down ip link del dummy0
root@dev1-10:~# 

```


3. Проверьте открытые TCP порты в Ubuntu, какие протоколы и приложения используют эти порты? Приведите несколько примеров.

```bash

root@dev1-10:~# netstat -tlpn
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    


root@dev1-10:~# lsof -iTCP -sTCP:LISTEN -P
COMMAND       PID        USER   FD   TYPE   DEVICE SIZE/OFF NODE NAME
root@dev1-10:~# 


```





4. Проверьте используемые UDP сокеты в Ubuntu, какие протоколы и приложения используют эти порты?


```bash

root@dev1-10:~# netstat -upn
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    


root@dev1-10:~# ss -aupn
State    Recv-Q   Send-Q                            Local Address:Port        Peer Address:Port    Process                                                          

root@dev1-10:~# lsof -iUDP -P
COMMAND      PID    USER   FD   TYPE   DEVICE SIZE/OFF NODE NAME
root@dev1-10:~# 


```

5. Используя diagrams.net, создайте L3 диаграмму вашей домашней сети или любой другой сети, с которой вы работали. 

```bash

https://viewer.diagrams.net/?highlight=0000ff&edit=_blank&layers=1&nav=1&title=25253-network.drawio#R7Vpbc5s4GP01ntl9qAdJ5vYY59LOtpnJTmYn3acOBsWokZFHyLf%2B%2BpVAXGRhr3d9IWmTh5jvQwj4ztGRDjBA17P1Rx7N03uWYDqATrIeoJsBhHDkIPmjMpsy4yFYJqacJGUKNIlH8gPrpKOzC5Lg3GgoGKOCzM1kzLIMx8LIRZyzldnsmVHzrPNoiq3EYxxRO%2FtEEpHqLHCcZscnTKapPnXg6h2TKH6ZcrbI9PkyluFyzyyqutFN8zRK2KqVQrcDdM0ZE%2BXWbH2NqSprVbHyuLsde%2BtL5jgThxyQ3i%2Bf%2FgB3s%2B%2Fu0%2F2fV09%2B8MT%2F%2BgBGZTfLiC50LfTVik1VHNmNxEEGY3kLc5WMKVvIXserlAj8OI9ilVxJashcKmZURkBu6q4xF3i986JBXQrJLsxmWPCNbFIdEOjqbWpIynjVwORVbdIWQqhKRpoa07rvpkZyQ5fpP5QM2QVKJJl0yLhI2ZRlEb1tsuOCIVj16sioafOFsbku1ncsxEaPjGghmFlKvCbiqzp86Orob92Z2r5Zt4NNK3jAnMjbxlznymtXF7wfEHl%2FbMFjvI863cBxTCNBlmb%2FXSDoQx8YkWeuAXcBMAH3kNmFiPgUC33UFpT1Zfx%2FdL0%2B0QVtbGukD0dXYsg3X9tBqycVNl0V0aYdnZsqUtIL6Pa0C89CKc81NQS68KKUCl6PYIAjKNWwqCSVqvebYJV%2FJKuOmi0qOesJ%2FVMJCnibggKcXrHveeQDcz4JUe%2FLhUMg63e4WsthOVu4SJ1qXvoPwRmlskBqtS3r41w93CxV6FF5V%2BOJ2pqqLRDCIfCCIZA4WDSoFtKz9VQZqmFM8pgNZ%2FL%2F0HcdaWnyb7%2F5LkC%2Fm9DO1RSF%2Be1SVj%2FXuSTK05ouz4TSa0YZL06DHOQFoa8W7vKqX3Brz3PxV%2B%2BpTI%2BSdLVeJ9IafYkmmD6wnAjCMrlvwoRgs1aDK0qmaodQxBxHOopxVvBnzBaCkkyetLJsDaGOsgQjH5rTOUCWJfAD2xFUuZNzxrZQN2k8v6a7OQFH8ld55js4srghKyNM2DnOyY9oUjRQRVRjPi%2BHP%2Biq%2FDZAM5IkhbYU%2FClu3x0P3JstwhTedZsrOmmq0ilQDLeMXRBYKALYZezO5etgr0v%2FU67THGTO1sAJe56v%2FQPFfxdpLiP%2BvjWQDxP3rlHcrfArIu8E53m98W3CSVHgd5m3ZB7JIdGWCBSGttC7tkJ45%2BIH9PtUiNM9HBg6vikQo57lITxUHmCf8hB2yMNnGiVs%2BRLtlQg1s7xrxBk0wvfNh4WyfaUZvWmEDfNb9PvKLY5MkXBHfs8yUT37%2F3edQL16SKdDKOSgeJFjZ69M7DAE7zJxpEzUrxlfj0xUnrXFkRYTnEOdYadX6%2FB0h1vErld6Jzd%2FnhuagIT2W71Rh%2FeD5%2FJ%2BwNsJB%2Fr14EAdL1kvCgd0X8skepQRD7fX2cirnXlfU%2BjBTrzfJ%2BddVvwzSfL9Vhy%2BT6BnmUCRY66zEbIF4rKrbHuJVTEjn0dZxY2PC5yL3ZRpSXvZRAbtw20R6vNLmK2HIb69goF%2Bh0jX3zCdHgT7ZcnPDgLyPQOFUcfC5dIowF8OhcDbWs87sHcU7PX84RV%2FRaX9EFywtDJsPn8sv7ZpPi9Ft%2F8A ---

```


## Задание для самостоятельной отработки (необязательно к выполнению)

6*. Установите Nginx, настройте в режиме балансировщика TCP или UDP.




```bash



root@dev1-10:~# cat /etc/nginx/nginx.conf 
user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;

events {
        worker_connections 768;
        # multi_accept on;
}


stream {


    server {
        listen     127.0.0.1:12345 udp;
        proxy_pass dns_servers;
    }



   upstream dns_servers {
        least_conn;
        server 194.152.34.35:53;
        server 194.152.34.39:53;
        server 194.152.34.40:53;
        # ...
    }

    # ...
}




root@dev1-10:~# ss -lnup sport = 12345
State              Recv-Q             Send-Q                         Local Address:Port                           Peer Address:Port             Process             
UNCONN             0                  0                                  127.0.0.1:12345                               0.0.0.0:*                 users:(("nginx",pid=833574,fd=5),("nginx",pid=833573,fd=5),("nginx",pid=833572,fd=5),("nginx",pid=833571,fd=5),("nginx",pid=833570,fd=5),("nginx",pid=833569,fd=5),("nginx",pid=833568,fd=5),("nginx",pid=833567,fd=5),("nginx",pid=833566,fd=5))
root@dev1-10:~# 


root@dev1-10:~# dig @127.0.0.1 -p 12345 www.ru

; <<>> DiG 9.16.22-Debian <<>> @127.0.0.1 -p 12345 www.ru
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 45767
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 5, ADDITIONAL: 11

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;www.ru.                                IN      A

;; ANSWER SECTION:
www.ru.                 704     IN      A       31.177.80.70
www.ru.                 704     IN      A       31.177.76.70

;; AUTHORITY SECTION:
ru.                     144900  IN      NS      a.dns.ripn.net.
ru.                     144900  IN      NS      e.dns.ripn.net.
ru.                     144900  IN      NS      b.dns.ripn.net.
ru.                     144900  IN      NS      f.dns.ripn.net.
ru.                     144900  IN      NS      d.dns.ripn.net.

;; ADDITIONAL SECTION:
a.dns.ripn.net.         26371   IN      A       193.232.128.6
a.dns.ripn.net.         83184   IN      AAAA    2001:678:17:0:193:232:128:6
b.dns.ripn.net.         120524  IN      A       194.85.252.62
b.dns.ripn.net.         120712  IN      AAAA    2001:678:16:0:194:85:252:62
d.dns.ripn.net.         83184   IN      A       194.190.124.17
d.dns.ripn.net.         83486   IN      AAAA    2001:678:18:0:194:190:124:17
e.dns.ripn.net.         26680   IN      A       193.232.142.17
e.dns.ripn.net.         129415  IN      AAAA    2001:678:15:0:193:232:142:17
f.dns.ripn.net.         129716  IN      A       193.232.156.17
f.dns.ripn.net.         26680   IN      AAAA    2001:678:14:0:193:232:156:17

;; Query time: 0 msec
;; SERVER: 127.0.0.1#12345(127.0.0.1)
;; WHEN: Sun Feb 27 22:51:15 MSK 2022
;; MSG SIZE  rcvd: 379

root@dev1-10:~# 


```

7*. Установите bird2, настройте динамический протокол маршрутизации RIP.


```bash

root@dev1-10:~# birdc
BIRD 2.0.7 ready.
bird> show protocols
Name       Proto      Table      State  Since         Info
device1    Device     ---        up     15:40:43.891  
direct1    Direct     ---        up     15:40:43.891  
kernel1    Kernel     master4    up     15:40:43.891  
static1    Static     master4    up     15:40:43.891  
rip1       RIP        master4    up     15:40:43.891  
bird> show rip neighbors 
rip1:
IP address                Interface  Metric Routes    Seen
bird> show route 
Table master4:
10.2.2.2/32          unicast [direct1 15:40:43.892] * (240)
        dev dummy0
bird> show interfaces 
lo up (index=1)
        MultiAccess AdminUp LinkUp Loopback Ignored MTU=65536
        127.0.0.1/8 (Preferred, scope host)
        ::1/128 (Preferred, scope host)
ens18 up (index=2)
        MultiAccess Broadcast Multicast AdminUp LinkUp MTU=1500
        192.168.1.117/24 (Preferred, scope site)
        fe80::a00:27ff:fed6:7b61/64 (Preferred, scope link)
docker0 up (index=3)
        MultiAccess Broadcast Multicast AdminUp LinkDown MTU=1500
        172.17.0.1/16 (Preferred, scope site)
        fe80::42:f3ff:fe73:dbb0/64 (Preferred, scope link)
dummy0 up (index=28)
        MultiAccess Broadcast Multicast AdminUp LinkUp MTU=1500
        10.2.2.2/32 (Preferred, scope site)
        fe80::88ca:9aff:fe2e:b04d/64 (Preferred, scope link)
bird>
```


 
8*. Установите Netbox, создайте несколько IP префиксов, используя curl проверьте работу API.


https://drive.google.com/file/d/1ILONbmgVu3m-DctPhBiPen1TBks3-LHL/view?usp=sharing








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

Любые вопросы по решению задач задавайте в чате учебной группы.

---

