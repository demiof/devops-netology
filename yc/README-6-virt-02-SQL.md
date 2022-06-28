# Домашнее задание к занятию "6.2. SQL"

## Введение

Перед выполнением задания вы можете ознакомиться с 
[дополнительными материалами](https://github.com/netology-code/virt-homeworks/tree/master/additional/README.md).
ё
## Задача 1

Используя docker поднимите инстанс PostgreSQL (версию 12) c 2 volume, 
в который будут складываться данные БД и бэкапы.

Приведите получившуюся команду или docker-compose манифест.

```bash

version: '3.0'
networks:
  monitoring:
    driver: bridge
services:
  postgresql:
    container_name: postgres_12_2_vol
    image: postgres
    environment:

      POSTGRES_USER: test-admin-user
      POSTGRES_PASSWORD: ''
      POSTGRES_URL: postgres://test-admin-user:''@localhost:5432/test_db
      POSTGRES_DB: test_db
      POSTGRES_HOST: postgres
      POSTGRES_HOST_AUTH_METHOD: trust
    volumes:
      - db-data-vol1:/var/lib/docker/volumes/db-data-vol1/_data
      - db-data-vol2:/var/lib/docker/volumes/db-data-vol2/_data
volumes:
  db-data-vol1:
  db-data-vol2:

```

## Задача 2

В БД из задачи 1: 
- создайте пользователя test-admin-user и БД test_db
- в БД test_db создайте таблицу orders и clients (спeцификация таблиц ниже)
- предоставьте привилегии на все операции пользователю test-admin-user на таблицы БД test_db
- создайте пользователя test-simple-user  
- предоставьте пользователю test-simple-user права на SELECT/INSERT/UPDATE/DELETE данных таблиц БД test_db

Таблица orders:
- id (serial primary key)
- наименование (string)
- цена (integer)

Таблица clients:
- id (serial primary key)
- фамилия (string)
- страна проживания (string, index)
- заказ (foreign key orders)

Приведите:
- итоговый список БД после выполнения пунктов выше,
- описание таблиц (describe)
- SQL-запрос для выдачи списка пользователей с правами над таблицами test_db
- список пользователей с правами над таблицами test_db


```bash

test_db-# \d clients
 id                | integer               |           | not null | nextval('clients_id_seq'::regclass)
 фамилия           | character varying(40) |           |          | 
 страна проживания | character varying(40) |           |          | 
 заказ             | integer               |           |          | 


test_db=# \d+ clients
                                                                    Table "public.clients"
      Column       |         Type          | Collation | Nullable |               Default               | Storage  | Comp
ression | Stats target | Description 
-------------------+-----------------------+-----------+----------+-------------------------------------+----------+-----
--------+--------------+-------------
 id                | integer               |           | not null | nextval('clients_id_seq'::regclass) | plain    |     
        |              | 
 фамилия           | character varying(40) |           |          |                                     | extended |     
        |              | 
 страна проживания | character varying(40) |           |          |                                     | extended |     
        |              | 
 заказ             | integer               |           |          |                                     | plain    |     
        |              | 
Indexes:
    "clients_pkey" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "orders" FOREIGN KEY (id) REFERENCES orders(id)
Access method: heap




test_db-# \d orders
 id           | integer               |           | not null | nextval('orders_id_seq'::regclass)
 наименование | character varying(40) |           |          | 
 цена         | integer               |           |          | 




test_db=# \d+ orders;
                                                                 Table "public.orders"
    Column    |         Type          | Collation | Nullable |              Default               | Storage  | Compressio
n | Stats target | Description 
--------------+-----------------------+-----------+----------+------------------------------------+----------+-----------
--+--------------+-------------
 id           | integer               |           | not null | nextval('orders_id_seq'::regclass) | plain    |           
  |              | 
 наименование | character varying(40) |           |          |                                    | extended |           
  |              | 
 цена         | integer               |           |          |                                    | plain    |           
  |              | 
Indexes:
    "orders_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "clients" CONSTRAINT "orders" FOREIGN KEY (id) REFERENCES orders(id)
Access method: heap


test_db-# \du
 test-admin-user  | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
 test-simple-user |                                                            | {}

test_db=# SELECT rolname FROM pg_roles;
 pg_database_owner
 pg_read_all_data
 pg_write_all_data
 pg_monitor
 pg_read_all_settings
 pg_read_all_stats
 pg_stat_scan_tables
 pg_read_server_files
 pg_write_server_files
 pg_execute_server_program
 pg_signal_backend
 test-admin-user
 test-simple-user


```

## Задача 3

Используя SQL синтаксис - наполните таблицы следующими тестовыми данными:

Таблица orders

|Наименование|цена|
|------------|----|
|Шоколад| 10 |
|Принтер| 3000 |
|Книга| 500 |
|Монитор| 7000|
|Гитара| 4000|

Таблица clients

|ФИО|Страна проживания|
|------------|----|
|Иванов Иван Иванович| USA |
|Петров Петр Петрович| Canada |
|Иоганн Себастьян Бах| Japan |
|Ронни Джеймс Дио| Russia|
|Ritchie Blackmore| Russia|

Используя SQL синтаксис:
- вычислите количество записей для каждой таблицы 
- приведите в ответе:
    - запросы 
    - результаты их выполнения.

```bash

test_db=# select * from orders;
 id | наименование | цена 
----+--------------+------
  1 | Шоколад      |   10
  2 | Принтер      | 3000
  3 | Книга        |  500
  4 | Монитор      | 7000
  5 | Гитара       | 4000
(5 rows)

test_db=# select * from clients;
 id |       фамилия        | страна проживания | заказ 
----+----------------------+-------------------+-------
  1 | Иванов Иван Иванович | USA               |      
  2 | Петров Петр Петрович | Canada            |      
  3 | Иоган Себастьян Бах  | Japan             |      
  4 | Ронни Джеймс Дио     | Russia            |      
  5 | Ritchie Blackmore    | Russia            |      
(5 rows)

test_db=# select count(*) from orders;
 count 
-------
     5
(1 row)

test_db=# select count(*) from clients;
 count 
-------
     5
(1 row)

test_db=# select count(1) from orders;
 count 
-------
     5
(1 row)

test_db=# select count(1) from clients;
 count 
-------
     5
(1 row)

test_db=# 

```

## Задача 4

Часть пользователей из таблицы clients решили оформить заказы из таблицы orders.

```bash


test_db=# UPDATE clients SET заказ = 5 WHERE id = 1;
UPDATE 1
test_db=# UPDATE clients SET заказ = 4 WHERE id = 2;
UPDATE 1
test_db=# UPDATE clients SET заказ = 3 WHERE id = 3;
UPDATE 1
test_db=# UPDATE clients SET заказ = 2 WHERE id = 4;
UPDATE 1
test_db=# UPDATE clients SET заказ = 1 WHERE id = 5;
UPDATE 1

```

Используя foreign keys свяжите записи из таблиц, согласно таблице:

|ФИО|Заказ|
|------------|----|
|Иванов Иван Иванович| Книга |
|Петров Петр Петрович| Монитор |
|Иоганн Себастьян Бах| Гитара |

Приведите SQL-запросы для выполнения данных операций.

```bash

Foreign-key constraints:
    "orders" FOREIGN KEY (id) REFERENCES orders(id)
Access method: heap

```

Приведите SQL-запрос для выдачи всех пользователей, которые совершили заказ, а также вывод данного запроса.

```bash

test_db=# SELECT * FROM clients c
LEFT JOIN orders o
ON c.заказ = o.id;
 id |       фамилия        | страна проживания | заказ | id | наименование | цена 
----+----------------------+-------------------+-------+----+--------------+------
  1 | Иванов Иван Иванович | USA               |     5 |  5 | Гитара       | 4000
  2 | Петров Петр Петрович | Canada            |     4 |  4 | Монитор      | 7000
  3 | Иоган Себастьян Бах  | Japan             |     3 |  3 | Книга        |  500
  4 | Ронни Джеймс Дио     | Russia            |     2 |  2 | Принтер      | 3000
  5 | Ritchie Blackmore    | Russia            |     1 |  1 | Шоколад      |   10
(5 rows)

```
Подсказк - используйте директиву `UPDATE`.

## Задача 5

Получите полную информацию по выполнению запроса выдачи всех пользователей из задачи 4 
(используя директиву EXPLAIN).

```bash

test_db=# EXPLAIN SELECT * FROM clients c
LEFT JOIN orders o
ON c.заказ = o.id;
                               QUERY PLAN                                
-------------------------------------------------------------------------
 Hash Left Join  (cost=23.50..37.93 rows=350 width=310)
   Hash Cond: (c."заказ" = o.id)
   ->  Seq Scan on clients c  (cost=0.00..13.50 rows=350 width=204)
   ->  Hash  (cost=16.00..16.00 rows=600 width=106)
         ->  Seq Scan on orders o  (cost=0.00..16.00 rows=600 width=106)
(5 rows)

test_db=# 

```

> Узлы выеденные при последовательном сканировании дают сл. информацию:
- Приблизительная стоимость запуcка Left Join  23.50
- Приблизительная общая стоимость 37.93
- Ожидаемой число срок для первого узла плана 350
- Ожидаемый средний размер строк 310 bytes
> Ниже по остальным узлам составляющие описанную выше процедуру ...


```bash

test_db=# EXPLAIN ANALYZE SELECT * FROM clients c
LEFT JOIN orders o
ON c.заказ = o.id;
                                                    QUERY PLAN                                                     
-------------------------------------------------------------------------------------------------------------------
 Hash Left Join  (cost=23.50..37.93 rows=350 width=310) (actual time=0.100..0.108 rows=5 loops=1)
   Hash Cond: (c."заказ" = o.id)
   ->  Seq Scan on clients c  (cost=0.00..13.50 rows=350 width=204) (actual time=0.028..0.033 rows=5 loops=1)
   ->  Hash  (cost=16.00..16.00 rows=600 width=106) (actual time=0.029..0.030 rows=5 loops=1)
         Buckets: 1024  Batches: 1  Memory Usage: 9kB
         ->  Seq Scan on orders o  (cost=0.00..16.00 rows=600 width=106) (actual time=0.014..0.015 rows=5 loops=1)
 Planning Time: 0.828 ms
 Execution Time: 0.250 ms
(8 rows)

```
> Проверка точности планировщика, благо более понятно, так как сканирование по clients займет actual time 0.028..0.033 ms. По join - 0.029..0.030 ms, по сканированию orders - 0.014..0.015 ms. Т.е. всего планируемое (затраченное на построение плана запроса из разобранного и его оптимизацию, время собственного разбора не включается) - 0.828 ms и актуальное время (прод-ть запуска и остановки исполнения запроса) - 0.250 ms 


Приведите получившийся результат и объясните что значат полученные значения.

## Задача 6

Создайте бэкап БД test_db и поместите его в volume, предназначенный для бэкапов (см. Задачу 1).

```bash

root@0493c38de6b6:/# pg_basebackup -h localhost -U test-admin-user -D /var/lib/docker/volumes/db-data-vol2/_data/
root@0493c38de6b6:/# ls -la /var/lib/docker/volumes/db-data-vol2/_data
total 312
drwxr-xr-x 19 root root   4096 Jun  2 16:04 .
drwxr-xr-x  3 root root   4096 Jun  1 19:39 ..
-rw-------  1 root root    225 Jun  2 16:04 backup_label
-rw-------  1 root root 181160 Jun  2 16:04 backup_manifest
drwx------  6 root root   4096 Jun  2 16:04 base
drwx------  2 root root   4096 Jun  2 16:04 global
drwx------  2 root root   4096 Jun  2 16:04 pg_commit_ts
drwx------  2 root root   4096 Jun  2 16:04 pg_dynshmem
-rw-------  1 root root   4917 Jun  2 16:04 pg_hba.conf
-rw-------  1 root root   1636 Jun  2 16:04 pg_ident.conf
drwx------  4 root root   4096 Jun  2 16:04 pg_logical
drwx------  4 root root   4096 Jun  2 16:04 pg_multixact
drwx------  2 root root   4096 Jun  2 16:04 pg_notify
drwx------  2 root root   4096 Jun  2 16:04 pg_replslot
drwx------  2 root root   4096 Jun  2 16:04 pg_serial
drwx------  2 root root   4096 Jun  2 16:04 pg_snapshots
drwx------  2 root root   4096 Jun  2 16:04 pg_stat
drwx------  2 root root   4096 Jun  2 16:04 pg_stat_tmp
drwx------  2 root root   4096 Jun  2 16:04 pg_subtrans
drwx------  2 root root   4096 Jun  2 16:04 pg_tblspc
drwx------  2 root root   4096 Jun  2 16:04 pg_twophase
-rw-------  1 root root      3 Jun  2 16:04 PG_VERSION
drwx------  3 root root   4096 Jun  2 16:04 pg_wal
drwx------  2 root root   4096 Jun  2 16:04 pg_xact
-rw-------  1 root root     88 Jun  2 16:04 postgresql.auto.conf
-rw-------  1 root root  28835 Jun  2 16:04 postgresql.conf
root@0493c38de6b6:/# 

```

Остановите контейнер с PostgreSQL (но не удаляйте volumes).

```bash

root@dev1-10:~/netol_do/docker-compose# docker ps
CONTAINER ID   IMAGE      COMMAND                  CREATED        STATUS        PORTS      NAMES
0493c38de6b6   postgres   "docker-entrypoint.s…"   20 hours ago   Up 20 hours   5432/tcp   postgres_12_2_vol


root@dev1-10:~/netol_do/docker-compose# ls -la /var/lib/docker/volumes/docker-compose_db-data-vol2/_data/
total 312
drwxr-xr-x 19 root root   4096 Jun  2 19:04 .
drwx-----x  3 root root   4096 Jun  1 22:37 ..
-rw-------  1 root root    225 Jun  2 19:04 backup_label
-rw-------  1 root root 181160 Jun  2 19:04 backup_manifest
drwx------  6 root root   4096 Jun  2 19:04 base
drwx------  2 root root   4096 Jun  2 19:04 global
drwx------  2 root root   4096 Jun  2 19:04 pg_commit_ts
drwx------  2 root root   4096 Jun  2 19:04 pg_dynshmem
-rw-------  1 root root   4917 Jun  2 19:04 pg_hba.conf
-rw-------  1 root root   1636 Jun  2 19:04 pg_ident.conf
drwx------  4 root root   4096 Jun  2 19:04 pg_logical
drwx------  4 root root   4096 Jun  2 19:04 pg_multixact
drwx------  2 root root   4096 Jun  2 19:04 pg_notify
drwx------  2 root root   4096 Jun  2 19:04 pg_replslot
drwx------  2 root root   4096 Jun  2 19:04 pg_serial
drwx------  2 root root   4096 Jun  2 19:04 pg_snapshots
drwx------  2 root root   4096 Jun  2 19:04 pg_stat
drwx------  2 root root   4096 Jun  2 19:04 pg_stat_tmp
drwx------  2 root root   4096 Jun  2 19:04 pg_subtrans
drwx------  2 root root   4096 Jun  2 19:04 pg_tblspc
drwx------  2 root root   4096 Jun  2 19:04 pg_twophase
-rw-------  1 root root      3 Jun  2 19:04 PG_VERSION
drwx------  3 root root   4096 Jun  2 19:04 pg_wal
drwx------  2 root root   4096 Jun  2 19:04 pg_xact
-rw-------  1 root root     88 Jun  2 19:04 postgresql.auto.conf
-rw-------  1 root root  28835 Jun  2 19:04 postgresql.conf

root@dev1-10:~/netol_do/docker-compose# docker container stop 0493c38de6b6
0493c38de6b6
root@dev1-10:~/netol_do/docker-compose# docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
root@dev1-10:~/netol_do/docker-compose# 

root@dev1-10:~/netol_do/docker-compose# ls -la /var/lib/docker/volumes/docker-compose_db-data-vol2/_data/
total 312
drwxr-xr-x 19 root root   4096 Jun  2 19:04 .
drwx-----x  3 root root   4096 Jun  1 22:37 ..
-rw-------  1 root root    225 Jun  2 19:04 backup_label
-rw-------  1 root root 181160 Jun  2 19:04 backup_manifest
drwx------  6 root root   4096 Jun  2 19:04 base
drwx------  2 root root   4096 Jun  2 19:04 global
drwx------  2 root root   4096 Jun  2 19:04 pg_commit_ts
drwx------  2 root root   4096 Jun  2 19:04 pg_dynshmem
-rw-------  1 root root   4917 Jun  2 19:04 pg_hba.conf
-rw-------  1 root root   1636 Jun  2 19:04 pg_ident.conf
drwx------  4 root root   4096 Jun  2 19:04 pg_logical
drwx------  4 root root   4096 Jun  2 19:04 pg_multixact
drwx------  2 root root   4096 Jun  2 19:04 pg_notify
drwx------  2 root root   4096 Jun  2 19:04 pg_replslot
drwx------  2 root root   4096 Jun  2 19:04 pg_serial
drwx------  2 root root   4096 Jun  2 19:04 pg_snapshots
drwx------  2 root root   4096 Jun  2 19:04 pg_stat
drwx------  2 root root   4096 Jun  2 19:04 pg_stat_tmp
drwx------  2 root root   4096 Jun  2 19:04 pg_subtrans
drwx------  2 root root   4096 Jun  2 19:04 pg_tblspc
drwx------  2 root root   4096 Jun  2 19:04 pg_twophase
-rw-------  1 root root      3 Jun  2 19:04 PG_VERSION
drwx------  3 root root   4096 Jun  2 19:04 pg_wal
drwx------  2 root root   4096 Jun  2 19:04 pg_xact
-rw-------  1 root root     88 Jun  2 19:04 postgresql.auto.conf
-rw-------  1 root root  28835 Jun  2 19:04 postgresql.conf
root@dev1-10:~/netol_do/docker-compose# 

root@dev1-10:~/netol_do/docker-compose# docker ps -a
CONTAINER ID   IMAGE      COMMAND                  CREATED        STATUS                     PORTS     NAMES
0493c38de6b6   postgres   "docker-entrypoint.s…"   22 hours ago   Exited (0) 7 seconds ago             postgres_12_2_vol



```

Поднимите новый пустой контейнер с PostgreSQL.

```bash

root@dev1-10:~/netol_do/docker-compose# docker ps -a
CONTAINER ID   IMAGE      COMMAND                  CREATED         STATUS         PORTS      NAMES
f5230294f073   postgres   "docker-entrypoint.s…"   9 seconds ago   Up 7 seconds   5432/tcp   postgres_12_2_vol-one-more-container

root@f5230294f073:/# ls /var/lib/docker/volumes/db-data-vol2/_data/
backup_label     base    pg_commit_ts  pg_hba.conf    pg_logical    pg_notify    pg_serial     pg_stat      pg_subtrans  pg_twophase  pg_wal   postgresql.auto.conf
backup_manifest  global  pg_dynshmem   pg_ident.conf  pg_multixact  pg_replslot  pg_snapshots  pg_stat_tmp  pg_tblspc    PG_VERSION   pg_xact  postgresql.conf

root@f5230294f073:/# postgres
"root" execution of the PostgreSQL server is not permitted.
The server must be started under an unprivileged user ID to prevent
possible system security compromise.  See the documentation for
more information on how to properly start the server.
root@f5230294f073:/# psql test_db test-admin-user
psql (14.3 (Debian 14.3-1.pgdg110+1))
Type "help" for help.

test_db=# \d+
                                               List of relations
 Schema |      Name      |   Type   |      Owner      | Persistence | Access method |    Size    | Description 
--------+----------------+----------+-----------------+-------------+---------------+------------+-------------
 public | clients        | table    | test-admin-user | permanent   | heap          | 8192 bytes | 
 public | clients_id_seq | sequence | test-admin-user | permanent   |               | 8192 bytes | 
 public | orders         | table    | test-admin-user | permanent   | heap          | 8192 bytes | 
 public | orders_id_seq  | sequence | test-admin-user | permanent   |               | 8192 bytes | 
(4 rows)

test_db=# root@dev1-10:~/netol_do/docker-compose# 

```

Восстановите БД test_db в новом контейнере.

Приведите список операций, который вы применяли для бэкапа данных и восстановления. 

---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
