# Домашнее задание к занятию "08.01 Введение в Ansible"

## Подготовка к выполнению
1. Установите ansible версии 2.10 или выше.
2. Создайте свой собственный публичный репозиторий на github с произвольным именем.
3. Скачайте [playbook](./playbook/) из репозитория с домашним заданием и перенесите его в свой репозиторий.

## Основная часть
1. Попробуйте запустить playbook на окружении из `test.yml`, зафиксируйте какое значение имеет факт 
`some_fact` для указанного хоста при выполнении playbook'a.

```bash

TASK [Print fact] **************************************************************************************************************
ok: [localhost] => {
    "msg": 12
}

```


2. Найдите файл с переменными (group_vars) в котором задаётся найденное в первом пункте значение и поменяйте его на 'all default fact'.

```bash
root@dev1-10:~/ansible-test/playbook# cat group_vars/all/examp.yml 
---
  some_fact: 12root@dev1-10:~/ansible-test/playbook# sed -e 's/12/all default fact/g' group_vars/all/examp.yml 
---
  some_fact: all default factroot@dev1
```

3. Воспользуйтесь подготовленным (используется `docker`) или создайте собственное окружение для проведения дальнейших испытаний.
4. Проведите запуск playbook на окружении из `prod.yml`. Зафиксируйте полученные значения `some_fact` для каждого из `managed host`.

```bash
TASK [Print OS] ****************************************************************************************************************
task path: /root/ansible-test/playbook/site.yml:31
redirecting (type: connection) ansible.builtin.docker to community.general.docker
redirecting (type: connection) ansible.builtin.docker to community.general.docker
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}

TASK [Print fact] **************************************************************************************************************
task path: /root/ansible-test/playbook/site.yml:35
redirecting (type: connection) ansible.builtin.docker to community.general.docker
redirecting (type: connection) ansible.builtin.docker to community.general.docker
ok: [centos7] => {
    "msg": "el"
}
ok: [ubuntu] => {
    "msg": "deb"
}
META: ran handlers
META: ran handlers

PLAY RECAP *********************************************************************************************************************
centos7                    : ok=5    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
ubuntu                     : ok=5    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

5. Добавьте факты в `group_vars` каждой из групп хостов так, чтобы для `some_fact` получились следующие значения: для `deb` - 'deb default fact', для `el` - 'el default fact'.

```bash
TASK [Print OS] ****************************************************************************************************************
task path: /root/ansible-test/playbook/site.yml:31
redirecting (type: connection) ansible.builtin.docker to community.general.docker
redirecting (type: connection) ansible.builtin.docker to community.general.docker
ok: [ubuntu] => {
    "msg": "Ubuntu"
}
ok: [centos7] => {
    "msg": "CentOS"
}

TASK [Print fact] **************************************************************************************************************
task path: /root/ansible-test/playbook/site.yml:35
redirecting (type: connection) ansible.builtin.docker to community.general.docker
redirecting (type: connection) ansible.builtin.docker to community.general.docker
ok: [ubuntu] => {
    "msg": "deb default fact"
}
ok: [centos7] => {
    "msg": "el default fact"
}
META: ran handlers
META: ran handlers

PLAY RECAP *********************************************************************************************************************
centos7                    : ok=5    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
ubuntu                     : ok=5    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

6.  Повторите запуск playbook на окружении `prod.yml`. Убедитесь, что выдаются корректные значения для всех хостов.

```bash
root@dev1-10:~/ansible-test/playbook# ansible-playbook -i inventory/prod.yml site.yml

PLAY [Install python and etc on el] ********************************************************************************************

TASK [Packet manager update] ***************************************************************************************************
changed: [centos7]

TASK [Install python and etc on el] ********************************************************************************************
changed: [centos7] => (item=python3-pip)
changed: [centos7] => (item=virtualenv)
changed: [centos7] => (item=python3-setuptools)
changed: [centos7] => (item=ca-certificates)
changed: [centos7] => (item=curl)

PLAY [Install python and etc on deb] *******************************************************************************************

TASK [Packet manager update] ***************************************************************************************************
changed: [ubuntu]

TASK [Install python and etc on deb] *******************************************************************************************
changed: [ubuntu] => (item=python3-pip)
changed: [ubuntu] => (item=virtualenv)
changed: [ubuntu] => (item=python3-setuptools)
changed: [ubuntu] => (item=ca-certificates)
changed: [ubuntu] => (item=curl)

PLAY [Print os facts] **********************************************************************************************************

TASK [Gathering Facts] *********************************************************************************************************
ok: [centos7]
ok: [ubuntu]

TASK [Print OS] ****************************************************************************************************************
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}

TASK [Print fact] **************************************************************************************************************
ok: [centos7] => {
    "msg": "el default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}

PLAY RECAP *********************************************************************************************************************
centos7                    : ok=5    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
ubuntu                     : ok=5    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

root@dev1-10:~/ansible-test/playbook# 

```

7. При помощи `ansible-vault` зашифруйте факты в `group_vars/deb` и `group_vars/el` с паролем `netology`.
8. Запустите playbook на окружении `prod.yml`. При запуске `ansible` должен запросить у вас пароль. Убедитесь в работоспособности.

```bash

root@dev1-10:~/ansible-test/playbook/group_vars# ansible-vault -v encrypt all/examp.yml deb/examp.yml el/examp.yml 
Using /etc/ansible/ansible.cfg as config file
New Vault password: 
Confirm New Vault password: 
Encryption successful
root@dev1-10:~/ansible-test/playbook/group_vars# cd ..

root@dev1-10:~/ansible-test/playbook# ansible-playbook --ask-vault-pass -i inventory/prod.yml site.yml
Vault password: 

PLAY [Install python and etc on el] ********************************************************************************************

TASK [Packet manager update] ***************************************************************************************************
changed: [centos7]

TASK [Install python and etc on el] ********************************************************************************************
changed: [centos7] => (item=python3-pip)
changed: [centos7] => (item=virtualenv)
changed: [centos7] => (item=python3-setuptools)
changed: [centos7] => (item=ca-certificates)
changed: [centos7] => (item=curl)

PLAY [Install python and etc on deb] *******************************************************************************************

TASK [Packet manager update] ***************************************************************************************************
changed: [ubuntu]

TASK [Install python and etc on deb] *******************************************************************************************
changed: [ubuntu] => (item=python3-pip)
changed: [ubuntu] => (item=virtualenv)
changed: [ubuntu] => (item=python3-setuptools)
changed: [ubuntu] => (item=ca-certificates)
changed: [ubuntu] => (item=curl)

PLAY [Print os facts] **********************************************************************************************************

TASK [Gathering Facts] *********************************************************************************************************
ok: [centos7]
ok: [ubuntu]

TASK [Print OS] ****************************************************************************************************************
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}

TASK [Print fact] **************************************************************************************************************
ok: [centos7] => {
    "msg": "el default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}

PLAY RECAP *********************************************************************************************************************
centos7                    : ok=5    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
ubuntu                     : ok=5    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

root@dev1-10:~/ansible-test/playbook# 

```

9. Посмотрите при помощи `ansible-doc` список плагинов для подключения. Выберите подходящий для работы на `control node`.
10. В `prod.yml` добавьте новую группу хостов с именем  `local`, в ней разместите localhost с необходимым типом подключения.
11. Запустите playbook на окружении `prod.yml`. При запуске `ansible` должен запросить у вас пароль. Убедитесь что факты `some_fact` для каждого из хостов определены из верных `group_vars`.

```bash
root@dev1-10:~/ansible-test/playbook# ansible-playbook --ask-vault-pass -i inventory/prod.yml site.yml
Vault password: 

PLAY [Install python and etc on el] ********************************************************************************************

TASK [Packet manager update] ***************************************************************************************************
[WARNING]: Collection community.general does not support Ansible version 2.10.8
changed: [centos7]

TASK [Install python and etc on el] ********************************************************************************************
[WARNING]: Collection community.general does not support Ansible version 2.10.8
changed: [centos7] => (item=python3-pip)
changed: [centos7] => (item=virtualenv)
changed: [centos7] => (item=python3-setuptools)
changed: [centos7] => (item=ca-certificates)
changed: [centos7] => (item=curl)

PLAY [Install python and etc on deb] *******************************************************************************************

TASK [Packet manager update] ***************************************************************************************************
[WARNING]: Collection community.general does not support Ansible version 2.10.8
changed: [ubuntu]

TASK [Install python and etc on deb] *******************************************************************************************
[WARNING]: Collection community.general does not support Ansible version 2.10.8
changed: [ubuntu] => (item=python3-pip)
changed: [ubuntu] => (item=virtualenv)
changed: [ubuntu] => (item=python3-setuptools)
changed: [ubuntu] => (item=ca-certificates)
changed: [ubuntu] => (item=curl)

PLAY [Print os facts] **********************************************************************************************************

TASK [Gathering Facts] *********************************************************************************************************
[WARNING]: Collection community.general does not support Ansible version 2.10.8
[WARNING]: Collection community.general does not support Ansible version 2.10.8
ok: [dev]
ok: [ubuntu]
ok: [centos7]

TASK [Print OS] ****************************************************************************************************************
ok: [dev] => {
    "msg": "Debian"
}
[WARNING]: Collection community.general does not support Ansible version 2.10.8
[WARNING]: Collection community.general does not support Ansible version 2.10.8
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}

TASK [Print fact] **************************************************************************************************************
ok: [dev] => {
    "msg": 12
}
[WARNING]: Collection community.general does not support Ansible version 2.10.8
[WARNING]: Collection community.general does not support Ansible version 2.10.8
ok: [centos7] => {
    "msg": "el default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}

PLAY RECAP *********************************************************************************************************************
centos7                    : ok=5    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
dev                        : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
ubuntu                     : ok=5    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

root@dev1-10:~/ansible-test/playbook# 
```

12. Заполните `README.md` ответами на вопросы. Сделайте `git push` в ветку `master`. В ответе отправьте ссылку на ваш открытый репозиторий с изменённым `playbook` и заполненным `README.md`.

## Необязательная часть

1. При помощи `ansible-vault` расшифруйте все зашифрованные файлы с переменными.

```bash
root@dev1-10:~/ansible-test/playbook# ansible-vault -v decrypt group_vars/all/examp.yml group_vars/deb/examp.yml group_vars/el/examp.yml 
Using /etc/ansible/ansible.cfg as config file
Vault password: 
Decryption successful
root@dev1-10:~/ansible-test/playbook# cat group_vars/all/examp.yml 
---
  

  some_fact: 12root@dev1-10:~/ansible-test/playbook# cat group_vars/deb/examp.yml 
---
  some_fact: "deb default fact"root@dev1-10:~/ansible-test/playbook# cat group_vars/el/examp.yml 
---
  some_fact: "el default fact"root@dev1-10:~/ansible-test/playbook# 
```

2. Зашифруйте отдельное значение `PaSSw0rd` для переменной `some_fact` паролем `netology`. Добавьте полученное значение в `group_vars/all/exmp.yml`.

```bash

root@dev1-10:~/ansible-test/playbook# ansible-vault encrypt_string PaSSw0rd --name pw
New Vault password: 
Confirm New Vault password: 
pw: !vault |
          $ANSIBLE_VAULT;1.1;AES256
          61626432643734303063613665333661616634663232376133663731326636613463363962653461
          6633396361623730626337356464386265636639356239620a633364303865616638353562323631
          66303262356438323539333965613930646139323534343434306361646534383065306231336439
          3463623364336262660a346634333733633766353433336464373034653938393733393635633364
          6637
Encryption successful

```

3. Запустите `playbook`, убедитесь, что для нужных хостов применился новый `fact`.

```bash

root@dev1-10:~/ansible-test/playbook# ansible-playbook --ask-vault-pass -i inventory/prod.yml site.yml
Vault password: 

PLAY [Install python and etc on el] ********************************************************************************************

TASK [Packet manager update] ***************************************************************************************************
[WARNING]: Collection community.general does not support Ansible version 2.10.8
changed: [centos7]

TASK [Install python and etc on el] ********************************************************************************************
[WARNING]: Collection community.general does not support Ansible version 2.10.8
changed: [centos7] => (item=python3-pip)
changed: [centos7] => (item=virtualenv)
changed: [centos7] => (item=python3-setuptools)
changed: [centos7] => (item=ca-certificates)
changed: [centos7] => (item=curl)

PLAY [Install python and etc on deb] *******************************************************************************************

TASK [Packet manager update] ***************************************************************************************************
[WARNING]: Collection community.general does not support Ansible version 2.10.8
changed: [ubuntu]

TASK [Install python and etc on deb] *******************************************************************************************
[WARNING]: Collection community.general does not support Ansible version 2.10.8
changed: [ubuntu] => (item=python3-pip)
changed: [ubuntu] => (item=virtualenv)
changed: [ubuntu] => (item=python3-setuptools)
changed: [ubuntu] => (item=ca-certificates)
changed: [ubuntu] => (item=curl)

PLAY [Print os facts] **********************************************************************************************************

TASK [Gathering Facts] *********************************************************************************************************
[WARNING]: Collection community.general does not support Ansible version 2.10.8
[WARNING]: Collection community.general does not support Ansible version 2.10.8
ok: [dev]
ok: [ubuntu]
ok: [centos7]

TASK [Print OS] ****************************************************************************************************************
ok: [dev] => {
    "msg": "Debian"
}
[WARNING]: Collection community.general does not support Ansible version 2.10.8
[WARNING]: Collection community.general does not support Ansible version 2.10.8
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}

TASK [Print fact] **************************************************************************************************************
ok: [dev] => {
    "msg": 12
}
[WARNING]: Collection community.general does not support Ansible version 2.10.8
[WARNING]: Collection community.general does not support Ansible version 2.10.8
ok: [centos7] => {
    "msg": "el default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}

TASK [Print pw] ****************************************************************************************************************
[WARNING]: Collection community.general does not support Ansible version 2.10.8
ok: [dev] => {
    "msg": "PaSSw0rd"
}
[WARNING]: Collection community.general does not support Ansible version 2.10.8
ok: [centos7] => {
    "msg": "PaSSw0rd"
}
ok: [ubuntu] => {
    "msg": "PaSSw0rd"
}

PLAY RECAP *********************************************************************************************************************
centos7                    : ok=6    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
dev                        : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
ubuntu                     : ok=6    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

root@dev1-10:~/ansible-test/playbook# 

```

4. Добавьте новую группу хостов `fedora`, самостоятельно придумайте для неё переменную. В качестве образа можно использовать [этот](https://hub.docker.com/r/pycontribs/fedora).
5. Напишите скрипт на bash: автоматизируйте поднятие необходимых контейнеров, запуск ansible-playbook и остановку контейнеров.

```bash

root@dev1-10:~/ansible-test/playbook# cat start_fedora.sh 
#!/bin/bash

if [ $# -eq 0 ]
then 
        echo "Please add docker image tag name to run container!"
else
docker run -h fedora --name fedora -d -it $1 /bin/bash
fi
root@dev1-10:~/ansible-test/playbook# 

```

6. Все изменения должны быть зафиксированы и отправлены в вашей личный репозиторий.

```bash

root@dev1-10:~/ansible-test/playbook# ansible-playbook -i inventory/docker.yml site.yml -vvvv
ansible-playbook 2.10.8
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3/dist-packages/ansible
  executable location = /usr/bin/ansible-playbook
  python version = 3.9.2 (default, Feb 28 2021, 17:03:44) [GCC 10.2.1 20210110]
Using /etc/ansible/ansible.cfg as config file
setting up inventory plugins
host_list declined parsing /root/ansible-test/playbook/inventory/docker.yml as it did not pass its verify_file() method
script declined parsing /root/ansible-test/playbook/inventory/docker.yml as it did not pass its verify_file() method
Set default localhost to localhost
Parsed /root/ansible-test/playbook/inventory/docker.yml inventory source with yaml plugin
Loading collection community.docker from /root/.ansible/collections/ansible_collections/community/docker
Loading callback plugin default of type stdout, v2.0 from /usr/lib/python3/dist-packages/ansible/plugins/callback/default.py
Skipping callback 'default', as we already have a stdout callback.
Skipping callback 'minimal', as we already have a stdout callback.
Skipping callback 'oneline', as we already have a stdout callback.

PLAYBOOK: site.yml ************************************************************************************************************
Positional arguments: site.yml
verbosity: 4
connection: smart
timeout: 10
become_method: sudo
tags: ('all',)
inventory: ('/root/ansible-test/playbook/inventory/docker.yml',)
forks: 5
4 plays in site.yml
[WARNING]: Could not match supplied host pattern, ignoring: el

PLAY [Install python and etc on el] *******************************************************************************************
skipping: no hosts matched
[WARNING]: Could not match supplied host pattern, ignoring: deb

PLAY [Install python and etc on deb] ******************************************************************************************
skipping: no hosts matched

PLAY [Pull, create and run fedora containers] *********************************************************************************
META: ran handlers

TASK [Pull an image] **********************************************************************************************************
task path: /root/ansible-test/playbook/site.yml:34
<localhost> ESTABLISH LOCAL CONNECTION FOR USER: root
<localhost> EXEC /bin/sh -c '( umask 77 && mkdir -p "` echo /tmp `"&& mkdir "` echo /tmp/ansible-tmp-1660047602.6767542-236352-3486264608269 `" && echo ansible-tmp-1660047602.6767542-236352-3486264608269="` echo /tmp/ansible-tmp-1660047602.6767542-236352-3486264608269 `" ) && sleep 0'
Using module file /root/.ansible/collections/ansible_collections/community/docker/plugins/modules/docker_image.py
<localhost> PUT /tmp/ansible-local-2363388t42nd9i/tmp2ayy4fzy TO /tmp/ansible-tmp-1660047602.6767542-236352-3486264608269/AnsiballZ_docker_image.py
<localhost> EXEC /bin/sh -c 'chmod u+x /tmp/ansible-tmp-1660047602.6767542-236352-3486264608269/ /tmp/ansible-tmp-1660047602.6767542-236352-3486264608269/AnsiballZ_docker_image.py && sleep 0'
<localhost> EXEC /bin/sh -c '/usr/bin/python3 /tmp/ansible-tmp-1660047602.6767542-236352-3486264608269/AnsiballZ_docker_image.py && sleep 0'
<localhost> EXEC /bin/sh -c 'rm -f -r /tmp/ansible-tmp-1660047602.6767542-236352-3486264608269/ > /dev/null 2>&1 && sleep 0'
ok: [localhost] => {
    "actions": [],
    "changed": false,
    "image": {
        "Architecture": "amd64",
        "Author": "",
        "Comment": "",
        "Config": {
            "AttachStderr": false,
            "AttachStdin": false,
            "AttachStdout": false,
            "Cmd": [
                "/bin/bash"
            ],
            "Domainname": "",
            "Entrypoint": null,
            "Env": [
                "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                "DISTTAG=f33container",
                "FGC=f33",
                "FBR=f33",
                "SHELL=/bin/bash"
            ],
            "Hostname": "",
            "Image": "sha256:9779b73454a85e1b2323b053d717320e60f947b433effa58220cd9caab076d17",
            "Labels": {
                "maintainer": "PyContribs <pycontribs@googlegroups.com>"
            },
            "OnBuild": null,
            "OpenStdin": false,
            "StdinOnce": false,
            "Tty": false,
            "User": "",
            "Volumes": null,
            "WorkingDir": ""
        },
        "Container": "62b77f6a7089f3588a55c3f75ab3c868817e4d0e7e4675311ad5ac55176c17ca",
        "ContainerConfig": {
            "AttachStderr": false,
            "AttachStdin": false,
            "AttachStdout": false,
            "Cmd": [
                "/bin/sh",
                "-c",
                "#(nop) ",
                "ENV SHELL=/bin/bash"
            ],
            "Domainname": "",
            "Entrypoint": null,
            "Env": [
                "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
                "DISTTAG=f33container",
                "FGC=f33",
                "FBR=f33",
                "SHELL=/bin/bash"
            ],
            "Hostname": "62b77f6a7089",
            "Image": "sha256:9779b73454a85e1b2323b053d717320e60f947b433effa58220cd9caab076d17",
            "Labels": {
                "maintainer": "PyContribs <pycontribs@googlegroups.com>"
            },
            "OnBuild": null,
            "OpenStdin": false,
            "StdinOnce": false,
            "Tty": false,
            "User": "",
            "Volumes": null,
            "WorkingDir": ""
        },
        "Created": "2021-04-21T12:59:56.709672062Z",
        "DockerVersion": "20.10.6",
        "GraphDriver": {
            "Data": {
                "LowerDir": "/var/lib/docker/overlay2/f3ab467727827cb2ca1ecfd263fc6c575b4eb3673874ec5026e5e3467fc68379/diff",
                "MergedDir": "/var/lib/docker/overlay2/2b99acbf3caa08dadb3853fdf7416ac60a161fd898873b6d5cd8c29d4f1af71d/merged",
                "UpperDir": "/var/lib/docker/overlay2/2b99acbf3caa08dadb3853fdf7416ac60a161fd898873b6d5cd8c29d4f1af71d/diff",
                "WorkDir": "/var/lib/docker/overlay2/2b99acbf3caa08dadb3853fdf7416ac60a161fd898873b6d5cd8c29d4f1af71d/work"
            },
            "Name": "overlay2"
        },
        "Id": "sha256:c317904963299aca8e51353eb6be1227ca22bb08028e5a20e64e6eb6fe034d33",
        "Metadata": {
            "LastTagTime": "0001-01-01T00:00:00Z"
        },
        "Os": "linux",
        "Parent": "",
        "RepoDigests": [
            "pycontribs/fedora@sha256:20eeb45ef6e394947058dc24dc2bd98dfb7a8fecbbe6363d14ab3170f10a27ab"
        ],
        "RepoTags": [
            "pycontribs/fedora:latest"
        ],
        "RootFS": {
            "Layers": [
                "sha256:6d668c00f3f1bda56574dbf2f0a1d9210d2f3f902d7da7840ba15313347a5760",
                "sha256:5b5c0ea8c17c9051e1d6c824777da735dd0a2902e05421535976e8b40eee6802"
            ],
            "Type": "layers"
        },
        "Size": 585973671,
        "VirtualSize": 585973671
    },
    "invocation": {
        "module_args": {
            "api_version": "auto",
            "archive_path": null,
            "build": null,
            "ca_cert": null,
            "client_cert": null,
            "client_key": null,
            "debug": false,
            "docker_host": "unix://var/run/docker.sock",
            "force_absent": false,
            "force_source": false,
            "force_tag": false,
            "load_path": null,
            "name": "pycontribs/fedora",
            "pull": {
                "platform": "amd64"
            },
            "push": false,
            "repository": null,
            "source": "pull",
            "ssl_version": null,
            "state": "present",
            "tag": "latest",
            "timeout": 60,
            "tls": false,
            "tls_hostname": null,
            "use_ssh_client": false,
            "validate_certs": false
        }
    }
}

TASK [Create & start container] ***********************************************************************************************
task path: /root/ansible-test/playbook/site.yml:41
<localhost> ESTABLISH LOCAL CONNECTION FOR USER: root
<localhost> EXEC /bin/sh -c '( umask 77 && mkdir -p "` echo /tmp `"&& mkdir "` echo /tmp/ansible-tmp-1660047603.838035-236392-28824348140959 `" && echo ansible-tmp-1660047603.838035-236392-28824348140959="` echo /tmp/ansible-tmp-1660047603.838035-236392-28824348140959 `" ) && sleep 0'
Using module file /usr/lib/python3/dist-packages/ansible/modules/command.py
<localhost> PUT /tmp/ansible-local-2363388t42nd9i/tmpde_z916c TO /tmp/ansible-tmp-1660047603.838035-236392-28824348140959/AnsiballZ_command.py
<localhost> EXEC /bin/sh -c 'chmod u+x /tmp/ansible-tmp-1660047603.838035-236392-28824348140959/ /tmp/ansible-tmp-1660047603.838035-236392-28824348140959/AnsiballZ_command.py && sleep 0'
<localhost> EXEC /bin/sh -c '/usr/bin/python3 /tmp/ansible-tmp-1660047603.838035-236392-28824348140959/AnsiballZ_command.py && sleep 0'
<localhost> EXEC /bin/sh -c 'rm -f -r /tmp/ansible-tmp-1660047603.838035-236392-28824348140959/ > /dev/null 2>&1 && sleep 0'
changed: [localhost] => {
    "changed": true,
    "cmd": [
        "./start_fedora.sh",
        "pycontribs/fedora"
    ],
    "delta": "0:00:00.664140",
    "end": "2022-08-09 15:20:04.982892",
    "invocation": {
        "module_args": {
            "_raw_params": "./start_fedora.sh pycontribs/fedora",
            "_uses_shell": false,
            "argv": null,
            "chdir": null,
            "creates": null,
            "executable": null,
            "removes": null,
            "stdin": null,
            "stdin_add_newline": true,
            "strip_empty_ends": true,
            "warn": false
        }
    },
    "rc": 0,
    "start": "2022-08-09 15:20:04.318752",
    "stderr": "",
    "stderr_lines": [],
    "stdout": "b71ffff566e392f47893511a547467378b6793130cde1e9e758cb078817fc1a4",
    "stdout_lines": [
        "b71ffff566e392f47893511a547467378b6793130cde1e9e758cb078817fc1a4"
    ]
}

TASK [print container_id variable] ********************************************************************************************
task path: /root/ansible-test/playbook/site.yml:53
ok: [localhost] => {
    "container_id.stdout": "b71ffff566e392f47893511a547467378b6793130cde1e9e758cb078817fc1a4"
}
META: ran handlers
META: ran handlers

PLAY [Print os facts] *********************************************************************************************************

TASK [Gathering Facts] ********************************************************************************************************
task path: /root/ansible-test/playbook/site.yml:57
<localhost> ESTABLISH LOCAL CONNECTION FOR USER: root
<localhost> EXEC /bin/sh -c '( umask 77 && mkdir -p "` echo /tmp `"&& mkdir "` echo /tmp/ansible-tmp-1660047605.1516645-236509-105742751858134 `" && echo ansible-tmp-1660047605.1516645-236509-105742751858134="` echo /tmp/ansible-tmp-1660047605.1516645-236509-105742751858134 `" ) && sleep 0'
redirecting (type: connection) ansible.builtin.docker to community.general.docker
Loading collection community.general from /root/.ansible/collections/ansible_collections/community/general
[WARNING]: Collection community.general does not support Ansible version 2.10.8
redirecting (type: connection) community.general.docker to community.docker.docker
<fedora> ESTABLISH DOCKER CONNECTION FOR USER: root
<fedora> EXEC ['/usr/bin/docker', b'exec', b'-u', 'root', b'-i', 'fedora', '/bin/sh', '-c', '/bin/sh -c \'( umask 77 && mkdir -p "` echo /tmp `"&& mkdir "` echo /tmp/ansible-tmp-1660047605.2351809-236510-4382298702639 `" && echo ansible-tmp-1660047605.2351809-236510-4382298702639="` echo /tmp/ansible-tmp-1660047605.2351809-236510-4382298702639 `" ) && sleep 0\'']
Using module file /usr/lib/python3/dist-packages/ansible/modules/setup.py
<localhost> PUT /tmp/ansible-local-2363388t42nd9i/tmpbt27ntxt TO /tmp/ansible-tmp-1660047605.1516645-236509-105742751858134/AnsiballZ_setup.py
Using module file /usr/lib/python3/dist-packages/ansible/modules/setup.py
<localhost> EXEC /bin/sh -c 'chmod u+x /tmp/ansible-tmp-1660047605.1516645-236509-105742751858134/ /tmp/ansible-tmp-1660047605.1516645-236509-105742751858134/AnsiballZ_setup.py && sleep 0'
<fedora> PUT /tmp/ansible-local-2363388t42nd9i/tmptwx0axtv TO /tmp/ansible-tmp-1660047605.2351809-236510-4382298702639/AnsiballZ_setup.py
<localhost> EXEC /bin/sh -c '/usr/bin/python3 /tmp/ansible-tmp-1660047605.1516645-236509-105742751858134/AnsiballZ_setup.py && sleep 0'
<fedora> EXEC ['/usr/bin/docker', b'exec', b'-u', 'root', b'-i', 'fedora', '/bin/sh', '-c', "/bin/sh -c 'chmod u+x /tmp/ansible-tmp-1660047605.2351809-236510-4382298702639/ /tmp/ansible-tmp-1660047605.2351809-236510-4382298702639/AnsiballZ_setup.py && sleep 0'"]
<fedora> EXEC ['/usr/bin/docker', b'exec', b'-u', 'root', b'-i', 'fedora', '/bin/sh', '-c', "/bin/sh -c '/usr/bin/python3 /tmp/ansible-tmp-1660047605.2351809-236510-4382298702639/AnsiballZ_setup.py && sleep 0'"]
<localhost> EXEC /bin/sh -c 'rm -f -r /tmp/ansible-tmp-1660047605.1516645-236509-105742751858134/ > /dev/null 2>&1 && sleep 0'
ok: [localhost]
<fedora> EXEC ['/usr/bin/docker', b'exec', b'-u', 'root', b'-i', 'fedora', '/bin/sh', '-c', "/bin/sh -c 'rm -f -r /tmp/ansible-tmp-1660047605.2351809-236510-4382298702639/ > /dev/null 2>&1 && sleep 0'"]
ok: [fedora]
META: ran handlers

TASK [Print OS] ***************************************************************************************************************
task path: /root/ansible-test/playbook/site.yml:62
ok: [localhost] => {
    "msg": "Debian"
}
redirecting (type: connection) ansible.builtin.docker to community.general.docker
Loading collection community.general from /root/.ansible/collections/ansible_collections/community/general
[WARNING]: Collection community.general does not support Ansible version 2.10.8
redirecting (type: connection) community.general.docker to community.docker.docker
ok: [fedora] => {
    "msg": "Fedora"
}

TASK [Print fact] *************************************************************************************************************
task path: /root/ansible-test/playbook/site.yml:66
ok: [localhost] => {
    "msg": 12
}
redirecting (type: connection) ansible.builtin.docker to community.general.docker
Loading collection community.general from /root/.ansible/collections/ansible_collections/community/general
[WARNING]: Collection community.general does not support Ansible version 2.10.8
redirecting (type: connection) community.general.docker to community.docker.docker
ok: [fedora] => {
    "msg": "rpm default fact"
}

TASK [Print pw] ***************************************************************************************************************
task path: /root/ansible-test/playbook/site.yml:70
Trying secret FileVaultSecret(filename='/root/.ans_vault_pass.txt') for vault_id=default
ok: [localhost] => {
    "msg": "PaSSw0rd"
}
Trying secret FileVaultSecret(filename='/root/.ans_vault_pass.txt') for vault_id=default
redirecting (type: connection) ansible.builtin.docker to community.general.docker
Loading collection community.general from /root/.ansible/collections/ansible_collections/community/general
[WARNING]: Collection community.general does not support Ansible version 2.10.8
redirecting (type: connection) community.general.docker to community.docker.docker
ok: [fedora] => {
    "msg": "PaSSw0rd"
}
META: ran handlers
META: ran handlers

PLAY RECAP ********************************************************************************************************************
fedora                     : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
localhost                  : ok=7    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

root@dev1-10:~/ansible-test/playbook# 

```

> Контейнер поднят из ansible:

```bash

root@dev1-10:~/ansible-test/playbook# docker ps -a
CONTAINER ID   IMAGE                                      COMMAND                  CREATED         STATUS                      PORTS     NAMES
b71ffff566e3   pycontribs/fedora                          "/bin/bash"              6 minutes ago   Up 6 minutes                

```




---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
