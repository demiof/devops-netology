# Домашнее задание к занятию "08.03 Работа с Roles"

## Подготовка к выполнению
1. Создайте два пустых публичных репозитория в любом своём проекте: elastic-role и kibana-role.
2. Скачайте [role](./roles/) из репозитория с домашним заданием и перенесите его в свой репозиторий elastic-role.
3. Скачайте дистрибутив [java](https://www.oracle.com/java/technologies/javase-jdk11-downloads.html) и положите его в директорию `playbook/files/`. 
4. Установите molecule: `pip3 install molecule`
5. Добавьте публичную часть своего ключа к своему профилю в github.

## Основная часть

Наша основная цель - разбить наш playbook на отдельные roles. Задача: сделать roles для elastic, kibana и написать playbook для использования этих ролей. Ожидаемый результат: существуют два ваших репозитория с roles и один репозиторий с playbook.

1. Создать в старой версии playbook файл `requirements.yml` и заполнить его следующим содержимым:
   ```yaml
   ---
     - src: git@github.com:netology-code/mnt-homeworks-ansible.git
       scm: git
       version: "1.0.1"
       name: java 
   ```
2. При помощи `ansible-galaxy` скачать себе эту роль. Запустите  `molecule test`, посмотрите на вывод команды.
3. Перейдите в каталог с ролью elastic-role и создайте сценарий тестирования по умолчаню при помощи `molecule init scenario --driver-name docker`.
4. Добавьте несколько разных дистрибутивов (centos:8, ubuntu:latest) для инстансов и протестируйте роль, исправьте найденные ошибки, если они есть. 
5. Создайте новый каталог с ролью при помощи `molecule init role --driver-name docker kibana-role`. Можете использовать другой драйвер, который более удобен вам.
6. На основе tasks из старого playbook заполните новую role. Разнесите переменные между `vars` и `default`. Проведите тестирование на разных дистрибитивах (centos:7, centos:8, ubuntu).
7. Выложите все roles в репозитории. Проставьте тэги, используя семантическую нумерацию.
8. Добавьте roles в `requirements.yml` в playbook.

```bash

root@dev1-10:~/netol_do/devops-netology/playbook-roles# ansible-galaxy install -r requirements.yml 
Starting galaxy role install process
- java (1.0.1) is already installed, skipping.
- kibana_role (v0.1) is already installed, skipping.
- extracting netology.elastic_role to /root/.ansible/roles/netology.elastic_role
- netology.elastic_role (v0.1) was installed successfully

```

9. Переработайте playbook на использование roles.

```bash

PLAY RECAP ****************************************************************************************************
192.168.1.200              : ok=35   changed=4    unreachable=0    failed=0    skipped=15   rescued=0    ignored=0   
192.168.1.201              : ok=7    changed=1    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   
localhost                  : ok=4    changed=2    unreachable=0    failed=0    skipped=4    rescued=0    ignored=0   
vm.linkintel.ru            : ok=0    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   

```

10. Выложите playbook в репозиторий.

> Т.к. тяжеловсеный files/, а vpn научил поднимать только с localhost, пришлось дистрибы удалить из files/ перед отправкой в git. Прошу добавить, в случае тестирования:

```bash
root@dev1-10:~/netol_do/devops-netology/playbook-roles# du -h --max-depth=1
28K     ./templates
4.0K    ./roles
36K     ./group_vars
1.6G    ./files
8.0K    ./inventory
1.6G    .

root@dev1-10:~/netol_do/devops-netology/playbook-roles# ll files/
total 1.3G
drwxr-xr-x 3 root root 4.0K Sep 10 21:12 .
drwxr-xr-x 7 root root 4.0K Sep 10 21:13 ..
-rw-r--r-- 1 root root 305M Sep 10 21:12 elasticsearch-7.10.1-linux-x86_64.tar.gz
-rw-r--r-- 1 root root 541M Sep 10 21:12 elasticsearch-8.4.0-linux-x86_64.tar.gz
drwxr-xr-x 8 root root 4.0K Sep 10 21:12 jdk-11
-rw-r--r-- 1 root root 268M Sep 10 21:12 kibana-8.4.0-linux-x86_64.tar.gz
-rw-r--r-- 1 root root 179M Sep 10 21:12 openjdk-11+28_linux-x64_bin.tar.gz

```

[https://github.com/demiof/ansible-playbook-roles/blob/master/files/screenshot-kibana.png](https://github.com/demiof/ansible-playbook-roles/blob/master/files/screenshot-kibana.png)


11. В ответ приведите ссылки на оба репозитория с roles и одну ссылку на репозиторий с playbook.

[https://github.com/demiof/kibana_role](https://github.com/demiof/kibana_role)

[https://github.com/demiof/netology.elastic_role](https://github.com/demiof/netology.elastic_role)

[https://github.com/demiof/ansible-playbook-roles](https://github.com/demiof/ansible-playbook-roles)




```bash

root@dev1-10:~/ansible-playbook/playbook# ansible-playbook -i inventory/prod.yml site.yml

PLAY [Some preparation checks] ********************************************************************************

TASK [Gathering Facts] ****************************************************************************************
ok: [192.168.1.201]
ok: [192.168.1.200]

TASK [check ssh to remote hosts works] ************************************************************************
changed: [192.168.1.201]
changed: [192.168.1.200]

TASK [Setting facts if vms are exists] ************************************************************************
ok: [192.168.1.200]
ok: [192.168.1.201]

PLAY [Create proxmox template or working vms] *****************************************************************

TASK [Create template vm template_debian_1vcpu_2cores_vmbr404_lvm_15] *****************************************
skipping: [localhost]

TASK [Clone vm template1] *************************************************************************************
skipping: [localhost] => (item=192.168.1.200) 
skipping: [localhost] => (item=192.168.1.201) 

TASK [Create new vm via Cloud-init] ***************************************************************************
skipping: [localhost] => (item=192.168.1.200) 
skipping: [localhost] => (item=192.168.1.201) 

PLAY [Set IP addresses] ***************************************************************************************

TASK [Set IP on each vm] **************************************************************************************
skipping: [vm.linkintel.ru] => (item=192.168.1.200) 
skipping: [vm.linkintel.ru] => (item=192.168.1.201) 

PLAY [Start] **************************************************************************************************

TASK [Start each vm] ******************************************************************************************
skipping: [localhost] => (item=192.168.1.200) 
skipping: [localhost] => (item=192.168.1.201) 

TASK [run vpn] ************************************************************************************************
changed: [localhost]

TASK [download tar.gz Elasticsearch need version] *************************************************************
ok: [localhost]

TASK [download tar.gz Kibana need version] ********************************************************************
ok: [localhost]

TASK [stop vpn] ***********************************************************************************************
changed: [localhost]

PLAY [Install Java] *******************************************************************************************

TASK [Gathering Facts] ****************************************************************************************
ok: [192.168.1.201]
ok: [192.168.1.200]

TASK [Set facts for Java 11 vars] *****************************************************************************
ok: [192.168.1.200]
ok: [192.168.1.201]

TASK [Upload .tar.gz file containing binaries from local storage] *********************************************
ok: [192.168.1.201]
ok: [192.168.1.200]

TASK [Ensure installation dir exists] *************************************************************************
ok: [192.168.1.200]
ok: [192.168.1.201]

TASK [Extract java in the installation directory] *************************************************************
skipping: [192.168.1.200]
skipping: [192.168.1.201]

PLAY [Install & Config Elasticsearch] *************************************************************************

TASK [Gathering Facts] ****************************************************************************************
ok: [192.168.1.200]

TASK [netology.elastic_role : Check if su exist] **************************************************************
ok: [192.168.1.200]

TASK [netology.elastic_role : Check if sudo exist] ************************************************************
ok: [192.168.1.200]

TASK [netology.elastic_role : Add the group elastic_group with sudo] ******************************************
ok: [192.168.1.200]

TASK [netology.elastic_role : Add the group elastic_group with su] ********************************************
skipping: [192.168.1.200]

TASK [netology.elastic_role : Add the user elastic_user with sudo] ********************************************
ok: [192.168.1.200]

TASK [netology.elastic_role : Add the user elastic_user with su] **********************************************
skipping: [192.168.1.200]

TASK [netology.elastic_role : copy tar.gz Elastic with sudo] **************************************************
ok: [192.168.1.200]

TASK [netology.elastic_role : copy tar.gz Elastic with su] ****************************************************
skipping: [192.168.1.200]

TASK [netology.elastic_role : Create directrory for Elasticsearch with sudo if not su] ************************
ok: [192.168.1.200]

TASK [netology.elastic_role : Create directrory for Elasticsearch with su] ************************************
skipping: [192.168.1.200]

TASK [netology.elastic_role : Extract Elasticsearch in the installation directory with sudo if not su] ********
skipping: [192.168.1.200]

TASK [netology.elastic_role : Extract Elasticsearch in the installation directory with su] ********************
skipping: [192.168.1.200]

TASK [netology.elastic_role : Set environment Elastic with sudo] **********************************************
ok: [192.168.1.200]

TASK [netology.elastic_role : Set environment Elastic with su] ************************************************
skipping: [192.168.1.200]

TASK [Make elk config] ****************************************************************************************
ok: [192.168.1.200]

TASK [Make jvm config] ****************************************************************************************
changed: [192.168.1.200]

TASK [Make max map count 262144] ******************************************************************************
changed: [192.168.1.200]

TASK [Make kibana config] *************************************************************************************
ok: [192.168.1.200]

PLAY [Install & Config Kibana] ********************************************************************************

TASK [Gathering Facts] ****************************************************************************************
ok: [192.168.1.200]

TASK [kibana_role : Check if su exist] ************************************************************************
ok: [192.168.1.200]

TASK [kibana_role : Check if sudo exist] **********************************************************************
ok: [192.168.1.200]

TASK [kibana_role : Add the group kibana_group with sudo] *****************************************************
ok: [192.168.1.200]

TASK [kibana_role : Add the group kibana_group with su] *******************************************************
skipping: [192.168.1.200]

TASK [kibana_role : Add the user kibana_user with sudo] *******************************************************
ok: [192.168.1.200]

TASK [kibana_role : Add the user kibana_user with su] *********************************************************
skipping: [192.168.1.200]

TASK [kibana_role : copy tar.gz Kibana with sudo] *************************************************************
ok: [192.168.1.200]

TASK [kibana_role : copy tar.gz Kibana with su] ***************************************************************
skipping: [192.168.1.200]

TASK [kibana_role : Create directrory for Kibana with sudo] ***************************************************
ok: [192.168.1.200]

TASK [kibana_role : Create directrory for Kibana with su] *****************************************************
skipping: [192.168.1.200]

TASK [kibana_role : Extract Kibana in the installation directory with sudo] ***********************************
skipping: [192.168.1.200]

TASK [kibana_role : Extract Kibana in the installation directory with su] *************************************
skipping: [192.168.1.200]

TASK [kibana_role : Set environment Kibana with sudo] *********************************************************
ok: [192.168.1.200]

TASK [kibana_role : Set environment Kibana with su] ***********************************************************
skipping: [192.168.1.200]

TASK [copy EnvironmentFile elasticsearch] *********************************************************************
ok: [192.168.1.200]

TASK [copy elasticsearch.service file] ************************************************************************
ok: [192.168.1.200]

TASK [copy kibana.service file] *******************************************************************************
ok: [192.168.1.200]

TASK [Create symbolic link to elasticsearch.service file] *****************************************************
ok: [192.168.1.200]

TASK [Create symbolic link to kibana.service file] ************************************************************
ok: [192.168.1.200]

TASK [Run systemctl daemon-reload for commit unit files] ******************************************************
changed: [192.168.1.200]

TASK [Start elasticsearch via systemd] ************************************************************************
ok: [192.168.1.200]

TASK [Start kibana via systemd] *******************************************************************************
ok: [192.168.1.200]

PLAY RECAP ****************************************************************************************************
192.168.1.200              : ok=35   changed=4    unreachable=0    failed=0    skipped=15   rescued=0    ignored=0   
192.168.1.201              : ok=7    changed=1    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   
localhost                  : ok=4    changed=2    unreachable=0    failed=0    skipped=4    rescued=0    ignored=0   
vm.linkintel.ru            : ok=0    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   

root@dev1-10:~/ansible-playbook/playbook# 

```


## Необязательная часть

1. Проделайте схожие манипуляции для создания роли logstash.
2. Создайте дополнительный набор tasks, который позволяет обновлять стек ELK.
3. В ролях добавьте тестирование в раздел `verify.yml`. Данный раздел должен проверять, что elastic запущен и возвращает успешный статус по API, web-интерфейс kibana отвечает без кодов ошибки, logstash через команду `logstash -e 'input { stdin { } } output { stdout {} }'`.
4. Убедитесь в работоспособности своего стека. Возможно, потребуется тестировать все роли одновременно.
5. Выложите свои roles в репозитории. В ответ приведите ссылки.

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
