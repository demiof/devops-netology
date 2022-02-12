# Домашнее задание к занятию "3.6. Компьютерные сети, лекция 1"

1. Работа c HTTP через телнет.
- Подключитесь утилитой телнет к сайту stackoverflow.com
`telnet stackoverflow.com 80`
- отправьте HTTP запрос
```bash
GET /questions HTTP/1.0
HOST: stackoverflow.com
[press enter]
[press enter]
```
- В ответе укажите полученный HTTP код, что он означает?


```bash
root@dev1-10:~# telnet stackoverflow.com 80
Trying 151.101.193.69...
Connected to stackoverflow.com.
Escape character is '^]'.
GET /questions HTTP/1.0
HOST: stackoverflow.com

HTTP/1.1 301 Moved Permanently
cache-control: no-cache, no-store, must-revalidate
location: https://stackoverflow.com/questions
x-request-guid: c128b3ac-e452-4e4c-9a2b-1f0919bfe75c
feature-policy: microphone 'none'; speaker 'none'
content-security-policy: upgrade-insecure-requests; frame-ancestors 'self' https://stackexchange.com
Accept-Ranges: bytes
Date: Fri, 11 Feb 2022 15:15:42 GMT
Via: 1.1 varnish
Connection: close
X-Served-By: cache-hel1410024-HEL
X-Cache: MISS
X-Cache-Hits: 0
X-Timer: S1644592542.423137,VS0,VE109
Vary: Fastly-SSL
X-DNS-Prefetch-Control: off
Set-Cookie: prov=b41fd331-3305-757e-12fd-bcd6d05e5c21; domain=.stackoverflow.com; expires=Fri, 01-Jan-2055 00:00:00 GMT; path=/; HttpOnly

Connection closed by foreign host.
root@dev1-10:~# 
```

> Запрос урла /questions по прикл. протоколу HTTP версии 1.0, посредством транспортного протокола TCP, в ответ сервер по прикл. протоколу HTTP версии 1.1 вернул перманентный (постоянный) редирект 301 на uri https://stackoverflow.com/questions. 
> Далее заголовки. 
* Сервер присвоил запросу соотв-ий x-requiest-guid, который он генерирует для каждого запроса. 
* Сервер запретил функции микрофона и вопроизведения.
> ...




2. Повторите задание 1 в браузере, используя консоль разработчика F12.
- откройте вкладку `Network`
- отправьте запрос http://stackoverflow.com
- найдите первый ответ HTTP сервера, откройте вкладку `Headers`
- укажите в ответе полученный HTTP код.

- проверьте время загрузки страницы, какой запрос обрабатывался дольше всего?

> GET https://stackoverflow.com/ выполнялся дольше всех - 145.47 c

- приложите скриншот консоли браузера в ответ.


> https://cloud.mail.ru/public/pa4X/LE1ixmDcE




3. Какой IP адрес у вас в интернете?

```bash
176.111.79.84
```

4. Какому провайдеру принадлежит ваш IP адрес? Какой автономной системе AS? Воспользуйтесь утилитой `whois`




```bash

root@dev1-10:~# whois -I 176.111.79.84
% IANA WHOIS server
% for more information on IANA, visit http://www.iana.org
% This query returned 1 object

refer:        whois.ripe.net

inetnum:      176.0.0.0 - 176.255.255.255
organisation: RIPE NCC
status:       ALLOCATED

whois:        whois.ripe.net

changed:      2010-05
source:       IANA

% This is the RIPE Database query service.
% The objects are in RPSL format.
%
% The RIPE Database is subject to Terms and Conditions.
% See http://www.ripe.net/db/support/db-terms-conditions.pdf

% Note: this output has been filtered.
%       To receive output for a database update, use the "-B" flag.

% Information related to '176.111.72.0 - 176.111.79.255'

% Abuse contact for '176.111.72.0 - 176.111.79.255' is 'admin@linkintel.ru'

inetnum:        176.111.72.0 - 176.111.79.255
netname:        LINKINTEL-NET
country:        RU
org:            ORG-Ll47-RIPE
admin-c:        DM10269-RIPE
tech-c:         DM10269-RIPE
status:         ASSIGNED PI
mnt-by:         RIPE-NCC-END-MNT
mnt-by:         MNT-LINKINTEL
mnt-routes:     MNT-LINKINTEL
mnt-domains:    MNT-LINKINTEL
created:        2012-03-07T13:43:38Z
last-modified:  2016-04-14T10:23:36Z
source:         RIPE
sponsoring-org: ORG-NGs2-RIPE

organisation:   ORG-Ll47-RIPE
org-name:       LINKINTEL ltd.
org-type:       OTHER
address:        141730, Moscow reg., Lobnya, Krupskoy st., 24
abuse-c:        AR25370-RIPE
mnt-ref:        MNT-LINKINTEL
mnt-by:         MNT-LINKINTEL
created:        2008-05-12T06:45:22Z
last-modified:  2014-11-17T21:03:56Z
source:         RIPE # Filtered

person:         Denis Milovanov
address:        141730, Moscow reg., Lobnya, Krupskoy st., 24
phone:          +7 498 7057333
nic-hdl:        DM10269-RIPE
mnt-by:         MNT-LINKINTEL
created:        2012-03-06T09:36:50Z
last-modified:  2018-08-27T07:30:07Z
source:         RIPE

% Information related to '176.111.72.0/21AS47655'

route:          176.111.72.0/21
descr:          route object
origin:         AS47655
mnt-by:         MNT-LINKINTEL
created:        2012-05-04T15:08:38Z
last-modified:  2012-05-04T15:08:38Z
source:         RIPE

% This query was served by the RIPE Database Query Service version 1.102.2 (WAGYU)


root@dev1-10:~# 



```











5. Через какие сети проходит пакет, отправленный с вашего компьютера на адрес 8.8.8.8? Через какие AS? Воспользуйтесь утилитой `traceroute`



```back

root@dev1-10:~# traceroute -A 8.8.8.8
traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 60 byte packets
 1  192.168.1.11 (192.168.1.11) [*]  0.394 ms  0.323 ms  0.291 ms
 2  194.152.35.1 (194.152.35.1) [AS47655]  0.643 ms  0.586 ms  0.494 ms
 3  194.152.34.6 (194.152.34.6) [AS47655]  0.848 ms  0.722 ms  0.723 ms
 4  72.14.209.210 (72.14.209.210) [AS15169]  2.740 ms  2.692 ms  2.660 ms
 5  * * *
 6  108.170.250.33 (108.170.250.33) [AS15169]  3.559 ms 216.239.46.254 (216.239.46.254) [AS15169]  2.191 ms 72.14.233.90 (72.14.233.90) [AS15169]  2.122 ms
 7  108.170.250.130 (108.170.250.130) [AS15169]  5.614 ms  3.852 ms 108.170.250.51 (108.170.250.51) [AS15169]  3.791 ms
 8  * 142.251.49.78 (142.251.49.78) [AS15169]  16.848 ms *
 9  209.85.254.6 (209.85.254.6) [AS15169]  15.040 ms 216.239.43.20 (216.239.43.20) [AS15169]  17.151 ms 209.85.254.6 (209.85.254.6) [AS15169]  18.857 ms
10  216.239.63.25 (216.239.63.25) [AS15169]  16.654 ms 142.250.238.181 (142.250.238.181) [AS15169]  15.481 ms 209.85.251.63 (209.85.251.63) [AS15169]  14.628 ms
11  * * *
12  * * *
13  * * *
14  * * *
15  * * *
16  * * *
17  * * *
18  * * *
19  * * *
20  dns.google (8.8.8.8) [AS15169]  18.894 ms  15.973 ms *
root@dev1-10:~# 


root@dev1-10:~# traceroute -An --back --mtu 8.8.8.8
traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 65000 byte packets
 1  192.168.1.11 [*]  0.429 ms F=1500  0.384 ms  0.268 ms
 2  194.152.35.1 [AS47655]  0.615 ms  1.363 ms  0.545 ms
 3  194.152.34.6 [AS47655]  0.958 ms  0.843 ms  0.843 ms
 4  72.14.209.210 [AS15169] '-5'  2.605 ms *  5.514 ms
 5  * * *
 6  108.170.250.129 [AS15169] '-5'  3.301 ms 72.14.239.130 [AS15169] '-5'  4.317 ms 108.170.250.129 [AS15169] '-5'  2.854 ms
 7  108.170.250.51 [AS15169] '-5'  2.515 ms 108.170.250.83 [AS15169] '-5'  2.116 ms 108.170.250.66 [AS15169] '-5'  2.361 ms
 8  142.251.49.158 [AS15169] '-5'  17.910 ms 142.251.49.24 [AS15169] '-5'  18.702 ms 142.251.71.194 [AS15169] '-5'  17.578 ms
 9  216.239.48.224 [AS15169] '-5'  56.075 ms * 172.253.65.159 [AS15169] '-5'  14.636 ms
10  142.250.56.221 [AS15169] '-5'  14.852 ms 172.253.79.169 [AS15169] '-5'  16.345 ms 216.239.58.67 [AS15169] '-5'  18.186 ms
11  * * *
12  * * *
13  * * *
14  * * *
15  * * *
16  * * *
17  * * *
18  * * *
19  * * *
20  8.8.8.8 [AS15169] '-5'  16.163 ms *  16.144 ms
root@dev1-10:~# 



```
6. Повторите задание 5 в утилите `mtr`. На каком участке наибольшая задержка - delay?


```bash

root@dev1-10:~# mtr -y 0 -n -o "LSD NBAW X" -w 8.8.8.8 | awk '{if ($6!=0 && $3!="???" || $9>20) print $0}'
Start: 2022-02-12T12:11:02+0300
HOST: dev1-10                  Loss%   Snt Drop   Last  Best   Avg  Wrst  Jmax
  7. AS15169  216.239.51.32    50.0%    10    5   17.0  16.7  17.5  19.1   2.4
  8. AS15169  172.253.66.110    0.0%    10    0   20.0  20.0  20.8  23.6   3.4
root@dev1-10:~# mtr -y 1 -n -o "LSD NBAW X" -w 8.8.8.8 | awk '{if ($6!=0 && $3!="???" || $9>20) print $0}'
Start: 2022-02-12T12:11:24+0300
HOST: dev1-10                            Loss%   Snt Drop   Last  Best   Avg  Wrst  Jmax
  6. 108.170.192.0/18   108.170.250.113  10.0%    10    1    2.2   2.2   2.7   5.3   2.9
  7. 216.239.32.0/19    216.239.51.32    40.0%    10    4   18.9  16.8  17.8  18.9   1.2
  8. 172.253.0.0/16     172.253.66.110    0.0%    10    0   20.3  20.0  21.5  28.8   8.5
root@dev1-10:~# 

```

> Обпатил бы внимание на эти узлы, с оговоркой, что их  политики по обрабоке входящих в цепочку INPUT, это их политики. Но если брать цифры то наибольшая средняя из 10 попыток задержка возникает, то узла 172.253.66.110 сети 172.253.0.0/16 с AS15169.


```bash
root@dev1-10:~# whois 172.253.66.110 | grep OrgName
OrgName:        Google LLC
root@dev1-10:~# 
```

7. Какие DNS сервера отвечают за доменное имя dns.google? Какие A записи? воспользуйтесь утилитой `dig`

```bash
root@dev1-10:~# dig dns.google | grep -P "(((0|1)?[0-9][0-9]?|2[0-4][0-9]|25[0-5])[.]){3}((0|1)?[0-9][0-9]?|2[0-4][0-9]|25[0-5])$"
dns.google.             294     IN      A       8.8.8.8
dns.google.             294     IN      A       8.8.4.4
i.root-servers.net.     211730  IN      A       192.36.148.17
k.root-servers.net.     355673  IN      A       193.0.14.129
a.root-servers.net.     51042   IN      A       198.41.0.4
b.root-servers.net.     504082  IN      A       199.9.14.201
g.root-servers.net.     138130  IN      A       192.112.36.4
m.root-servers.net.     458934  IN      A       202.12.27.33
j.root-servers.net.     138130  IN      A       192.58.128.30
e.root-servers.net.     417380  IN      A       192.203.230.10
h.root-servers.net.     235252  IN      A       198.97.190.53
c.root-servers.net.     489946  IN      A       192.33.4.12
d.root-servers.net.     377693  IN      A       199.7.91.13
l.root-servers.net.     355673  IN      A       199.7.83.42
f.root-servers.net.     423113  IN      A       192.5.5.241
root@dev1-10:~# 
```

> Первые две строки A записи, остальный DNS сервера.



8. Проверьте PTR записи для IP адресов из задания 7. Какое доменное имя привязано к IP? воспользуйтесь утилитой `dig`

В качестве ответов на вопросы можно приложите лог выполнения команд в консоли или скриншот полученных результатов.


```bash

root@dev1-10:~# dig -x 8.8.4.4 | grep -A 1 ANSWER
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 6, ADDITIONAL: 6

--
;; ANSWER SECTION:
4.4.8.8.in-addr.arpa.   20287   IN      PTR     dns.google.
root@dev1-10:~# dig -x 8.8.8.8 | grep -A 1 ANSWER
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 6, ADDITIONAL: 6

--
;; ANSWER SECTION:
8.8.8.8.in-addr.arpa.   11863   IN      PTR     dns.google.
root@dev1-10:~# 

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

