# Домашнее задание к занятию "5.5. Оркестрация кластером Docker контейнеров на примере Docker Swarm"

## Как сдавать задания

Обязательными к выполнению являются задачи без указания звездочки. Их выполнение необходимо для получения зачета и диплома о профессиональной переподготовке.

Задачи со звездочкой (*) являются дополнительными задачами и/или задачами повышенной сложности. Они не являются обязательными к выполнению, но помогут вам глубже понять тему.

Домашнее задание выполните в файле readme.md в github репозитории. В личном кабинете отправьте на проверку ссылку на .md-файл в вашем репозитории.

Любые вопросы по решению задач задавайте в чате учебной группы.

---

## Задача 1

Дайте письменые ответы на следующие вопросы:

- В чём отличие режимов работы сервисов в Docker Swarm кластере: replication и global?

> В Global - режиме система кластеризации создаст реплику на каждой ноде, в режиме replication кластер Docker Swarm исходя из заданного количеста экземпляров микросервисов, размещает их на менее загруженных worker'ах и направлять нагрузку на них. 

- Какой алгоритм выбора лидера используется в Docker Swarm кластере?

> Алгоритм Raft - алгоритм распреленного консенсуса позволяет выбирать лидера, если оставшееся кол-во лидеров более 1. При старте кластера все Последователи и только получают запросы. Если Последователи не получают запросов они становятя Кандидатами и проходят выборы. канидаты получающие большинство голосов в кластере становятся Лидерами. Лидеры рабтают до момента пока не выйдут из строя. В нормально работающем кластере два типа: Лидер, Последователь, в кластере с проблемами три: Лидер, Кандидат, Последователь. В нормально работающем кластере все запросы на последователей редиректятся на лидера. При возникновении проблем, переизберается лидер из кандидатов путем голосования. Некоторые выборы могут закончиться не определением Лидера, тогда они считаются failed. 

- Что такое Overlay Network?

> Это распределенная сеть между несколькими хостами, на которых запущен Docker демон. Связующая сущность, позволяющая контейнерами соединятся безопасно в случае включенного шифрования. Как только инициализируется кластер создается два типа сети: Overlay (так наз-ая ingress, входящий трафик к Swarm сервисам) и Bridge (так наз-ая docker_gwbridge, соединяющий индивидуальный Docker демон с другими в кластере).

## Задача 2

Создать ваш первый Docker Swarm кластер в Яндекс.Облаке

Для получения зачета, вам необходимо предоставить скриншот из терминала (консоли), с выводом команды:
```
docker node ls
```

```bash

[root@node01 ~]# docker node ls
ID                            HOSTNAME             STATUS    AVAILABILITY   MANAGER STATUS   ENGINE VERSION
jlhxtplzeu4dou5ebn3dah9kd *   node01.netology.yc   Ready     Active         Leader           20.10.16
swz9k5tjfd39rpvtcvwlut2co     node02.netology.yc   Ready     Active         Reachable        20.10.16
hxgvj4h3757cpa8cpfcp514a4     node03.netology.yc   Ready     Active         Reachable        20.10.16
0x01ilamocquxsvctqj9vh038     node04.netology.yc   Ready     Active                          20.10.16
t5l4nxe6wjtyi06v94jkflg57     node05.netology.yc   Ready     Active                          20.10.16
zlxzgeabu2u1ifg4n1faganu8     node06.netology.yc   Ready     Active                          20.10.16
[root@node01 ~]# 

```


## Задача 3

Создать ваш первый, готовый к боевой эксплуатации кластер мониторинга, состоящий из стека микросервисов.

Для получения зачета, вам необходимо предоставить скриншот из терминала (консоли), с выводом команды:
```
docker service ls
```

```bash

[root@node01 ~]# docker service ls
ID             NAME                                MODE         REPLICAS   IMAGE                                          PORTS
mitjadx8ia9s   swarm_monitoring_alertmanager       replicated   1/1        stefanprodan/swarmprom-alertmanager:v0.14.0    
7g54nhtkfhd0   swarm_monitoring_caddy              replicated   1/1        stefanprodan/caddy:latest                      *:3000->3000/tcp, *:9090->9090/tcp, *:9093-9094->9093-9094/tcp
ybbpv3x3y7jm   swarm_monitoring_cadvisor           global       6/6        google/cadvisor:latest                         
ulw5m88axt9o   swarm_monitoring_dockerd-exporter   global       6/6        stefanprodan/caddy:latest                      
04g82mk6e1o4   swarm_monitoring_grafana            replicated   1/1        stefanprodan/swarmprom-grafana:5.3.4           
0wcdp7v0hf2z   swarm_monitoring_node-exporter      global       6/6        stefanprodan/swarmprom-node-exporter:v0.16.0   
4psr2slxfver   swarm_monitoring_prometheus         replicated   1/1        stefanprodan/swarmprom-prometheus:v2.5.0       
r3sa5qkxjbs1   swarm_monitoring_unsee              replicated   1/1        cloudflare/unsee:v0.8.0                        
[root@node01 ~]# 

```


## Задача 4 (*)

Выполнить на лидере Docker Swarm кластера команду (указанную ниже) и дать письменное описание её функционала, что она делает и зачем она нужна:
```
# см.документацию: https://docs.docker.com/engine/swarm/swarm_manager_locking/
docker swarm update --autolock=true
```
> Логи Raft алгоритма Swarm, который используют менеджеры приголосовании, шифоруются по-умолчанию с помощью Docker secrets. Они обновляюются при рестарте вместе с ключами TLS, которые используются для шифрования соединений между нодами и занружаются в их память. Можно взять на себя контроль над данными ключами сняв ее с менеджеров, что есть фича --autolock. При рестарте Docker в таком случае, необходимо будет разлочить кластер swarm, используя encryption key, сгенерированный Docker. В любое время можно обновить данный encryption key.
Важная вешь: если обновляещь дянный ключ, обязательно сохрани старый, хотя бы на некоторое время, для того чтобы если менеджер отпадет до выдачи нового.

```bash

[root@node01 ~]# docker swarm update --autolock=true
Swarm updated.
To unlock a swarm manager after it restarts, run the `docker swarm unlock`
command and provide the following key:

    SWMKEY-1-cBv3Ler2ttNZwFiA05/Cu5+WoNYwYHTwOCRt5bsE2uc

Please remember to store this key in a password manager, since without it you
will not be able to restart the manager.
[root@node01 ~]# docker swarm update --autolock=false
Swarm updated.
[root@node01 ~]# 

```
