# Домашнее задание к занятию "3.4. Операционные системы, лекция 2"

1. На лекции мы познакомились с [node_exporter](https://github.com/prometheus/node_exporter/releases). В демонстрации его исполняемый файл запускался в background. Этого достаточно для демо, но не для настоящей production-системы, где процессы должны находиться под внешним управлением. Используя знания из лекции по systemd, создайте самостоятельно простой [unit-файл](https://www.freedesktop.org/software/systemd/man/systemd.service.html) для node_exporter:

    * поместите его в автозагрузку,
    * предусмотрите возможность добавления опций к запускаемому процессу через внешний файл (посмотрите, например, на `systemctl cat cron`),
    * удостоверьтесь, что с помощью systemctl процесс корректно стартует, завершается, а после перезагрузки автоматически поднимается.

> Запустился без ошибок, ниже юнит-файлы:

```bash
root@dev1-10:/etc/systemd/system# sctl status prometheus
● prometheus.service - Prometheus-2.33.0.linux-amd64
     Loaded: loaded (/etc/systemd/system/prometheus.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2022-02-03 10:47:03 MSK; 5s ago
   Main PID: 671557 (prometheus)
      Tasks: 11 (limit: 4657)
     Memory: 19.2M
        CPU: 193ms
     CGroup: /system.slice/prometheus.service
             └─671557 /root/prometheus-2.33.0.linux-amd64/prometheus --config.file=/root/prometheus-2.33.0.linux-amd64/prometheus.yml

Feb 03 10:47:04 dev1-10 prometheus[671557]: ts=2022-02-03T07:47:04.027Z caller=head.go:527 level=info component=tsdb msg="On-disk memory mappable chunks replay com>Feb 03 10:47:04 dev1-10 prometheus[671557]: ts=2022-02-03T07:47:04.027Z caller=head.go:533 level=info component=tsdb msg="Replaying WAL, this may take a while"
Feb 03 10:47:04 dev1-10 prometheus[671557]: ts=2022-02-03T07:47:04.027Z caller=tls_config.go:195 level=info component=web msg="TLS is disabled." http2=false
Feb 03 10:47:04 dev1-10 prometheus[671557]: ts=2022-02-03T07:47:04.030Z caller=head.go:604 level=info component=tsdb msg="WAL segment loaded" segment=0 maxSegment=0Feb 03 10:47:04 dev1-10 prometheus[671557]: ts=2022-02-03T07:47:04.030Z caller=head.go:610 level=info component=tsdb msg="WAL replay completed" checkpoint_replay_d>Feb 03 10:47:04 dev1-10 prometheus[671557]: ts=2022-02-03T07:47:04.035Z caller=main.go:944 level=info fs_type=EXT4_SUPER_MAGIC
Feb 03 10:47:04 dev1-10 prometheus[671557]: ts=2022-02-03T07:47:04.035Z caller=main.go:947 level=info msg="TSDB started"
Feb 03 10:47:04 dev1-10 prometheus[671557]: ts=2022-02-03T07:47:04.035Z caller=main.go:1128 level=info msg="Loading configuration file" filename=/root/prometheus-2>Feb 03 10:47:04 dev1-10 prometheus[671557]: ts=2022-02-03T07:47:04.037Z caller=main.go:1165 level=info msg="Completed loading of configuration file" filename=/root>Feb 03 10:47:04 dev1-10 prometheus[671557]: ts=2022-02-03T07:47:04.037Z caller=main.go:896 level=info msg="Server is ready to receive web requests."
lines 1-20/20 (END)



```


> Сами юнит-файлы:

```bash

root@dev1-10:/etc/systemd/system# systemctl cat  prometheus.service 
# /etc/systemd/system/prometheus.service
[Unit]
Description=Prometheus-2.33.0.linux-amd64
After=network-online.target mysqld.service apache2.service memcached.service node_exporter.service
Requires=network-online.target mysqld.service apache2.service memcached.service node_exporter.service


[Install]
WantedBy=multi-user.target


[Service]
ExecStart=/root/prometheus-2.33.0.linux-amd64/prometheus --config.file=/root/prometheus-2.33.0.linux-amd64/prometheus.yml

root@dev1-10:/etc/systemd/system# sctl cat node_exporter.service
# /etc/systemd/system/node_exporter.service
[Unit]
Description=node_exporter-1.3.1.linux-amd64
After=network-online.target apache2.service memcached.service 
Requires=network-online.target apache2.service memcached.service

[Install]
WantedBy=multi-user.target


[Service]
ExecStart=/root/node_exporter-1.3.1.linux-amd64/node_exporter

# /etc/systemd/system/node_exporter.service.d/override.conf

root@dev1-10:/etc/systemd/system# 


```

> Посмотрим зависимости юнит-файла prometheus.service


```bash

rometheus.service
● ├─apache2.service
● ├─memcached.service
● ├─mysqld.service
● ├─node_exporter.service
● ├─system.slice
● ├─network-online.target
● │ ├─networking.service
● │ └─NetworkManager-wait-online.service
● └─sysinit.target

```

> Проверим успешность перезапуска:


```bash


root@dev1-10:/etc/systemd/system# sctl status prometheus.service 
● prometheus.service - Prometheus-2.33.0.linux-amd64
     Loaded: loaded (/etc/systemd/system/prometheus.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2022-02-03 11:20:41 MSK; 8s ago
   Main PID: 671944 (prometheus)
      Tasks: 13 (limit: 4657)
     Memory: 27.3M
        CPU: 279ms
     CGroup: /system.slice/prometheus.service
             └─671944 /root/prometheus-2.33.0.linux-amd64/prometheus --config.file=/root/prometheus-2.33.0.linux-amd64/prometheus.yml

Feb 03 11:20:42 dev1-10 prometheus[671944]: ts=2022-02-03T08:20:42.154Z caller=head.go:604 level=info component=tsdb msg="WAL segment loaded" segment=1 maxSegment=4Feb 03 11:20:42 dev1-10 prometheus[671944]: ts=2022-02-03T08:20:42.178Z caller=head.go:604 level=info component=tsdb msg="WAL segment loaded" segment=2 maxSegment=4Feb 03 11:20:42 dev1-10 prometheus[671944]: ts=2022-02-03T08:20:42.180Z caller=head.go:604 level=info component=tsdb msg="WAL segment loaded" segment=3 maxSegment=4Feb 03 11:20:42 dev1-10 prometheus[671944]: ts=2022-02-03T08:20:42.180Z caller=head.go:604 level=info component=tsdb msg="WAL segment loaded" segment=4 maxSegment=4Feb 03 11:20:42 dev1-10 prometheus[671944]: ts=2022-02-03T08:20:42.180Z caller=head.go:610 level=info component=tsdb msg="WAL replay completed" checkpoint_replay_d>Feb 03 11:20:42 dev1-10 prometheus[671944]: ts=2022-02-03T08:20:42.183Z caller=main.go:944 level=info fs_type=EXT4_SUPER_MAGIC
Feb 03 11:20:42 dev1-10 prometheus[671944]: ts=2022-02-03T08:20:42.183Z caller=main.go:947 level=info msg="TSDB started"
Feb 03 11:20:42 dev1-10 prometheus[671944]: ts=2022-02-03T08:20:42.183Z caller=main.go:1128 level=info msg="Loading configuration file" filename=/root/prometheus-2>Feb 03 11:20:42 dev1-10 prometheus[671944]: ts=2022-02-03T08:20:42.184Z caller=main.go:1165 level=info msg="Completed loading of configuration file" filename=/root>Feb 03 11:20:42 dev1-10 prometheus[671944]: ts=2022-02-03T08:20:42.184Z caller=main.go:896 level=info msg="Server is ready to receive web requests."
root@dev1-10:/etc/systemd/system# sctl status node_exporter.service
● node_exporter.service - node_exporter-1.3.1.linux-amd64
     Loaded: loaded (/etc/systemd/system/node_exporter.service; enabled; vendor preset: enabled)
    Drop-In: /etc/systemd/system/node_exporter.service.d
             └─override.conf
     Active: active (running) since Thu 2022-02-03 11:20:02 MSK; 53s ago
   Main PID: 671916 (node_exporter)
      Tasks: 6 (limit: 4657)
     Memory: 4.8M
        CPU: 27ms
     CGroup: /system.slice/node_exporter.service
             └─671916 /root/node_exporter-1.3.1.linux-amd64/node_exporter

Feb 03 11:20:02 dev1-10 node_exporter[671916]: ts=2022-02-03T08:20:02.153Z caller=node_exporter.go:115 level=info collector=thermal_zone
Feb 03 11:20:02 dev1-10 node_exporter[671916]: ts=2022-02-03T08:20:02.153Z caller=node_exporter.go:115 level=info collector=time
Feb 03 11:20:02 dev1-10 node_exporter[671916]: ts=2022-02-03T08:20:02.153Z caller=node_exporter.go:115 level=info collector=timex
Feb 03 11:20:02 dev1-10 node_exporter[671916]: ts=2022-02-03T08:20:02.153Z caller=node_exporter.go:115 level=info collector=udp_queues
Feb 03 11:20:02 dev1-10 node_exporter[671916]: ts=2022-02-03T08:20:02.153Z caller=node_exporter.go:115 level=info collector=uname
Feb 03 11:20:02 dev1-10 node_exporter[671916]: ts=2022-02-03T08:20:02.153Z caller=node_exporter.go:115 level=info collector=vmstat
Feb 03 11:20:02 dev1-10 node_exporter[671916]: ts=2022-02-03T08:20:02.153Z caller=node_exporter.go:115 level=info collector=xfs
Feb 03 11:20:02 dev1-10 node_exporter[671916]: ts=2022-02-03T08:20:02.153Z caller=node_exporter.go:115 level=info collector=zfs
Feb 03 11:20:02 dev1-10 node_exporter[671916]: ts=2022-02-03T08:20:02.153Z caller=node_exporter.go:199 level=info msg="Listening on" address=:9100
Feb 03 11:20:02 dev1-10 node_exporter[671916]: ts=2022-02-03T08:20:02.154Z caller=tls_config.go:195 level=info msg="TLS is disabled." http2=false
root@dev1-10:/etc/systemd/system# date
Thu 03 Feb 2022 11:21:06 AM MSK
root@dev1-10:/etc/systemd/system# 


```


> Теперь добьемся, чтобы сервис Prometheus прочитал Environment, который создадим с помощью systemd edit prometheus.service. Удобно, т.к. за анс откроют эдитор, закоментят написанное в соотв. юнит файле и предложат указать имя для сохранения в только что специально созданную дерикторию (по названиию сервиса). Сохраним туда так называемый drop-in дополнение следующего содержания:


```bash
root@dev1-10:/etc/systemd/system# systemctl show prometheus.service | grep Envi
Environment=PROMETHEUS_CFG_OPTS=/root/prometheus-2.33.0.linux-amd64/prometheus.yml
root@dev1-10:/etc/systemd/system# vim ./prometheus.service
root@dev1-10:/etc/systemd/system# 
root@dev1-10:/etc/systemd/system# 
root@dev1-10:/etc/systemd/system# systemctl daemon-reload 
root@dev1-10:/etc/systemd/system# systemctl restart prometheus.service 
root@dev1-10:/etc/systemd/system# systemctl status prometheus.service 
● prometheus.service - Prometheus-2.33.0.linux-amd64
     Loaded: loaded (/etc/systemd/system/prometheus.service; enabled; vendor preset: enabled)
    Drop-In: /etc/systemd/system/prometheus.service.d
             └─myenv.conf
     Active: active (running) since Mon 2022-02-07 12:02:49 MSK; 3s ago
   Main PID: 885335 (prometheus)
      Tasks: 13 (limit: 4657)
     Memory: 31.7M
        CPU: 586ms
     CGroup: /system.slice/prometheus.service
             └─885335 /root/prometheus-2.33.0.linux-amd64/prometheus --config.file=/root/prometheus-2.33.0.linux-amd64/prometheus.yml

Feb 07 12:02:50 dev1-10 prometheus[885335]: ts=2022-02-07T09:02:50.095Z caller=head.go:604 level=info component=tsdb msg="WAL segment loaded" segment=55 maxSegment>Feb 07 12:02:50 dev1-10 prometheus[885335]: ts=2022-02-07T09:02:50.125Z caller=head.go:604 level=info component=tsdb msg="WAL segment loaded" segment=56 maxSegment>Feb 07 12:02:50 dev1-10 prometheus[885335]: ts=2022-02-07T09:02:50.126Z caller=head.go:604 level=info component=tsdb msg="WAL segment loaded" segment=57 maxSegment>Feb 07 12:02:50 dev1-10 prometheus[885335]: ts=2022-02-07T09:02:50.126Z caller=head.go:604 level=info component=tsdb msg="WAL segment loaded" segment=58 maxSegment>Feb 07 12:02:50 dev1-10 prometheus[885335]: ts=2022-02-07T09:02:50.127Z caller=head.go:610 level=info component=tsdb msg="WAL replay completed" checkpoint_replay_d>Feb 07 12:02:50 dev1-10 prometheus[885335]: ts=2022-02-07T09:02:50.129Z caller=main.go:944 level=info fs_type=EXT4_SUPER_MAGIC
Feb 07 12:02:50 dev1-10 prometheus[885335]: ts=2022-02-07T09:02:50.129Z caller=main.go:947 level=info msg="TSDB started"
Feb 07 12:02:50 dev1-10 prometheus[885335]: ts=2022-02-07T09:02:50.129Z caller=main.go:1128 level=info msg="Loading configuration file" filename=/root/prometheus-2>Feb 07 12:02:50 dev1-10 prometheus[885335]: ts=2022-02-07T09:02:50.158Z caller=main.go:1165 level=info msg="Completed loading of configuration file" filename=/root>Feb 07 12:02:50 dev1-10 prometheus[885335]: ts=2022-02-07T09:02:50.158Z caller=main.go:896 level=info msg="Server is ready to receive web requests."

root@dev1-10:/etc/systemd/system# systemctl show prometheus.service | grep Envi
Environment=PROMETHEUS_CFG_OPTS=/root/prometheus-2.33.0.linux-amd64/prometheus.yml
root@dev1-10:/etc/systemd/system# cat ./prometheus.service.d/myenv.conf 
### Editing /etc/systemd/system/prometheus.service.d/override.conf
### Anything between here and the comment below will become the new contents of the file


[Service]
Environment="PROMETHEUS_CFG_OPTS=/root/prometheus-2.33.0.linux-amd64/prometheus.yml"

### Lines below this comment will be discarded

### /etc/systemd/system/prometheus.service
# [Unit]
# Description=Prometheus-2.33.0.linux-amd64
# After=network-online.target mysqld.service apache2.service memcached.service node_exporter.service
# Requires=network-online.target mysqld.service apache2.service memcached.service node_exporter.service
# 
# 
# [Install]
# WantedBy=multi-user.target
# 
# 
# [Service]
# ExecStart=/root/prometheus-2.33.0.linux-amd64/prometheus --config.file=${PROMETHEUS_CFG_OPTS}
root@dev1-10:/etc/systemd/system# 




```





> И наконец попробуем заставить прочитать переменную PROMETHEUS_CFG_OPTS из раздела [Service] файла EnvironmentFile находящегося в /etc/default/prometheus:


```bash

root@dev1-10:/etc/systemd/system# sctl status prometheus.service
● prometheus.service - Prometheus-2.33.0.linux-amd64
     Loaded: loaded (/etc/systemd/system/prometheus.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2022-02-09 16:56:10 MSK; 5s ago
   Main PID: 1354395 (prometheus)
      Tasks: 13 (limit: 4657)
     Memory: 32.7M
        CPU: 548ms
     CGroup: /system.slice/prometheus.service
             └─1354395 /root/prometheus-2.33.0.linux-amd64/prometheus --config.file=/root/prometheus-2.33.0.linux-amd64/prometheus.yml

Feb 09 16:56:11 dev1-10 prometheus[1354395]: ts=2022-02-09T13:56:11.629Z caller=head.go:604 level=info component=tsdb msg="WAL segment loaded" segment=80 maxSegmen>Feb 09 16:56:11 dev1-10 prometheus[1354395]: ts=2022-02-09T13:56:11.664Z caller=head.go:604 level=info component=tsdb msg="WAL segment loaded" segment=81 maxSegmen>Feb 09 16:56:11 dev1-10 prometheus[1354395]: ts=2022-02-09T13:56:11.693Z caller=head.go:604 level=info component=tsdb msg="WAL segment loaded" segment=82 maxSegmen>Feb 09 16:56:11 dev1-10 prometheus[1354395]: ts=2022-02-09T13:56:11.694Z caller=head.go:604 level=info component=tsdb msg="WAL segment loaded" segment=83 maxSegmen>Feb 09 16:56:11 dev1-10 prometheus[1354395]: ts=2022-02-09T13:56:11.694Z caller=head.go:610 level=info component=tsdb msg="WAL replay completed" checkpoint_replay_>Feb 09 16:56:11 dev1-10 prometheus[1354395]: ts=2022-02-09T13:56:11.697Z caller=main.go:944 level=info fs_type=EXT4_SUPER_MAGIC
Feb 09 16:56:11 dev1-10 prometheus[1354395]: ts=2022-02-09T13:56:11.697Z caller=main.go:947 level=info msg="TSDB started"
Feb 09 16:56:11 dev1-10 prometheus[1354395]: ts=2022-02-09T13:56:11.698Z caller=main.go:1128 level=info msg="Loading configuration file" filename=/root/prometheus->Feb 09 16:56:11 dev1-10 prometheus[1354395]: ts=2022-02-09T13:56:11.705Z caller=main.go:1165 level=info msg="Completed loading of configuration file" filename=/roo>Feb 09 16:56:11 dev1-10 prometheus[1354395]: ts=2022-02-09T13:56:11.705Z caller=main.go:896 level=info msg="Server is ready to receive web requests."
root@dev1-10:/etc/systemd/system# vim prometheus.service 

root@dev1-10:/etc/systemd/system# cat /etc/default/prometheus 
PROMETHEUS_CFG_OPTS="/root/prometheus-2.33.0.linux-amd64/prometheus.yml"

root@dev1-10:/etc/systemd/system# cat prometheus.service 
[Unit]
Description=Prometheus-2.33.0.linux-amd64
After=network-online.target mysqld.service apache2.service memcached.service node_exporter.service
Requires=network-online.target mysqld.service apache2.service memcached.service node_exporter.service


[Install]
WantedBy=multi-user.target


[Service]
ExecStart=/root/prometheus-2.33.0.linux-amd64/prometheus --config.file=${PROMETHEUS_CFG_OPTS}
EnvironmentFile=/etc/default/prometheus
root@dev1-10:/etc/systemd/system# 


```



2. Ознакомьтесь с опциями node_exporter и выводом `/metrics` по-умолчанию. Приведите несколько опций, которые вы бы выбрали для базового мониторинга хоста по CPU, памяти, диску и сети.




>Я бы выбрал: ` node_cpu_seconds_total{mode="idle"} ` для CPU, ` node_disk_io_time_weighted_seconds_total ` для Диска, ` {__name__=~"node_memory_Mem.+"} ` для памяти и ` {__name__=~"node_network_transmit.+"}  ` для сети - все как запросы в поиске Prometheus, образуется такая вот ссылка- которую удобно доставать с пом. curl:


```bash


http://192.168.1.117:9090/graph?g0.expr=rate(node_cpu_seconds_total%7Bmode%3D%22idle%22%7D%5B5m%5D)&g0.tab=0&g0.stacked=0&g0.show_exemplars=0&g0.range_input=1d&g1.expr=rate(node_disk_io_time_weighted_seconds_total%5B5m%5D)&g1.tab=0&g1.stacked=0&g1.show_exemplars=0&g1.range_input=1d&g2.expr=%7B__name__%3D~%22node_memory_Mem.%2B%22%7D&g2.tab=0&g2.stacked=0&g2.show_exemplars=0&g2.range_input=1d&g3.expr=%7B__name__%3D~%22node_network_(.%2B)_(packets%7Cerrs)_total%22%7D&g3.tab=0&g3.stacked=0&g3.show_exemplars=0&g3.range_input=1d


```


> Соответственно:


```bash
rate(node_cpu_seconds_total{mode="idle"}[5m])
```

```bash
rate(node_disk_io_time_weighted_seconds_total[5m])
```

```bash
{__name__=~"node_memory_Mem.+"}
```
```bash
{__name__=~"node_network_(.+)_(packets|errs)_total"}
```




3. Установите в свою виртуальную машину [Netdata](https://github.com/netdata/netdata). Воспользуйтесь [готовыми пакетами](https://packagecloud.io/netdata/netdata/install) для установки (`sudo apt install -y netdata`). После успешной установки:
    * в конфигурационном файле `/etc/netdata/netdata.conf` в секции [web] замените значение с localhost на `bind to = 0.0.0.0`,
    * добавьте в Vagrantfile проброс порта Netdata на свой локальный компьютер и сделайте `vagrant reload`:

    ```bash
    config.vm.network "forwarded_port", guest: 19999, host: 19999
    ```

    После успешной перезагрузки в браузере *на своем ПК* (не в виртуальной машине) вы должны суметь зайти на `localhost:19999`. Ознакомьтесь с метриками, которые по умолчанию собираются Netdata и с комментариями, которые даны к этим метрикам.


> Установил. Пробросил. Метрики следующие:





```bash

Disk Current I/O Operations (disk_qops.dev1__10__vg_root)

Systemd Services Swap Memory Used (services.swap_usage)

Systemd Services Used Memory (services.mem_usage)

Systemd Services CPU utilization (100% = 1 core) (services.cpu)

Detailed Response Codes  (web_log_apache_vhosts.detailed_response_codes)

Requests Per HTTP Version (web_log_apache_vhosts.http_version)

NetData API Points (netdata.db_points)

NetData API Queries (netdata.queries)

User Groups Pipes (groups.pipes)

User Groups Open Sockets (groups.sockets)

User Groups Open Files (groups.files)

User Groups I/O Logical Writes (groups.lwrites)

User Groups Disk Logical Reads (groups.lreads)

User Groups Disk Writes (groups.pwrites)

User Groups Disk Reads (groups.preads)

User Groups Minor Page Faults (groups.minor_faults)

User Groups Major Page Faults (swap read) (groups.major_faults)

User Groups Swap Memory (groups.swap)

User Groups CPU System Time (100% = 1 core) (groups.cpu_system)

User Groups CPU User Time (100% = 1 core) (groups.cpu_user)

User Groups Maximum Uptime (groups.uptime_max)

User Groups Average Uptime (groups.uptime_avg)

User Groups Minimum Uptime (groups.uptime_min)

User Groups Carried Over Uptime (groups.uptime)

User Groups Processes (groups.processes)

User Groups Threads (groups.threads)

User Groups Virtual Memory Size (groups.vmem)

User Groups Real Memory (w/o shared) (groups.mem)

User Groups CPU Time (100% = 1 core) (groups.cpu)

Users Pipes (users.pipes)

Users Open Sockets (users.sockets)

Users Open Files (users.files)

Users I/O Logical Writes (users.lwrites)

Users Disk Logical Reads (users.lreads)

Users Disk Writes (users.pwrites)

Users Disk Reads (users.preads)

Users Minor Page Faults (users.minor_faults)

Users Major Page Faults (swap read) (users.major_faults)

Users Swap Memory (users.swap)

Users CPU System Time (100% = 1 core) (users.cpu_system)

Users CPU User Time (100% = 1 core) (users.cpu_user)

Rate (memcached_local.touch_rate)

Requests (memcached_local.touch)

Requests (memcached_local.decrement)

Requests (memcached_local.increment)

Requests (memcached_local.delete)

Requests (memcached_local.cas)

Rate (memcached_local.set_rate)

Rate (memcached_local.get_rate)

Requests (memcached_local.get)

Items (memcached_local.evicted_reclaimed)

Items (memcached_local.items)

Connections (memcached_local.connections)

Squid Server Requests (squid_local.servers_requests)

Network (memcached_local.net)

Squid Server Bandwidth (squid_local.servers_net)

Precision (ntpd_local.sys_precision)

Squid Client Requests (squid_local.clients_requests)

Squid Client Bandwidth (squid_local.clients_net)

Cache Size (memcached_local.cache)

Time constant and poll exponent (3-17) (ntpd_local.sys_tc)

Stratum (1-15) (ntpd_local.sys_stratum)

Total root dispersion to the primary reference clock (ntpd_local.sys_rootdisp)

Total roundtrip delay to the primary reference clock (ntpd_local.sys_rootdelay)

Clock frequency wander (ntpd_local.sys_wander)

Frequency offset relative to hardware clock (ntpd_local.sys_frequency)

Combined system jitter and clock jitter (ntpd_local.sys_jitter)

Combined offset of server relative to this host (ntpd_local.sys_offset)

All Time Unique Client IPs (web_log_apache_vhosts.clients_all)

Current Poll Unique Client IPs (web_log_apache_vhosts.clients)

Requests Per IP Protocol (web_log_apache_vhosts.requests_per_ipproto)

Requests Per HTTP Method (web_log_apache_vhosts.http_method)

Bandwidth (web_log_apache_vhosts.bandwidth)

Response Codes (web_log_apache_vhosts.response_codes)

Response Statuses (web_log_apache_vhosts.response_statuses)

Users Maximum Uptime (users.uptime_max)

Users Average Uptime (users.uptime_avg)

Users Minimum Uptime (users.uptime_min)

Users Carried Over Uptime (users.uptime)

Average Service Time (disk_svctm.dev1__10__vg_home)

Average Completed I/O Operation Bandwidth (disk_avgsz.dev1__10__vg_home)

Average Completed I/O Operation Time (disk_await.dev1__10__vg_home)

Average Service Time (disk_svctm.dev1__10__vg_tmp)

Average Completed I/O Operation Bandwidth (disk_avgsz.dev1__10__vg_tmp)

Average Completed I/O Operation Time (disk_await.dev1__10__vg_tmp)

Average Service Time (disk_svctm.dev1__10__vg_swap_1)

Average Completed I/O Operation Bandwidth (disk_avgsz.dev1__10__vg_swap_1)

Average Completed I/O Operation Time (disk_await.dev1__10__vg_swap_1)

Average Service Time (disk_svctm.dev1__10__vg_var)

Average Completed I/O Operation Bandwidth (disk_avgsz.dev1__10__vg_var)

Average Completed I/O Operation Time (disk_await.dev1__10__vg_var)

Average Service Time (disk_svctm.dev1__10__vg_root)

Average Completed I/O Operation Bandwidth (disk_avgsz.dev1__10__vg_root)

Average Completed I/O Operation Time (disk_await.dev1__10__vg_root)

Average Service Time (disk_svctm.sr0)

Average Completed I/O Operation Bandwidth (disk_avgsz.sr0)

Average Completed I/O Operation Time (disk_await.sr0)

Average Service Time (disk_svctm.sda)

Average Completed I/O Operation Bandwidth (disk_avgsz.sda)

Average Completed I/O Operation Time (disk_await.sda)

All Time Unique Client IPs (web_log_apache.clients_all)

Current Poll Unique Client IPs (web_log_apache.clients)

Requests Per IP Protocol (web_log_apache.requests_per_ipproto)

Requests Per HTTP Method (web_log_apache.http_method)

Bandwidth (web_log_apache.bandwidth)

Response Codes (web_log_apache.response_codes)

Response Statuses (web_log_apache.response_statuses)

Users Processes (users.processes)

Users Threads (users.threads)

Users Virtual Memory Size (users.vmem)

Users Real Memory (w/o shared) (users.mem)

Users CPU Time (100% = 1 core) (users.cpu)

Apps Pipes (apps.pipes)

Apps Open Sockets (apps.sockets)

Apps Open Files (apps.files)

Execution time for web_log_apache_vhosts (netdata.runtime_web_log_apache_vhosts)

Execution time for web_log_apache (netdata.runtime_web_log_apache)

Execution time for squid_local (netdata.runtime_squid_local)

Execution time for ntpd_local (netdata.runtime_ntpd_local)

Apps I/O Logical Writes (apps.lwrites)

Apps Disk Logical Reads (apps.lreads)

Apps Disk Writes (apps.pwrites)

Apps Disk Reads (apps.preads)

Apps Minor Page Faults (apps.minor_faults)

Apps Major Page Faults (swap read) (apps.major_faults)

Apps Swap Memory (apps.swap)

Apps CPU System Time (100% = 1 core) (apps.cpu_system)

Apps CPU User Time (100% = 1 core) (apps.cpu_user)

Apps Maximum Uptime (apps.uptime_max)

Apps Average Uptime (apps.uptime_avg)

Apps Minimum Uptime (apps.uptime_min)

Execution time for memcached_local (netdata.runtime_memcached_local)

NetData DB engine RAM usage (netdata.dbengine_ram)

NetData DB engine File Descriptors (netdata.dbengine_global_file_descriptors)

NetData DB engine errors (netdata.dbengine_global_errors)

NetData DB engine I/O operations (netdata.dbengine_io_operations)

NetData DB engine I/O throughput (netdata.dbengine_io_throughput)

NetData dbengine long-term page statistics (netdata.dbengine_long_term_page_stats)

Apps Carried Over Uptime (apps.uptime)

NetData dbengine page cache statistics (netdata.page_cache_stats)

NetData DB engine page cache hit ratio (netdata.page_cache_hit_ratio)

NetData DB engine data extents' compression savings ratio (netdata.dbengine_compression_ratio)

NetData API Responses Compression Savings Ratio (netdata.compression_ratio)

NetData API Response Time (netdata.response_time)

NetData Network Traffic (netdata.net)

NetData Web Requests (netdata.requests)

NetData Web Clients (netdata.clients)

NetData CPU usage (netdata.server_cpu)

NetData Proc Plugin CPU usage (netdata.plugin_proc_cpu)

NetData Proc Plugin Modules Durations (netdata.plugin_proc_modules)

IPC Shared Memory Used Bytes (system.shared_memory_bytes)

IPC Shared Memory Number of Segments (system.shared_memory_segments)

IPC Semaphore Arrays (system.ipc_semaphore_arrays)

IPC Semaphores (system.ipc_semaphores)

Disk I/O (system.io)

Disk Total I/O Time (disk_iotime.dev1__10__vg_home)

Disk Utilization Time (disk_util.dev1__10__vg_home)

Disk Backlog (disk_backlog.dev1__10__vg_home)

Disk Completed I/O Operations (disk_ops.dev1__10__vg_home)

Disk I/O Bandwidth (disk.dev1__10__vg_home)

Disk Total I/O Time (disk_iotime.dev1__10__vg_tmp)

Disk Utilization Time (disk_util.dev1__10__vg_tmp)

Disk Backlog (disk_backlog.dev1__10__vg_tmp)

Disk Completed I/O Operations (disk_ops.dev1__10__vg_tmp)

Disk I/O Bandwidth (disk.dev1__10__vg_tmp)

Disk Total I/O Time (disk_iotime.dev1__10__vg_swap_1)

Disk Utilization Time (disk_util.dev1__10__vg_swap_1)

Disk Backlog (disk_backlog.dev1__10__vg_swap_1)

Disk Completed I/O Operations (disk_ops.dev1__10__vg_swap_1)

Disk I/O Bandwidth (disk.dev1__10__vg_swap_1)

Disk Total I/O Time (disk_iotime.dev1__10__vg_var)

Disk Utilization Time (disk_util.dev1__10__vg_var)

Disk Backlog (disk_backlog.dev1__10__vg_var)

Disk Current I/O Operations (disk_qops.dev1__10__vg_var)

Disk Completed I/O Operations (disk_ops.dev1__10__vg_var)

Disk I/O Bandwidth (disk.dev1__10__vg_var)

Disk Total I/O Time (disk_iotime.dev1__10__vg_root)

Disk Utilization Time (disk_util.dev1__10__vg_root)

Disk Backlog (disk_backlog.dev1__10__vg_root)

Disk Completed I/O Operations (disk_ops.dev1__10__vg_root)

Disk I/O Bandwidth (disk.dev1__10__vg_root)

Disk Total I/O Time (disk_iotime.sr0)

Disk Utilization Time (disk_util.sr0)

Disk Backlog (disk_backlog.sr0)

Disk Completed I/O Operations (disk_ops.sr0)

Disk I/O Bandwidth (disk.sr0)

Disk Total I/O Time (disk_iotime.sda)

Disk Merged Operations (disk_mops.sda)

Disk Utilization Time (disk_util.sda)

Disk Backlog (disk_backlog.sda)

Disk Completed I/O Operations (disk_ops.sda)

Disk I/O Bandwidth (disk.sda)

CPU7 softnet_stat (cpu.cpu7_softnet_stat)

CPU6 softnet_stat (cpu.cpu6_softnet_stat)

CPU5 softnet_stat (cpu.cpu5_softnet_stat)

CPU4 softnet_stat (cpu.cpu4_softnet_stat)

CPU3 softnet_stat (cpu.cpu3_softnet_stat)

CPU2 softnet_stat (cpu.cpu2_softnet_stat)

CPU1 softnet_stat (cpu.cpu1_softnet_stat)

CPU0 softnet_stat (cpu.cpu0_softnet_stat)

System softnet_stat (system.softnet_stat)

IPv6 ECT Packets (ipv6.ect)

IPv6 ICMP Types (ipv6.icmptypes)

IPv6 ICMP MLDv2 Reports (ipv6.icmpmldv2)

IPv6 Neighbor Messages (ipv6.icmpneighbor)

IPv6 Router Messages (ipv6.icmprouter)

IPv6 ICMP Echo (ipv6.icmpechos)

IPv6 ICMP Errors (ipv6.icmperrors)

IPv6 ICMP Messages (ipv6.icmp)

IPv6 Multicast Packets (ipv6.mcastpkts)

IPv6 Multicast Bandwidth (ipv6.mcast)

IPv6 UDP Errors (ipv6.udperrors)

IPv6 UDP Packets (ipv6.udppackets)

IPv6 Packets (ipv6.packets)

IPv6 Bandwidth (system.ipv6)

IPv4 UDP Errors (ipv4.udperrors)

IPv4 UDP Packets (ipv4.udppackets)

IPv4 TCP Handshake Issues (ipv4.tcphandshake)

IPv4 TCP Opens (ipv4.tcpopens)

IPv4 TCP Errors (ipv4.tcperrors)

IPv4 TCP Packets (ipv4.tcppackets)

IPv4 TCP Connections (ipv4.tcpsock)

IPv4 ICMP Messages (ipv4.icmpmsg)

IPv4 ICMP Errors (ipv4.icmp_errors)

IPv4 ICMP Packets (ipv4.icmp)

IPv4 Errors (ipv4.errors)

IPv4 Packets (ipv4.packets)

IP ECN Statistics (ip.ecnpkts)

IP Broadcast Packets (ip.bcastpkts)

IP Multicast Packets (ip.mcastpkts)

IP Broadcast Bandwidth (ip.bcast)

IP Multicast Bandwidth (ip.mcast)

IP Bandwidth (system.ip)

TCP Out-Of-Order Queue (ip.tcpofo)

TCP Reordered Packets by Detection Method (ip.tcpreorders)

TCP Connection Aborts (ip.tcpconnaborts)

IPv6 RAW Sockets (ipv6.sockstat6_raw_sockets)

IPv6 UDP Sockets (ipv6.sockstat6_udp_sockets)

IPv6 TCP Sockets (ipv6.sockstat6_tcp_sockets)

IPv4 RAW Sockets (ipv4.sockstat_raw_sockets)

IPv4 UDP Sockets Memory (ipv4.sockstat_udp_mem)

IPv4 UDP Sockets (ipv4.sockstat_udp_sockets)

IPv4 TCP Sockets Memory (ipv4.sockstat_tcp_mem)

IPv4 TCP Sockets (ipv4.sockstat_tcp_sockets)

IPv4 Sockets Used (ipv4.sockstat_sockets)

Physical Network Interfaces Aggregated Bandwidth (system.net)

Interface Drops (net_drops.ens18)

Packets (net_packets.ens18)

Bandwidth (net.ens18)

Transparent HugePages Memory (mem.transparent_hugepages)

Reclaimable Kernel Memory (mem.slab)

Memory Used by Kernel (mem.kernel)

Writeback Memory (mem.writeback)

Committed (Allocated) Memory (mem.committed)

System Swap (system.swap)

Available RAM for applications (mem.available)

System RAM (system.ram)

Memory Page Faults (mem.pgfaults)

Memory Paged from/to disk (system.pgpgio)

Swap I/O (system.swapio)

CPU7 softirqs (cpu.cpu7_softirqs)

CPU6 softirqs (cpu.cpu6_softirqs)

CPU5 softirqs (cpu.cpu5_softirqs)

CPU4 softirqs (cpu.cpu4_softirqs)

CPU3 softirqs (cpu.cpu3_softirqs)

CPU2 softirqs (cpu.cpu2_softirqs)

CPU1 softirqs (cpu.cpu1_softirqs)

CPU0 softirqs (cpu.cpu0_softirqs)

System softirqs (system.softirqs)

CPU7 Interrupts (cpu.cpu7_interrupts)

CPU6 Interrupts (cpu.cpu6_interrupts)

CPU5 Interrupts (cpu.cpu5_interrupts)

CPU4 Interrupts (cpu.cpu4_interrupts)

CPU3 Interrupts (cpu.cpu3_interrupts)

CPU2 Interrupts (cpu.cpu2_interrupts)

CPU1 Interrupts (cpu.cpu1_interrupts)

CPU0 Interrupts (cpu.cpu0_interrupts)

System interrupts (system.interrupts)

I/O Full Pressure (system.io_full_pressure)

I/O Pressure (system.io_some_pressure)

Memory Full Pressure (system.memory_full_pressure)

Memory Pressure (system.memory_some_pressure)

CPU Pressure (system.cpu_pressure)

Available Entropy (system.entropy)

System Active Processes (system.active_processes)

System Load Average (system.load)

System Uptime (system.uptime)

C-state residency time (cpu.cpu7_cpuidle)

C-state residency time (cpu.cpu6_cpuidle)

C-state residency time (cpu.cpu5_cpuidle)

C-state residency time (cpu.cpu4_cpuidle)

C-state residency time (cpu.cpu3_cpuidle)

C-state residency time (cpu.cpu2_cpuidle)

C-state residency time (cpu.cpu1_cpuidle)

C-state residency time (cpu.cpu0_cpuidle)

System Processes (system.processes)

Started Processes (system.forks)

CPU Context Switches (system.ctxt)

CPU Interrupts (system.intr)

Core utilization (cpu.cpu7)

Core utilization (cpu.cpu6)

Core utilization (cpu.cpu5)

Core utilization (cpu.cpu4)

Core utilization (cpu.cpu3)

Apps Processes (apps.processes)

Core utilization (cpu.cpu2)

Core utilization (cpu.cpu1)

NetData Disk Space Plugin Duration (netdata.plugin_diskspace_dt)

NetData Disk Space Plugin CPU usage (netdata.plugin_diskspace)

Disk Files (inodes) Usage for /var [/dev/mapper/dev1--10--vg-var] (disk_inodes._var)

Disk Space Usage for /var [/dev/mapper/dev1--10--vg-var] (disk_space._var)

Disk Files (inodes) Usage for /tmp [/dev/mapper/dev1--10--vg-tmp] (disk_inodes._tmp)

Disk Space Usage for /tmp [/dev/mapper/dev1--10--vg-tmp] (disk_space._tmp)

Disk Files (inodes) Usage for /home [/dev/mapper/dev1--10--vg-home] (disk_inodes._home)

Disk Space Usage for /home [/dev/mapper/dev1--10--vg-home] (disk_space._home)

Disk Files (inodes) Usage for /boot [/dev/sda1] (disk_inodes._boot)

Disk Space Usage for /boot [/dev/sda1] (disk_space._boot)

Disk Files (inodes) Usage for /run/lock [tmpfs] (disk_inodes._run_lock)

Disk Space Usage for /run/lock [tmpfs] (disk_space._run_lock)

Disk Files (inodes) Usage for /dev/shm [tmpfs] (disk_inodes._dev_shm)

Disk Space Usage for /dev/shm [tmpfs] (disk_space._dev_shm)

Connection Tracker Expectations (netfilter.netlink_expect)

Connection Tracker Errors (netfilter.netlink_errors)

Connection Tracker Searches (netfilter.netlink_search)

NetData statsd collector thread No 1 CPU usage (netdata.plugin_statsd_collector1_cpu)

NetData statsd charting thread CPU usage (netdata.plugin_statsd_charting_cpu)

Private metric charts created by the netdata statsd server (netdata.private_charts)

statsd server TCP connected sockets (netdata.tcp_connected)

statsd server TCP connects and disconnects (netdata.tcp_connects)

Network packets processed by the netdata statsd server (netdata.statsd_packets)

Bytes read by the netdata statsd server (netdata.statsd_bytes)

Read operations made by the netdata statsd server (netdata.statsd_reads)

Apps Threads (apps.threads)

Events processed by the netdata statsd server (netdata.statsd_events)

Useful metrics in the netdata statsd database (netdata.statsd_useful_metrics)

NetData TC script execution (netdata.plugin_tc_time)

Core utilization (cpu.cpu0)

NetData CGroups Plugin CPU usage (netdata.plugin_cgroups_cpu)

NetData web server thread No 1 CPU usage (netdata.web_thread1_cpu)

NetData web server thread No 5 CPU usage (netdata.web_thread5_cpu)

NetData web server thread No 3 CPU usage (netdata.web_thread3_cpu)

NetData web server thread No 4 CPU usage (netdata.web_thread4_cpu)

NetData web server thread No 6 CPU usage (netdata.web_thread6_cpu)

NetData web server thread No 2 CPU usage (netdata.web_thread2_cpu)

Disk Files (inodes) Usage for / [/dev/mapper/dev1--10--vg-root] (disk_inodes._)

Disk Space Usage for / [/dev/mapper/dev1--10--vg-root] (disk_space._)

Disk Files (inodes) Usage for /run [tmpfs] (disk_inodes._run)

Disk Space Usage for /run [tmpfs] (disk_space._run)

Disk Files (inodes) Usage for /dev [udev] (disk_inodes._dev)

Connection Tracker Changes (netfilter.netlink_changes)

Apps Virtual Memory Size (apps.vmem)

Apps Real Memory (w/o shared) (apps.mem)

Apps CPU Time (100% = 1 core) (apps.cpu)

Apps Plugin Exited Children Normalization Ratios (netdata.apps_children_fix)

Apps Plugin Normalization Ratios (netdata.apps_fix)

Apps Plugin Files (netdata.apps_sizes)

Apps Plugin CPU (netdata.apps_cpu)

Total CPU utilization (system.cpu)

Connection Tracker New Connections (netfilter.netlink_new)

Disk Space Usage for /dev [udev] (disk_space._dev)

NetData TC CPU usage (netdata.plugin_tc_cpu)

Metrics in the netdata statsd database (netdata.statsd_metrics)

CPU Idle Jitter (system.idlejitter)


```
> Интересно что снапшот, который делает netdata читаем, распарсив его regexp'ом увидел, что в мониторинге 372 метрики прив. выше.
> Поиск ` ("title":")(.?)(")   ` и замена на ` \r\n$2\r  `. Далее замена ненужного на пустые строки.


4. Можно ли по выводу `dmesg` понять, осознает ли ОС, что загружена не на настоящем оборудовании, а на системе виртуализации?

```bash

root@dev1-10:~# dmesg -THk | grep virt
[  +0.000002] Booting paravirtualized kernel on KVM
[  +0.012310] virtio_net virtio2 ens18: renamed from eth0
root@dev1-10:~# dmesg -TH | grep virt
[  +0.000002] Booting paravirtualized kernel on KVM
[  +0.012310] virtio_net virtio2 ens18: renamed from eth0
[  +0.000152] systemd[1]: Detected virtualization kvm.
root@dev1-10:~# dmesg -THk | grep virt
[  +0.000002] Booting paravirtualized kernel on KVM
[  +0.012310] virtio_net virtio2 ens18: renamed from eth0
root@dev1-10:~# dmesg -THkS | grep virt
[  +0.000002] Booting paravirtualized kernel on KVM
[  +0.012310] virtio_net virtio2 ens18: renamed from eth0
root@dev1-10:~# dmesg -TH | grep virt
[  +0.000002] Booting paravirtualized kernel on KVM
[  +0.012310] virtio_net virtio2 ens18: renamed from eth0
[  +0.000152] systemd[1]: Detected virtualization kvm.
root@dev1-10:~# dmesg -TH | grep VM
[  +0.000000] Hypervisor detected: KVM
[  +0.000008] ACPI: SSDT 0x00000000BFFE1624 0000CA (v01 BOCHS  VMGENID  00000001 BXPC 00000001)
[  +0.000002] Booting paravirtualized kernel on KVM
[  +0.109898] smpboot: CPU0: Intel Common KVM processor (family: 0xf, model: 0x6, stepping: 0x1)
[  +0.004044] input: VirtualPS/2 VMware VMMouse as /devices/platform/i8042/serio1/input/input4
[  +0.002154] input: VirtualPS/2 VMware VMMouse as /devices/platform/i8042/serio1/input/input3
[  +0.000269] systemd[1]: Listening on LVM2 poll daemon socket.
root@dev1-10:~# dmesg -THS | grep VM
[  +0.000000] Hypervisor detected: KVM
[  +0.000008] ACPI: SSDT 0x00000000BFFE1624 0000CA (v01 BOCHS  VMGENID  00000001 BXPC 00000001)
[  +0.000002] Booting paravirtualized kernel on KVM
[  +0.109898] smpboot: CPU0: Intel Common KVM processor (family: 0xf, model: 0x6, stepping: 0x1)
[  +0.004044] input: VirtualPS/2 VMware VMMouse as /devices/platform/i8042/serio1/input/input4
[  +0.002154] input: VirtualPS/2 VMware VMMouse as /devices/platform/i8042/serio1/input/input3
[  +0.000269] systemd[1]: Listening on LVM2 poll daemon socket.
root@dev1-10:~# 

```

> Возможно, эти строки и в особенности:

```bash

root@dev1-10:~# dmesg -TH | grep VM
[  +0.000000] Hypervisor detected: KVM
[  +0.000008] ACPI: SSDT 0x00000000BFFE1624 0000CA (v01 BOCHS  VMGENID  00000001 BXPC 00000001)
[  +0.000002] Booting paravirtualized kernel on KVM

```


5. Как настроен sysctl `fs.nr_open` на системе по-умолчанию? Узнайте, что означает этот параметр. Какой другой существующий лимит не позволит достичь такого числа (`ulimit --help`)?

```bash


root@dev1-10:~# 
root@dev1-10:~# sysctl -a | grep fs.nr_open
fs.nr_open = 1048576
root@dev1-10:~# sysctl -a -r fs.nr_open
fs.nr_open = 1048576


root@dev1-10:~# find /proc/ -name nr_open -type f 
/proc/sys/fs/nr_open
root@dev1-10:~# cat /proc/sys/fs/nr_open
1048576
root@dev1-10:~# 



```

> fs.open_nr - ограничение на кол-во открытых дескрипторов области настройки глобальных и специфичных tunables ядра.


```bash

root@dev1-10:~# ulimit --help | grep 'descriptor'
      -n        the maximum number of open file descriptors
root@dev1-10:~# 
```








6. Запустите любой долгоживущий процесс (не `ls`, который отработает мгновенно, а, например, `sleep 1h`) в отдельном неймспейсе процессов; покажите, что ваш процесс работает под PID 1 через `nsenter`. Для простоты работайте в данном задании под root (`sudo -i`). Под обычным пользователем требуются дополнительные опции (`--map-root-user`) и т.д.



```bash
CONTAINER ID   IMAGE     COMMAND   CREATED          STATUS          PORTS     NAMES
e69d98b8b400   ubuntu    "bash"    59 minutes ago   Up 13 minutes             docker0-dev1-10
root@dev1-10:~# docker inspect --format '{{.State.Pid}}' docker0-dev1-10 
742335
root@dev1-10:~# ps aux | grep 742335
root      742335  0.0  0.0   4248  3452 pts/0    Ss   12:54   0:00 bash
root      743608  0.0  0.0   6184   664 pts/2    R+   13:08   0:00 grep 742335
root@dev1-10:~# nsenter -t 742335 -p -r ps -ef
UID          PID    PPID  C STIME TTY          TIME CMD
root           1       0  0 09:54 pts/0    00:00:00 bash
root          23       1  0 09:57 pts/0    00:00:00 /bin/bash ./test
root         740      23  0 10:09 pts/0    00:00:00 sleep 1
root         741       0  0 10:09 ?        00:00:00 ps -ef
root@dev1-10:~# nsenter -t 742335 -a
root@e69d98b8b400:/# ps -ef
UID          PID    PPID  C STIME TTY          TIME CMD
root           1       0  0 09:54 pts/0    00:00:00 bash
root          23       1  0 09:57 pts/0    00:00:00 /bin/bash ./test
root         823       0  0 10:10 ?        00:00:00 -bash
root         838      23  0 10:10 pts/0    00:00:00 sleep 1
root         839     823  0 10:10 ?        00:00:00 ps -ef
root@e69d98b8b400:/# 


```



7. Найдите информацию о том, что такое `:(){ :|:& };:`. Запустите эту команду в своей виртуальной машине Vagrant с Ubuntu 20.04 (**это важно, поведение в других ОС не проверялось**). Некоторое время все будет "плохо", после чего (минуты) – ОС должна стабилизироваться. Вызов `dmesg` расскажет, какой механизм помог автоматической стабилизации. Как настроен этот механизм по-умолчанию, и как изменить число процессов, которое можно создать в сессии?


> Запустил в контейнере. Действительно стало плохо:

```bash

root@e69d98b8b400:~/sbin/admin# :(){ :|:& };:
[1] 942
root@e69d98b8b400:~/sbin/admin# ps bash: fork: retry: Resource temporarily unavailable
bash: fork: retry: Resource temporarily unavailable
bash: fork: retry: Resource temporarily unavailable
bash: fork: retry: Resource temporarily unavailable
bash: fork: retry: Resource temporarily unavailable
bash: fork: retry: Resource temporarily unavailable
bash: fork: retry: Resource temporarily unavailable
bash: fork: retry: Resource temporarily unavailable
bash: fork: retry: Resource temporarily unavailable
bash: fork: Resource temporarily unavailable
bash: fork: Resource temporarily unavailable


```
> Попробовал найти причину:




```bash

root@dev1-10:~# dmesg -T -l crit,err,warn | grep "Feb  5 13:"
[Sat Feb  5 13:17:57 2022] INFO: task C2 CompilerThre:623711 blocked for more than 120 seconds.
[Sat Feb  5 13:17:57 2022]       Not tainted 5.10.0-9-amd64 #1 Debian 5.10.70-1
[Sat Feb  5 13:17:57 2022] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
[Sat Feb  5 13:17:57 2022] INFO: task C1 CompilerThre:623712 blocked for more than 120 seconds.
[Sat Feb  5 13:17:57 2022]       Not tainted 5.10.0-9-amd64 #1 Debian 5.10.70-1
[Sat Feb  5 13:17:57 2022] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
[Sat Feb  5 13:17:57 2022] INFO: task VM Periodic Tas:623715 blocked for more than 120 seconds.
[Sat Feb  5 13:17:57 2022]       Not tainted 5.10.0-9-amd64 #1 Debian 5.10.70-1
[Sat Feb  5 13:17:57 2022] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
[Sat Feb  5 13:17:57 2022] INFO: task Timer-0:623727 blocked for more than 120 seconds.
[Sat Feb  5 13:17:57 2022]       Not tainted 5.10.0-9-amd64 #1 Debian 5.10.70-1
[Sat Feb  5 13:17:57 2022] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
[Sat Feb  5 13:17:57 2022] INFO: task Periodic tasks :623747 blocked for more than 120 seconds.
[Sat Feb  5 13:17:57 2022]       Not tainted 5.10.0-9-amd64 #1 Debian 5.10.70-1
[Sat Feb  5 13:17:57 2022] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
[Sat Feb  5 13:17:57 2022] INFO: task TimerQueue:623771 blocked for more than 120 seconds.
[Sat Feb  5 13:17:57 2022]       Not tainted 5.10.0-9-amd64 #1 Debian 5.10.70-1
[Sat Feb  5 13:17:57 2022] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
[Sat Feb  5 13:17:57 2022] INFO: task ThreadPoolForeg:623900 blocked for more than 120 seconds.
[Sat Feb  5 13:17:57 2022]       Not tainted 5.10.0-9-amd64 #1 Debian 5.10.70-1
[Sat Feb  5 13:17:57 2022] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
[Sat Feb  5 13:17:57 2022] INFO: task Flushing Daemon:738529 blocked for more than 120 seconds.
[Sat Feb  5 13:17:57 2022]       Not tainted 5.10.0-9-amd64 #1 Debian 5.10.70-1
[Sat Feb  5 13:17:57 2022] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
[Sat Feb  5 13:17:57 2022] INFO: task Index Healthche:743946 blocked for more than 120 seconds.
[Sat Feb  5 13:17:57 2022]       Not tainted 5.10.0-9-amd64 #1 Debian 5.10.70-1
[Sat Feb  5 13:17:57 2022] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
[Sat Feb  5 13:17:57 2022] INFO: task ApplicationImpl:752924 blocked for more than 120 seconds.
[Sat Feb  5 13:17:57 2022]       Not tainted 5.10.0-9-amd64 #1 Debian 5.10.70-1
[Sat Feb  5 13:17:57 2022] "echo 0 > /proc/sys/kernel/hung_task_timeout_secs" disables this message.
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

Любые вопросы по решению задач задавайте в чате Slack.

---
