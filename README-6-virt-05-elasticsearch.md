# Домашнее задание к занятию "6.5. Elasticsearch"

## Задача 1

В этом задании вы потренируетесь в:
- установке elasticsearch
- первоначальном конфигурировании elastcisearch
- запуске elasticsearch в docker

Используя докер образ [centos:7](https://hub.docker.com/_/centos) как базовый и 
[документацию по установке и запуску Elastcisearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html):

- составьте Dockerfile-манифест для elasticsearch
- соберите docker-образ и сделайте `push` в ваш docker.io репозиторий

[https://hub.docker.com/layers/246655966/demiof/my_es_test_cluster/8.3.1/images/sha256-81025e1548da9371086969f96dfe27b140f46af879c0f1171713ae2b63505710?context=repo](https://hub.docker.com/layers/246655966/demiof/my_es_test_cluster/8.3.1/images/sha256-81025e1548da9371086969f96dfe27b140f46af879c0f1171713ae2b63505710?context=repo)

- запустите контейнер из получившегося образа и выполните запрос пути `/` c хост-машины

Требования к `elasticsearch.yml`:
- данные `path` должны сохраняться в `/var/lib`
- имя ноды должно быть `netology_test`

В ответе приведите:
- текст Dockerfile манифеста

```bash

ARG version=8.3.1
FROM centos:latest
#elasticsearch USER & GROUP
ENV USER=elasticsearch
ENV USER_pass=test_pass 
ENV UID=1000    
ENV GROUP=elasticsearch
ENV GID=1000
#elasticsearch
ENV ELASTICSEARCH_VERSION 8.2.3

ENV PID=/var/run/elasticsearch
ENV PID_FILE=elasticsearch.pid

ENV ES_HOME=/usr/share/elasticsearch
ENV ES_HOME_BIN=/usr/share/elasticsearch/bin/
ENV ES_DATA_LOGS=/var/lib/elasticsearch
ENV ES_DATA=/var/lib/elasticsearch/data
ENV ES_LOGS=/var/lib/elasticsearch/logs
ENV ES_VARLOG=/var/log/elasticsearch
ENV ES_SYSCONFIG=/etc/sysconfig/elasticsearch
ENV ES_ETC=/etc/elasticsearch
ENV ES_EXEC_FILE=/usr/share/elasticsearch/bin/elasticsearch

ENV PATH ${ES_HOME}/:$PATH

ENV GOSU_VERSION 1.14

LABEL creator="demi"

#preparing os

RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-* && \
    sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-* && \
    rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-centosofficial && \
    yum update -y && yum install net-tools vim wget -y && \
    wget -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-amd64" && \
    wget -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-amd64.asc" && \
    export GNUPGHOME="$(mktemp -d)" && \
    gpg --keyserver hkps://keys.openpgp.org --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4 && \
    gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu && \
    rm -rf "$GNUPGHOME" /usr/local/bin/gosu.asc && \
    chmod +x /usr/local/bin/gosu && \
    gosu nobody true && \
    rm -rf /var/lib/apt/lists/*

#install elasticsearch
RUN mkdir ${ES_HOME} && mkdir /tmp/elasticsearch/
WORKDIR /tmp/elasticsearch
ADD https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.3.1-linux-x86_64.tar.gz ./elasticsearch.tar.gz 
RUN tar -zxf ./elasticsearch.tar.gz --strip-components=1 && cp -r ./ ${ES_HOME}/


WORKDIR ${ES_HOME}
RUN sed -i -e 's/ES_DISTRIBUTION_TYPE=tar/ES_DISTRIBUTION_TYPE=docker/' bin/elasticsearch-env && \
    mkdir data && mkdir ${ES_DATA_LOGS} && \
    find . -type d -exec chmod 0555 {} + && \
    find . -type f -exec chmod 0444 {} + && \
    chmod 0555 bin/* jdk/bin/* jdk/lib/jspawnhelper modules/x-pack-ml/platform/linux-*/bin/* && \
    chmod 0775 bin config config/jvm.options.d data logs plugins && \
    find config -type f -exec chmod 0664 {} + && \
    groupadd -g ${GID} ${GROUP} && useradd -u ${UID} -g ${GROUP} -s /bin/sh -m ${USER}

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
COPY elasticsearch.yml ${ES_HOME}/config/elasticsearch.yml

RUN chmod g=u /etc/passwd && \
    chmod 0555 /usr/local/bin/entrypoint.sh && \
    find / -xdev -perm -4000 -exec chmod ug-s {} + && \
    chmod 0775 /usr/share/elasticsearch ${ES_DATA_LOGS} && \
    chown elasticsearch bin config config/jvm.options.d data logs plugins ${ES_DATA_LOGS}

RUN set -Eeuo pipefail && trust extract \
    --overwrite \
    --format=java-cacerts \
    --filter=ca-anchors \
    --purpose=server-auth \
    ${ES_HOME}/jdk/lib/security/cacerts

# expose the default Elasticsearch port
EXPOSE 9200:9300

# entrypoint for elasticsearch

ENTRYPOINT ["gosu", "elasticsearch:root", "/usr/local/bin/entrypoint.sh"]

CMD ["elasticsearch"]

```

> entrypoint.sh

```bash

#!/bin/bash
set -e

# Files created by Elasticsearch should always be group writable too
umask 0002

# Allow user specify custom CMD, maybe bin/elasticsearch itself
# for example to directly specify `-E` style parameters for elasticsearch on k8s
# or simply to run /bin/bash to check the image
if [[ "$1" == "eswrapper" || $(basename "$1") == "elasticsearch" ]]; then
  # Rewrite CMD args to remove the explicit command,
  # so that we are backwards compatible with the docs
  # from the previous Elasticsearch versions < 6
  # and configuration option:
  # https://www.elastic.co/guide/en/elasticsearch/reference/5.6/docker.html#_d_override_the_image_8217_s_default_ulink_url_https_docs_docker_com_engine_reference_run_cmd_default_command_or_options_cmd_ulink
  # Without this, user could specify `elasticsearch -E x.y=z` but
  # `bin/elasticsearch -E x.y=z` would not work. In any case,
  # we want to continue through this script, and not exec early.
  set -- "${@:2}"
else
  # Run whatever command the user wanted
  exec "$@"
fi

# Allow environment variables to be set by creating a file with the
# contents, and setting an environment variable with the suffix _FILE to
# point to it. This can be used to provide secrets to a container, without
# the values being specified explicitly when running the container.
#
# This is also sourced in elasticsearch-env, and is only needed here
# as well because we use ELASTIC_PASSWORD below. Sourcing this script
# is idempotent.
source /usr/share/elasticsearch/bin/elasticsearch-env-from-file

if [[ -f bin/elasticsearch-users ]]; then
  # Check for the ELASTIC_PASSWORD environment variable to set the
  # bootstrap password for Security.
  #
  # This is only required for the first node in a cluster with Security
  # enabled, but we have no way of knowing which node we are yet. We'll just
  # honor the variable if it's present.
  if [[ -n "$ELASTIC_PASSWORD" ]]; then
    [[ -f /usr/share/elasticsearch/config/elasticsearch.keystore ]] || (elasticsearch-keystore create)
    if ! (elasticsearch-keystore has-passwd --silent) ; then
      # keystore is unencrypted
      if ! (elasticsearch-keystore list | grep -q '^bootstrap.password$'); then
        (echo "$ELASTIC_PASSWORD" | elasticsearch-keystore add -x 'bootstrap.password')
      fi
    else
      # keystore requires password
      if ! (echo "$KEYSTORE_PASSWORD" \
          | elasticsearch-keystore list | grep -q '^bootstrap.password$') ; then
        COMMANDS="$(printf "%s\n%s" "$KEYSTORE_PASSWORD" "$ELASTIC_PASSWORD")"
        (echo "$COMMANDS" | elasticsearch-keystore add -x 'bootstrap.password')
      fi
    fi
  fi
fi

if [[ -n "$ES_LOG_STYLE" ]]; then
  case "$ES_LOG_STYLE" in
    console)
      # This is the default. Nothing to do.
      ;;
    file)
      # Overwrite the default config with the stack config. Do this as a
      # copy, not a move, in case the container is restarted.
      cp -f /usr/share/elasticsearch/config/log4j2.file.properties /usr/share/elasticsearch/config/log4j2.properties
      ;;
    *)
      echo "ERROR: ES_LOG_STYLE set to [$ES_LOG_STYLE]. Expected [console] or [file]" >&2
      exit 1 ;;
  esac
fi

if [[ -n "$ENROLLMENT_TOKEN" ]]; then
  POSITIONAL_PARAMETERS="--enrollment-token $ENROLLMENT_TOKEN"
else
  POSITIONAL_PARAMETERS=""
fi

# Signal forwarding and child reaping is handled by `tini`, which is the
# actual entrypoint of the container
exec /usr/share/elasticsearch/bin/elasticsearch $POSITIONAL_PARAMETERS <<<"$KEYSTORE_PASSWORD"

```

Подсказки:
- возможно вам понадобится установка пакета perl-Digest-SHA для корректной работы пакета shasum
- при сетевых проблемах внимательно изучите кластерные и сетевые настройки в elasticsearch.yml
- при некоторых проблемах вам поможет docker директива ulimit
- elasticsearch в логах обычно описывает проблему и пути ее решения

Далее мы будем работать с данным экземпляром elasticsearch.

## Задача 2

В этом задании вы научитесь:
- создавать и удалять индексы
- изучать состояние кластера
- обосновывать причину деградации доступности данных

Ознакомтесь с [документацией](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html) 
и добавьте в `elasticsearch` 3 индекса, в соответствии со таблицей:

| Имя | Количество реплик | Количество шард |
|-----|-------------------|-----------------|
| ind-1| 0 | 1 |
| ind-2 | 1 | 2 |
| ind-3 | 2 | 4 |

```bash


[root@8d8c5fc77975 elasticsearch]# curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:AoJIhJCiVA_2hKtM=yj2 -X PUT "https://localhost:9200/ind-1?pretty" -H 'Content-Type: application/json' -d'
{
"settings" : {
"index" : {
"number_of_replicas" : 0,
"number_of_shards": 1
}
}
}'
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "ind-1"
}
[root@8d8c5fc77975 elasticsearch]# curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:AoJIhJCiVA_2hKtM=yj2 -X PUT "https://localhost:9200/ind-2?pretty" -H 'Content-Type: application/json' -d'
{
"settings" : {
"index" : {
"number_of_replicas" : 1,
"number_of_shards": 2
}
}
}'
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "ind-2"
}
[root@8d8c5fc77975 elasticsearch]# curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:AoJIhJCiVA_2hKtM=yj2 -X PUT "https://localhost:9200/ind-3?pretty" -H 'Content-Type: application/json' -d'
{
"settings" : {
"index" : {
"number_of_replicas" : 2,
"number_of_shards": 4 
}
}
}'
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "ind-3"
}
[root@8d8c5fc77975 elasticsearch]# 


```


Получите список индексов и их статусов, используя API и **приведите в ответе** на задание.

```bash

[root@8d8c5fc77975 elasticsearch]# curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:AoJIhJCiVA_2hKtM=yj2 -X GET "https://localhost:9200/*?pretty"
{
  "ind-1" : {
    "aliases" : { },
    "mappings" : { },
    "settings" : {
      "index" : {
        "routing" : {
          "allocation" : {
            "include" : {
              "_tier_preference" : "data_content"
            }
          }
        },
        "number_of_shards" : "1",
        "provided_name" : "ind-1",
        "creation_date" : "1656323540458",
        "number_of_replicas" : "0",
        "uuid" : "uCqxiJPsRB2Yu0SO09vS4g",
        "version" : {
          "created" : "8020399"
        }
      }
    }
  },
  "ind-2" : {
    "aliases" : { },
    "mappings" : { },
    "settings" : {
      "index" : {
        "routing" : {
          "allocation" : {
            "include" : {
              "_tier_preference" : "data_content"
            }
          }
        },
        "number_of_shards" : "2",
        "provided_name" : "ind-2",
        "creation_date" : "1656323578271",
        "number_of_replicas" : "1",
        "uuid" : "0Uda7SF5TZ-FbvxKDa0D_Q",
        "version" : {
          "created" : "8020399"
        }
      }
    }
  },
  "ind-3" : {
    "aliases" : { },
    "mappings" : { },
    "settings" : {
      "index" : {
        "routing" : {
          "allocation" : {
            "include" : {
              "_tier_preference" : "data_content"
            }
          }
        },
        "number_of_shards" : "4",
        "provided_name" : "ind-3",
        "creation_date" : "1656323594281",
        "number_of_replicas" : "2",
        "uuid" : "ms9km0kwRyS6di9nyF3YWg",
        "version" : {
          "created" : "8020399"
        }
      }
    }
  }
}
[root@8d8c5fc77975 elasticsearch]# 

```



Получите состояние кластера `elasticsearch`, используя API.

```bash
[root@8d8c5fc77975 elasticsearch]# curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:AoJIhJCiVA_2hKtM=yj2 -X GET "https://localhost:9200/_cluster/health/?pretty"
{
  "cluster_name" : "my-es-test-cluster",
  "status" : "yellow",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 9,
  "active_shards" : 9,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 10,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 47.368421052631575
}
[root@8d8c5fc77975 elasticsearch]# 

```

Как вы думаете, почему часть индексов и кластер находится в состоянии yellow?

> Потому что кластер из 1 узла не отказоусточив, рекомендуется не менее 3-х узлов с точки зрения кворума и отказоустойчивости.

Удалите все индексы.


```bash

[root@8d8c5fc77975 elasticsearch]# echo 'action.destructive_requires_name: false'  >> /etc/elasticsearch/elasticsearch.yml

[root@8d8c5fc77975 elasticsearch]# ps aux | grep elasticsearch
elastic+     330  2.0 42.2 8024460 1698252 pts/1 Sl   08:27   2:20 /usr/share/elasticsearch/jdk/bin/java -Xshare:auto -Des.networkaddress.cache.ttl=60 -Des.networkaddress.cache.negative.ttl=10 -Djava.security.manager=allow -XX:+AlwaysPreTouch -Xss1m -Djava.awt.headless=true -Dfile.encoding=UTF-8 -Djna.nosys=true -XX:-OmitStackTraceInFastThrow -XX:+ShowCodeDetailsInExceptionMessages -Dio.netty.noUnsafe=true -Dio.netty.noKeySetOptimization=true -Dio.netty.recycler.maxCapacityPerThread=0 -Dlog4j.shutdownHookEnabled=false -Dlog4j2.disable.jmx=true -Dlog4j2.formatMsgNoLookups=true -Djava.locale.providers=SPI,COMPAT --add-opens=java.base/java.io=ALL-UNNAMED -XX:+UseG1GC -Djava.io.tmpdir=/tmp/elasticsearch-7048102489720961423 -XX:+HeapDumpOnOutOfMemoryError -XX:+ExitOnOutOfMemoryError -XX:HeapDumpPath=/var/lib/elasticsearch -XX:ErrorFile=/var/log/elasticsearch/hs_err_pid%p.log -Xlog:gc*,gc+age=trace,safepoint:file=/var/log/elasticsearch/gc.log:utctime,pid,tags:filecount=32,filesize=64m -Xms1964m -Xmx1964m -XX:MaxDirectMemorySize=1029701632 -XX:G1HeapRegionSize=4m -XX:InitiatingHeapOccupancyPercent=30 -XX:G1ReservePercent=15 -Des.path.home=/usr/share/elasticsearch -Des.path.conf=/etc/elasticsearch -Des.distribution.flavor=default -Des.distribution.type=rpm -Des.bundled_jdk=true -cp /usr/share/elasticsearch/lib/* org.elasticsearch.bootstrap.Elasticsearch -d
elastic+     362  0.0  0.0 120608  1692 pts/1    Sl   08:27   0:00 /usr/share/elasticsearch/modules/x-pack-ml/platform/linux-x86_64/bin/controller
root         667  0.0  0.0  12136  1000 pts/1    S+   10:18   0:00 grep --color=auto elasticsearch
[root@8d8c5fc77975 elasticsearch]# kill -9 330 362
[root@8d8c5fc77975 elasticsearch]# /entrypoint.sh elasticsearch
parameter set & runuser=0
[root@8d8c5fc77975 elasticsearch]# curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:AoJIhJCiVA_2hKtM=yj2 -X GET "https://localhost:9200/*"
{}[root@8d8c5fc77975 elasticsearch]# 

```

**Важно**

При проектировании кластера elasticsearch нужно корректно рассчитывать количество реплик и шард,
иначе возможна потеря данных индексов, вплоть до полной, при деградации системы.

## Задача 3

В данном задании вы научитесь:
- создавать бэкапы данных
- восстанавливать индексы из бэкапов

Создайте директорию `{путь до корневой директории с elasticsearch в образе}/snapshots`.

Используя API [зарегистрируйте](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-register-repository.html#snapshots-register-repository) 
данную директорию как `snapshot repository` c именем `netology_backup`.

**Приведите в ответе** запрос API и результат вызова API для создания репозитория.

```bash

[root@8d8c5fc77975 elasticsearch]# curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:AoJIhJCiVA_2hKtM=yj2 -X PUT "https://localhost:9200/_snapshot/my_repo" -H 'Content-Type: application/json' -d'
> {
> "type" : "fs",
> "settings" : {
> "location" : "/usr/share/elasticsearch/snapshots"
> }
> }'
{"acknowledged":true}[root@8d8c5fc77975 elasticsearch]# 

[root@8d8c5fc7curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:AoJIhJCiVA_2hKtM=yj2 -X GET "https://localhost:9200/_snapshot/*"
{"my_repo":{"type":"fs","settings":{"location":"/usr/share/elasticsearch/snapshots"}}}
[root@8d8c5fc77975 elasticsearch]#

```

Создайте индекс `test` с 0 реплик и 1 шардом и **приведите в ответе** список индексов.


```bash

[root@8d8c5fc77975 elasticsearch]# curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:AoJIhJCiVA_2hKtM=yj2 -X GET "https://localhost:9200/*?pretty"
{
  "test" : {
    "aliases" : { },
    "mappings" : { },
    "settings" : {
      "index" : {
        "routing" : {
          "allocation" : {
            "include" : {
              "_tier_preference" : "data_content"
            }
          }
        },
        "number_of_shards" : "1",
        "provided_name" : "test",
        "creation_date" : "1656328564753",
        "number_of_replicas" : "0",
        "uuid" : "e0FxBt8tQC-sLUnRFZS5QQ",
        "version" : {
          "created" : "8020399"
        }
      }
    }
  }
}
[root@8d8c5fc77975 elasticsearch]# 

```

[Создайте `snapshot`](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-take-snapshot.html) 
состояния кластера `elasticsearch`.

```bash

[root@8d8c5fc77975 snapshots]# curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:AoJIhJCiVA_2hKtM=yj2 -X PUT "https://localhost:9200/_slm/policy/test-snapshots" -H 'Content-Type: application/json' -d'
{
  "schedule": "0 5 * * * ?",       
  "name": "<test-every-5-min-snap-{now/d}>", 
  "repository": "my_repo",    
  "config": {
    "indices": "*",                 
    "include_global_state": true    
  },
  "retention": {                    
    "expire_after": "1h",
    "min_count": 5,
    "max_count": 50
  } 
}'
{"acknowledged":true}

[root@8d8c5fc77975 snapshots]# curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:AoJIhJCiVA_2hKtM=yj2 -X POST "https://localhost:9200/_slm/policy/test-snapshots/_execute?pretty"
{
  "snapshot_name" : "test-every-5-min-snap-2022.06.27-hdi_ngdtqgsithzbcsacga"
}
[root@8d8c5fc77975 snapshots]# 

[root@8d8c5fc77975 snapshots]# ls -la
total 48
drwxrwxr-x 3 elasticsearch elasticsearch  4096 Jun 27 11:37 .
drwxr-xr-x 1 elasticsearch elasticsearch  4096 Jun 27 10:28 ..
-rw-rw-r-- 1 elasticsearch elasticsearch  1154 Jun 27 11:37 index-0
-rw-rw-r-- 1 elasticsearch elasticsearch     8 Jun 27 11:37 index.latest
drwxrwxr-x 5 elasticsearch elasticsearch  4096 Jun 27 11:37 indices
-rw-rw-r-- 1 elasticsearch elasticsearch 18627 Jun 27 11:37 meta-6j8RrnKpQi-9_hmdoaklmQ.dat
-rw-rw-r-- 1 elasticsearch elasticsearch   445 Jun 27 11:37 snap-6j8RrnKpQi-9_hmdoaklmQ.dat
[root@8d8c5fc77975 snapshots]# 


```

**Приведите в ответе** список файлов в директории со `snapshot`ами.

Удалите индекс `test` и создайте индекс `test-2`. **Приведите в ответе** список индексов.

```bash

[root@8d8c5fc77975 snapshots]# curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:AoJIhJCiVA_2hKtM=yj2 -X DELETE "https://localhost:9200/test?pretty"
{
  "acknowledged" : true
}
[root@8d8c5fc77975 snapshots]# 

[root@8d8c5fc77975 snapshots]# curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:AoJIhJCiVA_2hKtM=yj2 -X PUT "https://localhost:9200/test-2?pretty"
{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "test-2"
}
[root@8d8c5fc77975 snapshots]# curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:AoJIhJCiVA_2hKtM=yj2 -X GET "https://localhost:9200/*?pretty"
{
  "test-2" : {
    "aliases" : { },
    "mappings" : { },
    "settings" : {
      "index" : {
        "routing" : {
          "allocation" : {
            "include" : {
              "_tier_preference" : "data_content"
            }
          }
        },
        "number_of_shards" : "1",
        "provided_name" : "test-2",
        "creation_date" : "1656330145039",
        "number_of_replicas" : "1",
        "uuid" : "J4VJu3s7T9qckkVHK0MDJA",
        "version" : {
          "created" : "8020399"
        }
      }
    }
  }
}
[root@8d8c5fc77975 snapshots]# 


[root@8d8c5fc77975 snapshots]# curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:AoJIhJCiVA_2hKtM=yj2 -X GET "https://localhost:9200/_snapshot/my_repo/*?verbose=false"
{"snapshots":[{"snapshot":"test-every-5-min-snap-2022.06.27-hdi_ngdtqgsithzbcsacga","uuid":"6j8RrnKpQi-9_hmdoaklmQ","repository":"my_repo","indices":[".geoip_databases",".security-7","test"],"data_streams":[],"state":"SUCCESS"}],"total":1,"remaining":0}


```


[Восстановите](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-restore-snapshot.html) состояние
кластера `elasticsearch` из `snapshot`, созданного ранее. 

```bash

[root@8d8c5fc77975 snapshots]# curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:AoJIhJCiVA_2hKtM=yj2 -X POST "https://localhost:9200/_snapshot/my_repo/test-every-5-min-snap-2022.06.27-hdi_ngdtqgsithzbcsacga/_restore"
{"accepted":true}
[root@8d8c5fc77975 snapshots]#
```
**Приведите в ответе** запрос к API восстановления и итоговый список индексов.


```bash

[root@8d8c5fc77975 snapshots]# curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:AoJIhJCiVA_2hKtM=yj2 -X GET "https://localhost:9200/*?pretty"
{
  "test" : {
    "aliases" : { },
    "mappings" : { },
    "settings" : {
      "index" : {
        "routing" : {
          "allocation" : {
            "include" : {
              "_tier_preference" : "data_content"
            }
          }
        },
        "number_of_shards" : "1",
        "provided_name" : "test",
        "creation_date" : "1656328564753",
        "number_of_replicas" : "0",
        "uuid" : "uE0JXfv7RFGo3XjubhR7qg",
        "version" : {
          "created" : "8020399"
        }
      }
    }
  },
  "test-2" : {
    "aliases" : { },
    "mappings" : { },
    "settings" : {
      "index" : {
        "routing" : {
          "allocation" : {
            "include" : {
              "_tier_preference" : "data_content"
            }
          }
        },
        "number_of_shards" : "1",
        "provided_name" : "test-2",
        "creation_date" : "1656330145039",
        "number_of_replicas" : "1",
        "uuid" : "J4VJu3s7T9qckkVHK0MDJA",
        "version" : {
          "created" : "8020399"
        }
      }
    }
  }
}
[root@8d8c5fc77975 snapshots]# 


```




Подсказки:
- возможно вам понадобится доработать `elasticsearch.yml` в части директивы `path.repo` и перезапустить `elasticsearch`

---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
