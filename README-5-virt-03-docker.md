
# Домашнее задание к занятию "5.3. Введение. Экосистема. Архитектура. Жизненный цикл Docker контейнера"

## Как сдавать задания

Обязательными к выполнению являются задачи без указания звездочки. Их выполнение необходимо для получения зачета и диплома о профессиональной переподготовке.

Задачи со звездочкой (*) являются дополнительными задачами и/или задачами повышенной сложности. Они не являются обязательными к выполнению, но помогут вам глубже понять тему.

Домашнее задание выполните в файле readme.md в github репозитории. В личном кабинете отправьте на проверку ссылку на .md-файл в вашем репозитории.

Любые вопросы по решению задач задавайте в чате учебной группы.

---

## Задача 1

Сценарий выполения задачи:

- создайте свой репозиторий на https://hub.docker.com;
- выберете любой образ, который содержит веб-сервер Nginx;
- создайте свой fork образа;
- реализуйте функциональность:
запуск веб-сервера в фоне с индекс-страницей, содержащей HTML-код ниже:
```
<html>
<head>
Hey, Netology
</head>
<body>
<h1>I’m DevOps Engineer!</h1>
</body>
</html>
```
Опубликуйте созданный форк в своем репозитории и предоставьте ответ в виде ссылки на https://hub.docker.com/username_repo.

[https://hub.docker.com/layers/211526835/demiof/test/nginx_first_page/images/sha256-e117bdb844738fadffda8a1c6236a7a2644be7c640c708401ceafef1bf2b8de8?context=repo](https://hub.docker.com/layers/211526835/demiof/test/nginx_first_page/images/sha256-e117bdb844738fadffda8a1c6236a7a2644be7c640c708401ceafef1bf2b8de8?context=repo)

> Ход выполнения и содержимое Dockerfile:

```bash

root@dev1-10:~/docker/myngx# docker images
REPOSITORY      TAG       IMAGE ID       CREATED          SIZE
demi/nginx      v2        b5c41b0dd37c   6 minutes ago    25.3MB
demi/nginx      v1        d0bd8703a963   35 minutes ago   25.3MB
kasmweb/nginx   latest    95cbbc869690   6 months ago     25.3MB
hello-world     latest    feb5d9fea6a5   7 months ago     13.3kB
root@dev1-10:~/docker/myngx# docker build -t demi/nginx:v3 .
Sending build context to Docker daemon  2.048kB
Step 1/4 : FROM kasmweb/nginx
 ---> 95cbbc869690
Step 2/4 : ENV TZ=Europe/Moscow
 ---> Using cache
 ---> d9fd1fa645a9
Step 3/4 : RUN rm /usr/share/nginx/html/index.html
 ---> Using cache
 ---> 4a413b4cdbe8
Step 4/4 : RUN echo -e "<html>\n<head>\nHey, Netology\n</head>\n<body>\n<h1>I'm DevOps Engineer!</h1>\n</body>\n</html>" > /usr/share/nginx/html/index.html
 ---> Running in e1c8d8754b14
Removing intermediate container e1c8d8754b14
 ---> 891cc13b1708
Successfully built 891cc13b1708
Successfully tagged demi/nginx:v3
root@dev1-10:~/docker/myngx# docker run -d -p 8081:80 demi/nginx:v3
91aa1f9c11012e47715ab11e7d2a31fc62711afe34946856ce00e011551f77f0
root@dev1-10:~/docker/myngx# docker ps
CONTAINER ID   IMAGE           COMMAND                  CREATED         STATUS         PORTS                                   NAMES
91aa1f9c1101   demi/nginx:v3   "/docker-entrypoint.…"   4 seconds ago   Up 3 seconds   0.0.0.0:8081->80/tcp, :::8081->80/tcp   wizardly_dirac
root@dev1-10:~/docker/myngx# cat Dockerfile 
FROM kasmweb/nginx

#LABEL name="Demi" email="demi@corp.linkintel.ru"

ENV TZ=Europe/Moscow


RUN rm /usr/share/nginx/html/index.html
RUN echo -e "<html>\n<head>\nHey, Netology\n</head>\n<body>\n<h1>I'm DevOps Engineer!</h1>\n</body>\n</html>" > /usr/share/nginx/html/index.htmlroot@dev1-10:~/docker/myngx# 


```

## Задача 2

Посмотрите на сценарий ниже и ответьте на вопрос:
"Подходит ли в этом сценарии использование Docker контейнеров или лучше подойдет виртуальная машина, физическая машина? Может быть возможны разные варианты?"

Детально опишите и обоснуйте свой выбор.

--

Сценарий:

- Высоконагруженное монолитное java веб-приложение;

> С точки зрения производительности железо или ВМ, однако, учитывая удобство развертывания, выбор падает на ВМ, с учетом того, что это скореее всего Prod.

- Nodejs веб-приложение;

> В целом, наверное, за контейнеризацию, с учетом ограничений и требований по критичности к возможности потери данных и способа организации хранилища.

- Мобильное приложение c версиями для Android и iOS;

> Разные ОС - ценность и преимущества от контейнеризации теряется.

- Шина данных на базе Apache Kafka;

> Учитывая ценность данных и возможные обращения от консьюмеров за данными старых периодов, опять же не в пользу контейнеризации, хотя если storage организовать отдельно, то возможно. Железо - громоздко, ВМ более прожорливы к месту, но минимизируют риск утери данных. 

- Elasticsearch кластер для реализации логирования продуктивного веб-приложения - три ноды elasticsearch, два logstash и две ноды kibana;

> Так же удобства в развертывании, архивации и баланс производительности за ВМ, а особенно т.к., как есть требования по кластеризации, то либо, ВМ либо физика.

- Мониторинг-стек на базе Prometheus и Grafana;

> Данный мониторинговые платформы используются под различными ОС, это наталкивает на не оптимальность контейнеризации в случае необходимости использования на разл. ОС. В случае, использовани на одной системе, высокая утилизация одной, может оказать воздействие на другую мониторинговую систему (при использовании менеджера контейнеров). Поэтому выбор опять за гипервизор.  

- MongoDB, как основное хранилище данных для java-приложения;

> Кластер на железе или на ВМ - это все-таки наверняка Prod DB, но тут выбор за удобством развертывания, резервирования ... Не про контейнеры, это совсем не микросервисы.

- Gitlab сервер для реализации CI/CD процессов и приватный (закрытый) Docker Registry.

> Вполне оптимально выглядит контейнеризация. 

## Задача 3

- Запустите первый контейнер из образа ***centos*** c любым тэгом в фоновом режиме, подключив папку ```/data``` из текущей рабочей директории на хостовой машине в ```/data``` контейнера;

```bash

root@dev1-10:~/docker/test# docker images
REPOSITORY      TAG                IMAGE ID       CREATED        SIZE
demiof/test     nginx_first_page   891cc13b1708   2 hours ago    25.3MB
demi/nginx      v3                 891cc13b1708   2 hours ago    25.3MB
demi/nginx      v2                 b5c41b0dd37c   2 hours ago    25.3MB
demi/nginx      v1                 d0bd8703a963   2 hours ago    25.3MB
debian          latest             a11311205db1   2 weeks ago    124MB
kasmweb/nginx   latest             95cbbc869690   6 months ago   25.3MB
hello-world     latest             feb5d9fea6a5   7 months ago   13.3kB
root@dev1-10:~/docker/test# docker run -v /data/:/data_from_host -d kasmweb/nginx
a66d8c13d1b66f335b078cf08ec09f1bfdbccb639e9d2d64dc7736c9a7e87ff3
root@dev1-10:~/docker/test# docker ps
CONTAINER ID   IMAGE           COMMAND                  CREATED         STATUS         PORTS     NAMES
a66d8c13d1b6   kasmweb/nginx   "/docker-entrypoint.…"   4 seconds ago   Up 3 seconds   80/tcp    blissful_mayer


```

- Запустите второй контейнер из образа ***debian*** в фоновом режиме, подключив папку ```/data``` из текущей рабочей директории на хостовой машине в ```/data``` контейнера;

```bash

root@dev1-10:~/docker/test# docker run -v "/data/:/data_from_host" -it debian:bullseye /bin/sh
# 
# 
# 
# ls
bin  boot  data_from_host  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
# ls -la /data_from_host
total 84
drwxr-xr-x 20 root root  4096 May 10 20:40 .
drwxr-xr-x  1 root root  4096 May 11 07:51 ..
drwxr-xr-x  3 root root  4096 Feb  3 23:00 01FV0X2GVM6RYJTMDVWQTEY5NM
drwxr-xr-x  3 root root  4096 Feb  4 17:00 01FV2TVN3G6W7NK513S25M8EAH
drwxr-xr-x  3 root root  4096 Feb  5 11:00 01FV4RNPGPY08GRZWJ2WQCJDMY
drwxr-xr-x  3 root root  4096 Feb  6 03:00 01FV6FKC9CXT1AYZMPF7AGW4T0
drwxr-xr-x  3 root root  4096 Feb  6 23:00 01FV8M8QDJEJ6RAGM3TEH86ZRY
drwxr-xr-x  3 root root  4096 Feb  7 17:00 01FVAJ24QNH0VV717Q2WXEGJ1H
drwxr-xr-x  3 root root  4096 Feb  8 11:00 01FVCFVQRB1ZJ3DSM7D5D65CPP
drwxr-xr-x  3 root root  4096 Feb  9 05:00 01FVEDN8JE9K6X9DCC7NVEJ65Y
drwxr-xr-x  3 root root  4096 Feb  9 23:00 01FVGBEB5WYQ2CD736Q9NC63QK
drwxr-xr-x  3 root root  4096 Feb 10 17:00 01FVJ97Y0CNZAMJC9R9S8TQ46J
drwxr-xr-x  3 root root  4096 Feb 10 23:00 01FVJXVGGNKVKS5W0ZVRHHAT57
drwxr-xr-x  3 root root  4096 Feb 11 03:00 01FVKBJW50BSBVW86RC4YD522Q
drwxr-xr-x  3 root root  4096 Feb 11 05:00 01FVKJEKD3288GJQ8EKSMEHTKN
drwxr-xr-x  3 root root  4096 Feb 11 05:00 01FVKJENNB68XT86GBGJMXFD6P
drwxr-xr-x  3 root root  4096 Feb 11 07:00 01FVKS9W0MGCZ3N4QCHRR0HCCB
drwxr-xr-x  3 root root  4096 Feb 11 09:00 01FVM05K8H5A6DPHB10VDMYPHW
-rw-r--r--  1 root root     0 May 10 20:32 123
-rw-r--r--  1 root root     0 May 10 20:40 456
drwxr-xr-x  2 root root  4096 Feb 11 09:00 chunks_head
-rw-r--r--  1 root root 20001 Feb 11 10:57 queries.active
drwxr-xr-x  3 root root  4096 Feb 11 10:57 wal

```


- Подключитесь к первому контейнеру с помощью ```docker exec``` и создайте текстовый файл любого содержания в ```/data```;


```bash


root@dev1-10:~/docker/test# docker exec -it blissful_mayer /bin/sh
/ # ls -ls /data_from_host/
total 76
     4 drwxr-xr-x    3 root     root          4096 Feb  3 23:00 01FV0X2GVM6RYJTMDVWQTEY5NM
     4 drwxr-xr-x    3 root     root          4096 Feb  4 17:00 01FV2TVN3G6W7NK513S25M8EAH
     4 drwxr-xr-x    3 root     root          4096 Feb  5 11:00 01FV4RNPGPY08GRZWJ2WQCJDMY
     4 drwxr-xr-x    3 root     root          4096 Feb  6 03:00 01FV6FKC9CXT1AYZMPF7AGW4T0
     4 drwxr-xr-x    3 root     root          4096 Feb  6 23:00 01FV8M8QDJEJ6RAGM3TEH86ZRY
     4 drwxr-xr-x    3 root     root          4096 Feb  7 17:00 01FVAJ24QNH0VV717Q2WXEGJ1H
     4 drwxr-xr-x    3 root     root          4096 Feb  8 11:00 01FVCFVQRB1ZJ3DSM7D5D65CPP
     4 drwxr-xr-x    3 root     root          4096 Feb  9 05:00 01FVEDN8JE9K6X9DCC7NVEJ65Y
     4 drwxr-xr-x    3 root     root          4096 Feb  9 23:00 01FVGBEB5WYQ2CD736Q9NC63QK
     4 drwxr-xr-x    3 root     root          4096 Feb 10 17:00 01FVJ97Y0CNZAMJC9R9S8TQ46J
     4 drwxr-xr-x    3 root     root          4096 Feb 10 23:00 01FVJXVGGNKVKS5W0ZVRHHAT57
     4 drwxr-xr-x    3 root     root          4096 Feb 11 03:00 01FVKBJW50BSBVW86RC4YD522Q
     4 drwxr-xr-x    3 root     root          4096 Feb 11 05:00 01FVKJEKD3288GJQ8EKSMEHTKN
     4 drwxr-xr-x    3 root     root          4096 Feb 11 05:00 01FVKJENNB68XT86GBGJMXFD6P
     4 drwxr-xr-x    3 root     root          4096 Feb 11 07:00 01FVKS9W0MGCZ3N4QCHRR0HCCB
     4 drwxr-xr-x    3 root     root          4096 Feb 11 09:00 01FVM05K8H5A6DPHB10VDMYPHW
     4 drwxr-xr-x    2 root     root          4096 Feb 11 09:00 chunks_head
     4 -rw-r--r--    1 root     root         20001 Feb 11 10:57 queries.active
     4 drwxr-xr-x    3 root     root          4096 Feb 11 10:57 wal
/ # 


/ # touch /data_from_host/123
/ # ls -ls /data_from_host/
total 76
     4 drwxr-xr-x    3 root     root          4096 Feb  3 23:00 01FV0X2GVM6RYJTMDVWQTEY5NM
     4 drwxr-xr-x    3 root     root          4096 Feb  4 17:00 01FV2TVN3G6W7NK513S25M8EAH
     4 drwxr-xr-x    3 root     root          4096 Feb  5 11:00 01FV4RNPGPY08GRZWJ2WQCJDMY
     4 drwxr-xr-x    3 root     root          4096 Feb  6 03:00 01FV6FKC9CXT1AYZMPF7AGW4T0
     4 drwxr-xr-x    3 root     root          4096 Feb  6 23:00 01FV8M8QDJEJ6RAGM3TEH86ZRY
     4 drwxr-xr-x    3 root     root          4096 Feb  7 17:00 01FVAJ24QNH0VV717Q2WXEGJ1H
     4 drwxr-xr-x    3 root     root          4096 Feb  8 11:00 01FVCFVQRB1ZJ3DSM7D5D65CPP
     4 drwxr-xr-x    3 root     root          4096 Feb  9 05:00 01FVEDN8JE9K6X9DCC7NVEJ65Y
     4 drwxr-xr-x    3 root     root          4096 Feb  9 23:00 01FVGBEB5WYQ2CD736Q9NC63QK
     4 drwxr-xr-x    3 root     root          4096 Feb 10 17:00 01FVJ97Y0CNZAMJC9R9S8TQ46J
     4 drwxr-xr-x    3 root     root          4096 Feb 10 23:00 01FVJXVGGNKVKS5W0ZVRHHAT57
     4 drwxr-xr-x    3 root     root          4096 Feb 11 03:00 01FVKBJW50BSBVW86RC4YD522Q
     4 drwxr-xr-x    3 root     root          4096 Feb 11 05:00 01FVKJEKD3288GJQ8EKSMEHTKN
     4 drwxr-xr-x    3 root     root          4096 Feb 11 05:00 01FVKJENNB68XT86GBGJMXFD6P
     4 drwxr-xr-x    3 root     root          4096 Feb 11 07:00 01FVKS9W0MGCZ3N4QCHRR0HCCB
     4 drwxr-xr-x    3 root     root          4096 Feb 11 09:00 01FVM05K8H5A6DPHB10VDMYPHW
     0 -rw-r--r--    1 root     root             0 May 10 20:32 123
     4 drwxr-xr-x    2 root     root          4096 Feb 11 09:00 chunks_head
     4 -rw-r--r--    1 root     root         20001 Feb 11 10:57 queries.active
     4 drwxr-xr-x    3 root     root          4096 Feb 11 10:57 wal
/ # 

```


- Добавьте еще один файл в папку ```/data``` на хостовой машине;

```bash

root@dev1-10:~/docker/test# touch /data/456
root@dev1-10:~/docker/test# ls -la /data/456 
-rw-r--r-- 1 root root 0 May 10 23:40 /data/456
root@dev1-10:~/docker/test# 

```

- Подключитесь во второй контейнер и отобразите листинг и содержание файлов в ```/data``` контейнера.


```bash

root@dev1-10:~# ls -la /data
total 84
drwxr-xr-x 20 root root  4096 May 10 23:40 .
drwxr-xr-x 22 root root  4096 May  8 12:43 ..
drwxr-xr-x  3 root root  4096 Feb  4 02:00 01FV0X2GVM6RYJTMDVWQTEY5NM
drwxr-xr-x  3 root root  4096 Feb  4 20:00 01FV2TVN3G6W7NK513S25M8EAH
drwxr-xr-x  3 root root  4096 Feb  5 14:00 01FV4RNPGPY08GRZWJ2WQCJDMY
drwxr-xr-x  3 root root  4096 Feb  6 06:00 01FV6FKC9CXT1AYZMPF7AGW4T0
drwxr-xr-x  3 root root  4096 Feb  7 02:00 01FV8M8QDJEJ6RAGM3TEH86ZRY
drwxr-xr-x  3 root root  4096 Feb  7 20:00 01FVAJ24QNH0VV717Q2WXEGJ1H
drwxr-xr-x  3 root root  4096 Feb  8 14:00 01FVCFVQRB1ZJ3DSM7D5D65CPP
drwxr-xr-x  3 root root  4096 Feb  9 08:00 01FVEDN8JE9K6X9DCC7NVEJ65Y
drwxr-xr-x  3 root root  4096 Feb 10 02:00 01FVGBEB5WYQ2CD736Q9NC63QK
drwxr-xr-x  3 root root  4096 Feb 10 20:00 01FVJ97Y0CNZAMJC9R9S8TQ46J
drwxr-xr-x  3 root root  4096 Feb 11 02:00 01FVJXVGGNKVKS5W0ZVRHHAT57
drwxr-xr-x  3 root root  4096 Feb 11 06:00 01FVKBJW50BSBVW86RC4YD522Q
drwxr-xr-x  3 root root  4096 Feb 11 08:00 01FVKJEKD3288GJQ8EKSMEHTKN
drwxr-xr-x  3 root root  4096 Feb 11 08:00 01FVKJENNB68XT86GBGJMXFD6P
drwxr-xr-x  3 root root  4096 Feb 11 10:00 01FVKS9W0MGCZ3N4QCHRR0HCCB
drwxr-xr-x  3 root root  4096 Feb 11 12:00 01FVM05K8H5A6DPHB10VDMYPHW
-rw-r--r--  1 root root     0 May 10 23:32 123
-rw-r--r--  1 root root     0 May 10 23:40 456
drwxr-xr-x  2 root root  4096 Feb 11 12:00 chunks_head
-rw-r--r--  1 root root 20001 Feb 11 13:57 queries.active
drwxr-xr-x  3 root root  4096 Feb 11 13:57 wal

root@dev1-10:~# docker run -v "/data:/data_from_host" -it kasmweb/nginx /bin/sh
/ # ls -la /data_from_host
total 84
drwxr-xr-x   20 root     root          4096 May 10 20:40 .
drwxr-xr-x    1 root     root          4096 May 11 09:31 ..
drwxr-xr-x    3 root     root          4096 Feb  3 23:00 01FV0X2GVM6RYJTMDVWQTEY5NM
drwxr-xr-x    3 root     root          4096 Feb  4 17:00 01FV2TVN3G6W7NK513S25M8EAH
drwxr-xr-x    3 root     root          4096 Feb  5 11:00 01FV4RNPGPY08GRZWJ2WQCJDMY
drwxr-xr-x    3 root     root          4096 Feb  6 03:00 01FV6FKC9CXT1AYZMPF7AGW4T0
drwxr-xr-x    3 root     root          4096 Feb  6 23:00 01FV8M8QDJEJ6RAGM3TEH86ZRY
drwxr-xr-x    3 root     root          4096 Feb  7 17:00 01FVAJ24QNH0VV717Q2WXEGJ1H
drwxr-xr-x    3 root     root          4096 Feb  8 11:00 01FVCFVQRB1ZJ3DSM7D5D65CPP
drwxr-xr-x    3 root     root          4096 Feb  9 05:00 01FVEDN8JE9K6X9DCC7NVEJ65Y
drwxr-xr-x    3 root     root          4096 Feb  9 23:00 01FVGBEB5WYQ2CD736Q9NC63QK
drwxr-xr-x    3 root     root          4096 Feb 10 17:00 01FVJ97Y0CNZAMJC9R9S8TQ46J
drwxr-xr-x    3 root     root          4096 Feb 10 23:00 01FVJXVGGNKVKS5W0ZVRHHAT57
drwxr-xr-x    3 root     root          4096 Feb 11 03:00 01FVKBJW50BSBVW86RC4YD522Q
drwxr-xr-x    3 root     root          4096 Feb 11 05:00 01FVKJEKD3288GJQ8EKSMEHTKN
drwxr-xr-x    3 root     root          4096 Feb 11 05:00 01FVKJENNB68XT86GBGJMXFD6P
drwxr-xr-x    3 root     root          4096 Feb 11 07:00 01FVKS9W0MGCZ3N4QCHRR0HCCB
drwxr-xr-x    3 root     root          4096 Feb 11 09:00 01FVM05K8H5A6DPHB10VDMYPHW
-rw-r--r--    1 root     root             0 May 10 20:32 123
-rw-r--r--    1 root     root             0 May 10 20:40 456
drwxr-xr-x    2 root     root          4096 Feb 11 09:00 chunks_head
-rw-r--r--    1 root     root         20001 Feb 11 10:57 queries.active
drwxr-xr-x    3 root     root          4096 Feb 11 10:57 wal
/ # touch /data_from_host/789
/ # echo '789' > /data_from_host/789 
/ # cat /data_from_host/789
789

root@dev1-10:~# ls -la /data/ | grep 789
-rw-r--r--  1 root root     4 May 11 12:32 789
root@dev1-10:~# cat /data/789 
789
root@dev1-10:~# 

```

## Задача 4 (*)

> Ссылка на dockerhub:

[https://hub.docker.com/layers/212051323/demiof/ansible/2.9.24/images/sha256-f1c0ac54a392d720ccedca01ab7d35426379d12dd84920e083b56736c6d9b611?context=repo]:https://hub.docker.com/layers/212051323/demiof/ansible/2.9.24/images/sha256-f1c0ac54a392d720ccedca01ab7d35426379d12dd84920e083b56736c6d9b611?context=repo


> Обнаружил что 2.9.24 не рабочая и есть кментарий с решением проблемы с багом (обновления ansible до 2.9.26)

[https://github.com/ansible-community/ansible-lint-action/issues/41#issuecomment-933663572]:https://github.com/ansible-community/ansible-lint-action/issues/41#issuecomment-933663572

```bash

/ansible # ansible --version
ERROR! Unexpected Exception, this is probably a bug: cannot import name 'AnsibleCollectionLoader' from 'ansible.utils.collection_loader' (/usr/lib/python3.9/site-packages/ansible/utils/collection_loader/__init__.py)
the full traceback was:

Traceback (most recent call last):
  File "/usr/bin/ansible", line 92, in <module>
    mycli = getattr(__import__("ansible.cli.%s" % sub, fromlist=[myclass]), myclass)
  File "/usr/lib/python3.9/site-packages/ansible/cli/__init__.py", line 22, in <module>
    from ansible.inventory.manager import InventoryManager
  File "/usr/lib/python3.9/site-packages/ansible/inventory/manager.py", line 38, in <module>
    from ansible.plugins.loader import inventory_loader
  File "/usr/lib/python3.9/site-packages/ansible/plugins/loader.py", line 26, in <module>
    from ansible.utils.collection_loader import AnsibleCollectionLoader, AnsibleFlatMapLoader, AnsibleCollectionRef
ImportError: cannot import name 'AnsibleCollectionLoader' from 'ansible.utils.collection_loader' (/usr/lib/python3.9/site-packages/ansible/utils/collection_loader/__init__.py)



/ansible # sudo python3 -m pip uninstall ansible ansible-core -y
Found existing installation: ansible 2.9.24
Uninstalling ansible-2.9.24:
  Successfully uninstalled ansible-2.9.24
Found existing installation: ansible-core 2.12.5
Uninstalling ansible-core-2.12.5:
  Successfully uninstalled ansible-core-2.12.5
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
/ansible # sudo python3 -m pip install ansible==2.9.26
Collecting ansible==2.9.26
  Downloading ansible-2.9.26.tar.gz (14.3 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 14.3/14.3 MB 19.8 MB/s eta 0:00:00
  Preparing metadata (setup.py) ... done
Requirement already satisfied: jinja2 in /usr/lib/python3.9/site-packages (from ansible==2.9.26) (3.1.2)
Requirement already satisfied: PyYAML in /usr/lib/python3.9/site-packages (from ansible==2.9.26) (6.0)
Requirement already satisfied: cryptography in /usr/lib/python3.9/site-packages (from ansible==2.9.26) (37.0.2)
Requirement already satisfied: cffi>=1.12 in /usr/lib/python3.9/site-packages (from cryptography->ansible==2.9.26) (1.15.0)
Requirement already satisfied: MarkupSafe>=2.0 in /usr/lib/python3.9/site-packages (from jinja2->ansible==2.9.26) (2.1.1)
Requirement already satisfied: pycparser in /usr/lib/python3.9/site-packages (from cffi>=1.12->cryptography->ansible==2.9.26) (2.21)
Building wheels for collected packages: ansible
  Building wheel for ansible (setup.py) ... done
  Created wheel for ansible: filename=ansible-2.9.26-py3-none-any.whl size=16205999 sha256=f012decd2c45f94f6f1e9a70d1f009cb02c03a76dbf017d95b515c00a9e1447c
  Stored in directory: /root/.cache/pip/wheels/b7/28/3f/c5255737198b1bb61e633bbe3cf7d518b9a0cdd5463b03f6b9
Successfully built ansible
Installing collected packages: ansible
Successfully installed ansible-2.9.26
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
/ansible # ansible --version
ansible 2.9.26
  config file = None
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3.9/site-packages/ansible
  executable location = /usr/bin/ansible
  python version = 3.9.5 (default, Nov 24 2021, 21:19:13) [GCC 10.3.1 20210424]
/ansible # 

```


Воспроизвести практическую часть лекции самостоятельно.

Соберите Docker образ с Ansible, загрузите на Docker Hub и пришлите ссылку вместе с остальными ответами к задачам.


---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
