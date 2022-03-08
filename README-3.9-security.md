# Домашнее задание к занятию "3.9. Элементы безопасности информационных систем"

1. Установите Bitwarden плагин для браузера. Зарегестрируйтесь и сохраните несколько паролей.

> +

2. Установите Google authenticator на мобильный телефон. Настройте вход в Bitwarden акаунт через Google authenticator OTP.

> +

3. Установите apache2, сгенерируйте самоподписанный сертификат, настройте тестовый сайт для работы по HTTPS.



```bash

root@odines0:/opt/1cv8/x86_64/8.3.19.1467# systemctl reload apache2
root@odines0:/opt/1cv8/x86_64/8.3.19.1467# curl -k https://172.16.1.3/
<h1> It works! </h1>.
root@odines0:/opt/1cv8/x86_64/8.3.19.1467# curl -k https://172.16.1.3:443
<h1> It works! </h1>.
root@odines0:/opt/1cv8/x86_64/8.3.19.1467# cat /etc/apache2/sites-enabled/odines0.linkintel.ru-2.conf
<VirtualHost *:443>

ServerName odines0.linkintel.ru
DocumentRoot /var/www/html

SSLEngine on
SSLCertificateFile /etc/ssl/certs/apache-selfsigned.crt
SSLCertificateKeyFile /etc/ssl/private/apache-selfsigned.key


</VirtualHost>
root@odines0:/opt/1cv8/x86_64/8.3.19.1467# ls -la //etc/ssl/certs/apache-selfsigned.crt
-rw-r--r-- 1 root root 1375 мар  8 08:08 //etc/ssl/certs/apache-selfsigned.crt
root@odines0:/opt/1cv8/x86_64/8.3.19.1467# ls -la /etc/ssl/private/apache-selfsigned.key
-rw------- 1 root root 1704 мар  8 08:08 /etc/ssl/private/apache-selfsigned.key
root@odines0:/opt/1cv8/x86_64/8.3.19.1467#

```


4. Проверьте на TLS уязвимости произвольный сайт в интернете (кроме сайтов МВД, ФСБ, МинОбр, НацБанк, РосКосмос, РосАтом, РосНАНО и любых госкомпаний, объектов КИИ, ВПК ... и тому подобное).




```bash
root@dev1-10:~# /root/testssl/testssl.sh/testssl.sh -U --sneaky https://magmatel.ru | tee /root/testssl/magmatel.ru-U-sneaky | grep VULNERABLE
                                           VULNERABLE -- but also supports higher protocols  TLSv1.1 TLSv1.2 (likely mitigated)
 LUCKY13 (CVE-2013-0169), experimental     potentially VULNERABLE, uses cipher block chaining (CBC) ciphers with TLS. Check patches
root@dev1-10:~# 
```




5. Установите на Ubuntu ssh сервер, сгенерируйте новый приватный ключ. Скопируйте свой публичный ключ на другой сервер. Подключитесь к серверу по SSH-ключу.


```bash
demi@dev1-10:~$ ssh 192.168.1.33

Last login: Tue Mar  8 12:30:45 2022 from 192.168.1.117
demi@odines1:~$ 
```

 
6. Переименуйте файлы ключей из задания 5. Настройте файл конфигурации SSH клиента, так чтобы вход на удаленный сервер осуществлялся по имени сервера.

```bash
demi@dev1-10:~$ ssh odines1
Welcome to Ubuntu 18.04.5 LTS (GNU/Linux 4.15.0-135-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Tue Mar  8 13:01:15 MSK 2022


...





demi@odines1:~$
```







7. Соберите дамп трафика утилитой tcpdump в формате pcap, 100 пакетов. Откройте файл pcap в Wireshark.



```bash


root@dev1-10:~# tcpdump -A -n -i any host 192.168.1.117 and host 192.168.30.218 and  tcp and port 443 | tee /root/1.117-http.pcap

....









root@dev1-10:~# tail /root/1.117-http.pcap 
....rT.xW..9.D..        @.r)j...y..".!.}:...Vg.L........dj$*.r...#....9.Y?.F1.......+.-PqGoe...%D...w..F
13:16:54.075951 ens18 In  IP 192.168.30.218.26806 > 192.168.1.117.443: Flags [.], ack 14366, win 512, length 0
E..(..@.~..........uh...+0~...i.P.......
13:16:54.075987 ens18 Out IP 192.168.1.117.443 > 192.168.30.218.26806: Flags [P.], seq 14366:17008, ack 2208, win 501, length 2642
E.
z..@.@......u......h...i.+0~.P...........M.Z.eE.......Pk...../.d>..SH..RD.aU......lC...R...BA8...W.1w.R.\       ..gg..y....Xy......MJ..Q,.....5o.'Sd.....k}&C...*.}`.1..........Nw..[. X......Z...).g..w.....g..d.4M...0...."t.[p.g...,..q.9.(..W..Tp....z*w.M.&...T.~N..S........Sb.).......>0]...9-W..i1VQ.....gy......9....,.Y..Me.A..f.`^`..........K.....1u..$^.i$.e....#....
E.ge....4\d....?(.N.."...U....(.s...9........`.<s..D....\'.k..l.o...o...{.q}OQ.R..
.l...B)ZMT0...<#f.....NtR.6..T..}e5?).[.g..U%..CD..$..f{...UB.k.._.E...m,F~..<....Y.....Z.....#i...Ll..7.......#).It......a.u......jz....]....Pa$...>..:..@;d.....l?.%.\K...h.."..".Kbr.    mz...M4|;..7q...k.*..lQ.$...H..It...Kzi9..ry...y$.qAx.....s....1..j.J....m......,..e.G[...0Ia..*!]...$a....a........VJ..".~.....4...X.|.yq.......#5l...i....V^Z..U".%.@...f......tI6........*][...^................n.4..AG@.1$>.
.S._i.;Z..Ri..i.H...E....4.v.....CK.<....s-..yS..!..4....w.....8i4.&..*......;o...e.6..g".X...Q.c.l.v#DaH.C.......u..)..R..sV..=...F......{C.Af..iX..h..<....T..8.T.|F...Q....H..=.......l;.)...8..J.&.FK.[..].c.
.T...(....J.....#...d.k.(.K....;...S..."....$.....l....+..ewra..b *o..;.P-&.....H.k/vl.g.3....._....]'J.A>>...r.'.*._....&. .....'....7`t..)...0i..jR.....).............C.^.N.C7.cz..I..R.....~.&.g..~>t...a.q....2....F..!.#....&.YT.....O.E.......jV!..@A..e!..K.GO...?.C.p...{.|A<.=v0.*:H......f..im.`(. X..\.."Py.h.k..hM...*.....~Yr..P..+ .,z}<...2....,.........t.Q=.t...&HJJ..A......o.8"v\..an\..8....QS"V~0  .K......3.+..n.9B...*v(.*.F.... .....6.4u......q+3..ah./.       :r4...4Gm"|....E....pB/..9.Ul.#.Iho"{.}.7.....6..cd....     .....?..y)Z~\)?...6..7.WY.,.H..pC.E.Q......tI(.....ON$.*=1......3.root@dev1-10:~# 



```





 ---
## Задание для самостоятельной отработки (необязательно к выполнению)

8*. Просканируйте хост scanme.nmap.org. Какие сервисы запущены?

```bash

Scanning scanme.nmap.org (45.33.32.156) [1000 ports]
Discovered open port 22/tcp on 45.33.32.156
Discovered open port 80/tcp on 45.33.32.156
Discovered open port 9929/tcp on 45.33.32.156
Discovered open port 31337/tcp on 45.33.32.156

...

PORT      STATE SERVICE    VERSION
22/tcp    open  ssh        OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   1024 ac:00:a0:1a:82:ff:cc:55:99:dc:67:2b:34:97:6b:75 (DSA)
|   2048 20:3d:2d:44:62:2a:b0:5a:9d:b5:b3:05:14:c2:a6:b2 (RSA)
|   256 96:02:bb:5e:57:54:1c:4e:45:2f:56:4c:4a:24:b2:57 (ECDSA)
|_  256 33:fa:91:0f:e0:e1:7b:1f:6d:05:a2:b0:f1:54:41:56 (ED25519)
80/tcp    open  http       Apache httpd 2.4.7 ((Ubuntu))
|_http-favicon: Unknown favicon MD5: 156515DA3C0F7DC6B2493BD5CE43F795
| http-methods: 
|_  Supported Methods: OPTIONS GET HEAD POST
|_http-server-header: Apache/2.4.7 (Ubuntu)
|_http-title: Go ahead and ScanMe!
9929/tcp  open  nping-echo Nping echo
31337/tcp open  tcpwrapped

```


9*. Установите и настройте фаервол ufw на web-сервер из задания 3. Откройте доступ снаружи только к портам 22,80,443


```bash

root@odines0:~# ufw status
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
443/tcp                    ALLOW       Anywhere

root@odines0:~# ufw status verbose
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)
New profiles: skip

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW IN    Anywhere
80/tcp                     ALLOW IN    Anywhere
443/tcp                    ALLOW IN    Anywhere









root@odines0:~# ufw status
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
443/tcp                    ALLOW       Anywhere

root@odines0:~# ufw status verbose
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)
New profiles: skip

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW IN    Anywhere
80/tcp                     ALLOW IN    Anywhere
443/tcp                    ALLOW IN    Anywhere


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

Любые вопросы по решению задач задавайте в чате учебной группы.

---

