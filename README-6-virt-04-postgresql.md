# Домашнее задание к занятию "6.4. PostgreSQL"

## Задача 1

Используя docker поднимите инстанс PostgreSQL (версию 13). Данные БД сохраните в volume.

Подключитесь к БД PostgreSQL используя `psql`.

Воспользуйтесь командой `\?` для вывода подсказки по имеющимся в `psql` управляющим командам.

**Найдите и приведите** управляющие команды для:
- вывода списка БД

```bash

postgres=# \l+
                                                                   List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges   |  Size   | Tablespace |                Description                 
-----------+----------+----------+------------+------------+-----------------------+---------+------------+--------------------------------------------
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 |                       | 7901 kB | pg_default | default administrative connection database
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +| 7753 kB | pg_default | unmodifiable empty database
           |          |          |            |            | postgres=CTc/postgres |         |            | 
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +| 7753 kB | pg_default | default template for new databases
           |          |          |            |            | postgres=CTc/postgres |         |            | 
(3 rows)

postgres=# 

```

- подключения к БД

```bash

postgres=# SELECT *  FROM pg_stat_activity;
 datid | datname  | pid | leader_pid | usesysid | usename  | application_name | client_addr | client_hostname | client_port |         backend_start         |       
   xact_start           |          query_start          |         state_change         | wait_event_type |     wait_event      | state  | backend_xid | backend_xmin |              query               |         backend_type         
-------+----------+-----+------------+----------+----------+------------------+-------------+-----------------+-------------+-------------------------------+-------------------------------+-------------------------------+------------------------------+-----------------+---------------------+--------+-------------+--------------+----------------------------------+------------------------------
       |          |  64 |            |          |          |                  |             |                 |             | 2022-06-12 06:07:10.589698+00 |       
                        |                               |                              | Activity        | AutoVacuumMain      |        |             |             
 |                                  | autovacuum launcher
       |          |  66 |            |       10 | postgres |                  |             |                 |             | 2022-06-12 06:07:10.590981+00 |       
                        |                               |                              | Activity        | LogicalLauncherMain |        |             |             
 |                                  | logical replication launcher
 13445 | postgres |  76 |            |       10 | postgres | psql             |             |                 |          -1 | 2022-06-12 06:07:39.676175+00 | 2022-06-12 06:16:12.206066+00 | 2022-06-12 06:16:12.206066+00 | 2022-06-12 06:16:12.20607+00 |                 |                     | active |             |          486 | SELECT *  FROM pg_stat_activity; | client backend
       |          |  62 |            |          |          |                  |             |                 |             | 2022-06-12 06:07:10.588457+00 |       
                        |                               |                              | Activity        | BgWriterMain        |        |             |             
 |                                  | background writer
       |          |  61 |            |          |          |                  |             |                 |             | 2022-06-12 06:07:10.587713+00 |       
                        |                               |                              | Activity        | CheckpointerMain    |        |             |             
 |                                  | checkpointer
       |          |  63 |            |          |          |                  |             |                 |             | 2022-06-12 06:07:10.588965+00 |       
                        |                               |                              | Activity        | WalWriterMain       |        |             |             
 |                                  | walwriter
(6 rows)

postgres=# SELECT datname FROM pg_stat_activity;
 datname  
----------
 
 
 postgres
 
 
 
(6 rows)

postgres=# 

```

- вывода списка таблиц

```bash

postgres=# \dS
                        List of relations
   Schema   |              Name               | Type  |  Owner   
------------+---------------------------------+-------+----------
 pg_catalog | pg_aggregate                    | table | postgres
 pg_catalog | pg_am                           | table | postgres
 pg_catalog | pg_amop                         | table | postgres
 pg_catalog | pg_amproc                       | table | postgres
 pg_catalog | pg_attrdef                      | table | postgres
 pg_catalog | pg_attribute                    | table | postgres
 pg_catalog | pg_auth_members                 | table | postgres
 pg_catalog | pg_authid                       | table | postgres
 pg_catalog | pg_available_extension_versions | view  | postgres
 pg_catalog | pg_available_extensions         | view  | postgres
 pg_catalog | pg_cast                         | table | postgres
 pg_catalog | pg_class                        | table | postgres
 pg_catalog | pg_collation                    | table | postgres
 pg_catalog | pg_config                       | view  | postgres
 pg_catalog | pg_constraint                   | table | postgres
 pg_catalog | pg_conversion                   | table | postgres
 pg_catalog | pg_cursors                      | view  | postgres
 pg_catalog | pg_database                     | table | postgres
 pg_catalog | pg_db_role_setting              | table | postgres
 pg_catalog | pg_default_acl                  | table | postgres
 pg_catalog | pg_depend                       | table | postgres
 pg_catalog | pg_description                  | table | postgres
 pg_catalog | pg_enum                         | table | postgres
 pg_catalog | pg_event_trigger                | table | postgres
 pg_catalog | pg_extension                    | table | postgres
 pg_catalog | pg_file_settings                | view  | postgres
 pg_catalog | pg_foreign_data_wrapper         | table | postgres
 pg_catalog | pg_foreign_server               | table | postgres
 pg_catalog | pg_foreign_table                | table | postgres
 pg_catalog | pg_group                        | view  | postgres
 pg_catalog | pg_hba_file_rules               | view  | postgres
 pg_catalog | pg_index                        | table | postgres
 pg_catalog | pg_indexes                      | view  | postgres
 pg_catalog | pg_inherits                     | table | postgres
 pg_catalog | pg_init_privs                   | table | postgres
 pg_catalog | pg_language                     | table | postgres
 pg_catalog | pg_largeobject                  | table | postgres
 pg_catalog | pg_largeobject_metadata         | table | postgres
 pg_catalog | pg_locks                        | view  | postgres
 pg_catalog | pg_matviews                     | view  | postgres
 pg_catalog | pg_namespace                    | table | postgres
 pg_catalog | pg_opclass                      | table | postgres
 pg_catalog | pg_operator                     | table | postgres
 pg_catalog | pg_opfamily                     | table | postgres
 pg_catalog | pg_partitioned_table            | table | postgres
 pg_catalog | pg_policies                     | view  | postgres
 pg_catalog | pg_policy                       | table | postgres
 pg_catalog | pg_prepared_statements          | view  | postgres
 pg_catalog | pg_prepared_xacts               | view  | postgres
 pg_catalog | pg_proc                         | table | postgres
 pg_catalog | pg_publication                  | table | postgres
 pg_catalog | pg_publication_rel              | table | postgres
 pg_catalog | pg_publication_tables           | view  | postgres
 pg_catalog | pg_range                        | table | postgres
 pg_catalog | pg_replication_origin           | table | postgres
 pg_catalog | pg_replication_origin_status    | view  | postgres
 pg_catalog | pg_replication_slots            | view  | postgres
 pg_catalog | pg_rewrite                      | table | postgres
 pg_catalog | pg_roles                        | view  | postgres
 pg_catalog | pg_rules                        | view  | postgres
 pg_catalog | pg_seclabel                     | table | postgres
 pg_catalog | pg_seclabels                    | view  | postgres
 pg_catalog | pg_sequence                     | table | postgres
 pg_catalog | pg_sequences                    | view  | postgres
 pg_catalog | pg_settings                     | view  | postgres
 pg_catalog | pg_shadow                       | view  | postgres
 pg_catalog | pg_shdepend                     | table | postgres
 pg_catalog | pg_shdescription                | table | postgres
 pg_catalog | pg_shmem_allocations            | view  | postgres
 pg_catalog | pg_shseclabel                   | table | postgres
 pg_catalog | pg_stat_activity                | view  | postgres
 pg_catalog | pg_stat_all_indexes             | view  | postgres
 pg_catalog | pg_stat_all_tables              | view  | postgres
 pg_catalog | pg_stat_archiver                | view  | postgres
 pg_catalog | pg_stat_bgwriter                | view  | postgres
 pg_catalog | pg_stat_database                | view  | postgres
 pg_catalog | pg_stat_database_conflicts      | view  | postgres
 pg_catalog | pg_stat_gssapi                  | view  | postgres
 pg_catalog | pg_stat_progress_analyze        | view  | postgres
 pg_catalog | pg_stat_progress_basebackup     | view  | postgres
 pg_catalog | pg_stat_progress_cluster        | view  | postgres
 pg_catalog | pg_stat_progress_create_index   | view  | postgres
 pg_catalog | pg_stat_progress_vacuum         | view  | postgres
 pg_catalog | pg_stat_replication             | view  | postgres
 pg_catalog | pg_stat_slru                    | view  | postgres
 pg_catalog | pg_stat_ssl                     | view  | postgres
 pg_catalog | pg_stat_subscription            | view  | postgres
 pg_catalog | pg_stat_sys_indexes             | view  | postgres
 pg_catalog | pg_stat_sys_tables              | view  | postgres
 pg_catalog | pg_stat_user_functions          | view  | postgres
 pg_catalog | pg_stat_user_indexes            | view  | postgres
 pg_catalog | pg_stat_user_tables             | view  | postgres
 pg_catalog | pg_stat_wal_receiver            | view  | postgres
 pg_catalog | pg_stat_xact_all_tables         | view  | postgres
 pg_catalog | pg_stat_xact_sys_tables         | view  | postgres
 pg_catalog | pg_stat_xact_user_functions     | view  | postgres
 pg_catalog | pg_stat_xact_user_tables        | view  | postgres
 pg_catalog | pg_statio_all_indexes           | view  | postgres
 pg_catalog | pg_statio_all_sequences         | view  | postgres
 pg_catalog | pg_statio_all_tables            | view  | postgres
 pg_catalog | pg_statio_sys_indexes           | view  | postgres
 pg_catalog | pg_statio_sys_sequences         | view  | postgres
 pg_catalog | pg_statio_sys_tables            | view  | postgres
 pg_catalog | pg_statio_user_indexes          | view  | postgres
 pg_catalog | pg_statio_user_sequences        | view  | postgres
 pg_catalog | pg_statio_user_tables           | view  | postgres
 pg_catalog | pg_statistic                    | table | postgres
 pg_catalog | pg_statistic_ext                | table | postgres
 pg_catalog | pg_statistic_ext_data           | table | postgres
 pg_catalog | pg_stats                        | view  | postgres
 pg_catalog | pg_stats_ext                    | view  | postgres
 pg_catalog | pg_subscription                 | table | postgres
 pg_catalog | pg_subscription_rel             | table | postgres
 pg_catalog | pg_tables                       | view  | postgres
 pg_catalog | pg_tablespace                   | table | postgres
 pg_catalog | pg_timezone_abbrevs             | view  | postgres
 pg_catalog | pg_timezone_names               | view  | postgres
 pg_catalog | pg_transform                    | table | postgres
 pg_catalog | pg_trigger                      | table | postgres
 pg_catalog | pg_ts_config                    | table | postgres
 pg_catalog | pg_ts_config_map                | table | postgres
 pg_catalog | pg_ts_dict                      | table | postgres
 pg_catalog | pg_ts_parser                    | table | postgres
 pg_catalog | pg_ts_template                  | table | postgres
 pg_catalog | pg_type                         | table | postgres
 pg_catalog | pg_user                         | view  | postgres
 pg_catalog | pg_user_mapping                 | table | postgres
 pg_catalog | pg_user_mappings                | view  | postgres
 pg_catalog | pg_views                        | view  | postgres
(129 rows)

postgres=# 

```


- вывода описания содержимого таблиц

```bash

postgres=# \dS+
                                            List of relations
   Schema   |              Name               | Type  |  Owner   | Persistence |    Size    | Description 
------------+---------------------------------+-------+----------+-------------+------------+-------------
 pg_catalog | pg_aggregate                    | table | postgres | permanent   | 56 kB      | 
 pg_catalog | pg_am                           | table | postgres | permanent   | 40 kB      | 
 pg_catalog | pg_amop                         | table | postgres | permanent   | 80 kB      | 
 pg_catalog | pg_amproc                       | table | postgres | permanent   | 64 kB      | 
 pg_catalog | pg_attrdef                      | table | postgres | permanent   | 8192 bytes | 
 pg_catalog | pg_attribute                    | table | postgres | permanent   | 456 kB     | 
 pg_catalog | pg_auth_members                 | table | postgres | permanent   | 40 kB      | 
 pg_catalog | pg_authid                       | table | postgres | permanent   | 48 kB      | 
 pg_catalog | pg_available_extension_versions | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_available_extensions         | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_cast                         | table | postgres | permanent   | 48 kB      | 
 pg_catalog | pg_class                        | table | postgres | permanent   | 136 kB     | 
 pg_catalog | pg_collation                    | table | postgres | permanent   | 240 kB     | 
 pg_catalog | pg_config                       | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_constraint                   | table | postgres | permanent   | 48 kB      | 
 pg_catalog | pg_conversion                   | table | postgres | permanent   | 48 kB      | 
 pg_catalog | pg_cursors                      | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_database                     | table | postgres | permanent   | 48 kB      | 
 pg_catalog | pg_db_role_setting              | table | postgres | permanent   | 8192 bytes | 
 pg_catalog | pg_default_acl                  | table | postgres | permanent   | 8192 bytes | 
 pg_catalog | pg_depend                       | table | postgres | permanent   | 488 kB     | 
 pg_catalog | pg_description                  | table | postgres | permanent   | 376 kB     | 
 pg_catalog | pg_enum                         | table | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_event_trigger                | table | postgres | permanent   | 8192 bytes | 
 pg_catalog | pg_extension                    | table | postgres | permanent   | 48 kB      | 
 pg_catalog | pg_file_settings                | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_foreign_data_wrapper         | table | postgres | permanent   | 8192 bytes | 
 pg_catalog | pg_foreign_server               | table | postgres | permanent   | 8192 bytes | 
 pg_catalog | pg_foreign_table                | table | postgres | permanent   | 8192 bytes | 
 pg_catalog | pg_group                        | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_hba_file_rules               | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_index                        | table | postgres | permanent   | 64 kB      | 
 pg_catalog | pg_indexes                      | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_inherits                     | table | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_init_privs                   | table | postgres | permanent   | 56 kB      | 
 pg_catalog | pg_language                     | table | postgres | permanent   | 48 kB      | 
 pg_catalog | pg_largeobject                  | table | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_largeobject_metadata         | table | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_locks                        | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_matviews                     | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_namespace                    | table | postgres | permanent   | 48 kB      | 
 pg_catalog | pg_opclass                      | table | postgres | permanent   | 48 kB      | 
 pg_catalog | pg_operator                     | table | postgres | permanent   | 144 kB     | 
 pg_catalog | pg_opfamily                     | table | postgres | permanent   | 48 kB      | 
 pg_catalog | pg_partitioned_table            | table | postgres | permanent   | 8192 bytes | 
 pg_catalog | pg_policies                     | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_policy                       | table | postgres | permanent   | 8192 bytes | 
 pg_catalog | pg_prepared_statements          | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_prepared_xacts               | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_proc                         | table | postgres | permanent   | 688 kB     | 
 pg_catalog | pg_publication                  | table | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_publication_rel              | table | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_publication_tables           | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_range                        | table | postgres | permanent   | 40 kB      | 
 pg_catalog | pg_replication_origin           | table | postgres | permanent   | 8192 bytes | 
 pg_catalog | pg_replication_origin_status    | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_replication_slots            | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_rewrite                      | table | postgres | permanent   | 656 kB     | 
 pg_catalog | pg_roles                        | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_rules                        | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_seclabel                     | table | postgres | permanent   | 8192 bytes | 
 pg_catalog | pg_seclabels                    | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_sequence                     | table | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_sequences                    | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_settings                     | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_shadow                       | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_shdepend                     | table | postgres | permanent   | 40 kB      | 
 pg_catalog | pg_shdescription                | table | postgres | permanent   | 48 kB      | 
 pg_catalog | pg_shmem_allocations            | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_shseclabel                   | table | postgres | permanent   | 8192 bytes | 
 pg_catalog | pg_stat_activity                | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_stat_all_indexes             | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_stat_all_tables              | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_stat_archiver                | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_stat_bgwriter                | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_stat_database                | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_stat_database_conflicts      | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_stat_gssapi                  | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_stat_progress_analyze        | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_stat_progress_basebackup     | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_stat_progress_cluster        | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_stat_progress_create_index   | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_stat_progress_vacuum         | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_stat_replication             | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_stat_slru                    | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_stat_ssl                     | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_stat_subscription            | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_stat_sys_indexes             | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_stat_sys_tables              | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_stat_user_functions          | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_stat_user_indexes            | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_stat_user_tables             | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_stat_wal_receiver            | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_stat_xact_all_tables         | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_stat_xact_sys_tables         | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_stat_xact_user_functions     | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_stat_xact_user_tables        | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_statio_all_indexes           | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_statio_all_sequences         | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_statio_all_tables            | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_statio_sys_indexes           | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_statio_sys_sequences         | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_statio_sys_tables            | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_statio_user_indexes          | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_statio_user_sequences        | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_statio_user_tables           | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_statistic                    | table | postgres | permanent   | 248 kB     | 
 pg_catalog | pg_statistic_ext                | table | postgres | permanent   | 8192 bytes | 
 pg_catalog | pg_statistic_ext_data           | table | postgres | permanent   | 8192 bytes | 
 pg_catalog | pg_stats                        | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_stats_ext                    | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_subscription                 | table | postgres | permanent   | 8192 bytes | 
 pg_catalog | pg_subscription_rel             | table | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_tables                       | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_tablespace                   | table | postgres | permanent   | 48 kB      | 
 pg_catalog | pg_timezone_abbrevs             | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_timezone_names               | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_transform                    | table | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_trigger                      | table | postgres | permanent   | 8192 bytes | 
 pg_catalog | pg_ts_config                    | table | postgres | permanent   | 40 kB      | 
 pg_catalog | pg_ts_config_map                | table | postgres | permanent   | 56 kB      | 
 pg_catalog | pg_ts_dict                      | table | postgres | permanent   | 48 kB      | 
 pg_catalog | pg_ts_parser                    | table | postgres | permanent   | 40 kB      | 
 pg_catalog | pg_ts_template                  | table | postgres | permanent   | 40 kB      | 
 pg_catalog | pg_type                         | table | postgres | permanent   | 120 kB     | 
 pg_catalog | pg_user                         | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_user_mapping                 | table | postgres | permanent   | 8192 bytes | 
 pg_catalog | pg_user_mappings                | view  | postgres | permanent   | 0 bytes    | 
 pg_catalog | pg_views                        | view  | postgres | permanent   | 0 bytes    | 
(129 rows)

postgres=# 

```

- выхода из psql

```bash

postgres=# \q
postgres@a077a4625b1b:/$ 

```

## Задача 2

Используя `psql` создайте БД `test_database`.

```bash

postgres=# create database test_database;
CREATE DATABASE
postgres=# \l
                                   List of databases
     Name      |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges   
---------------+----------+----------+------------+------------+-----------------------
 postgres      | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
 template0     | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
               |          |          |            |            | postgres=CTc/postgres
 template1     | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
               |          |          |            |            | postgres=CTc/postgres
 test_database | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
(4 rows)

postgres=# 

```

Изучите [бэкап БД](https://github.com/netology-code/virt-homeworks/tree/master/06-db-04-postgresql/test_data).

Восстановите бэкап БД в `test_database`.

```bash

postgres-# \i /var/lib/postgresql/postgresql/test_data/test_dump.sql 
SET
SET
SET
SET
SET
 set_config 
------------
 
(1 row)

SET
SET
SET
SET
SET
SET
CREATE TABLE
ALTER TABLE
CREATE SEQUENCE
ALTER TABLE
ALTER SEQUENCE
ALTER TABLE
COPY 8
 setval 
--------
      8
(1 row)

ALTER TABLE

```

Перейдите в управляющую консоль `psql` внутри контейнера.

Подключитесь к восстановленной БД и проведите операцию ANALYZE для сбора статистики по таблице.

> Я нашел таблицу orders не в базе данных test_database, а в postgres.

```bash
test_database=# \c postgres 
You are now connected to database "postgres" as user "postgres".
postgres=# \dt
         List of relations
 Schema |  Name  | Type  |  Owner   
--------+--------+-------+----------
 public | orders | table | postgres
(1 row)

postgres=# ANALYZE VERBOSE orders;
INFO:  analyzing "public.orders"
INFO:  "orders": scanned 1 of 1 pages, containing 8 live rows and 0 dead rows; 8 rows in sample, 8 estimated total rows
ANALYZE
postgres=# \l
                                   List of databases
     Name      |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges   
---------------+----------+----------+------------+------------+-----------------------
 postgres      | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
 template0     | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
               |          |          |            |            | postgres=CTc/postgres
 template1     | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
               |          |          |            |            | postgres=CTc/postgres
 test_database | postgres | UTF8     | en_US.utf8 | en_US.utf8 | 
(4 rows)

postgres=# \c test_database 
You are now connected to database "test_database" as user "postgres".
test_database=# \dt
Did not find any relations.
test_database=# 



```

Используя таблицу [pg_stats](https://postgrespro.ru/docs/postgresql/12/view-pg-stats), найдите столбец таблицы `orders` 
с наибольшим средним значением размера элементов в байтах.

**Приведите в ответе** команду, которую вы использовали для вычисления и полученный результат.

```bash

postgres=# SELECT tablename, attname, avg_width FROM pg_stats WHERE tablename='orders' ORDER BY avg_width DESC;
 tablename | attname | avg_width 
-----------+---------+-----------
 orders    | title   |        16
 orders    | id      |         4
 orders    | price   |         4
(3 rows)

postgres=# 

```

## Задача 3

Архитектор и администратор БД выяснили, что ваша таблица orders разрослась до невиданных размеров и
поиск по ней занимает долгое время. Вам, как успешному выпускнику курсов DevOps в нетологии предложили
провести разбиение таблицы на 2 (шардировать на orders_1 - price>499 и orders_2 - price<=499).

Предложите SQL-транзакцию для проведения данной операции.

```bash

postgres=# CREATE TABLE orders_1 (
postgres(# CHECK (price > 499)
postgres(# ) INHERITS (orders);
CREATE TABLE
postgres=# CREATE TABLE orders_2 (
CHECK (price <= 499)
) INHERITS (orders);
CREATE TABLE
postgres=# \dt
          List of relations
 Schema |   Name   | Type  |  Owner   
--------+----------+-------+----------
 public | orders   | table | postgres
 public | orders_1 | table | postgres
 public | orders_2 | table | postgres
(3 rows)

postgres=# 
postgres=# CREATE RULE orders_insert_to_1 AS ON INSERT TO orders
postgres-# WHERE (price > 499)
postgres-# DO INSTEAD INSERT INTO orders_1 VALUES (NEW.*);
CREATE RULE
postgres=# CREATE RULE orders_insert_to_2 AS ON INSERT TO orders
WHERE (price <= 499)
DO INSTEAD INSERT INTO orders_2 VALUES (NEW.*);
CREATE RULE



postgres=# select * from orders;
 id |        title         | price 
----+----------------------+-------
  1 | War and peace        |   100
  2 | My little database   |   500
  3 | Adventure psql time  |   300
  4 | Server gravity falls |   300
  5 | Log gossips          |   123
  6 | WAL never lies       |   900
  7 | Me and my bash-pet   |   499
  8 | Dbiezdmin            |   501
(8 rows)

postgres=# INSERT INTO orders VALUES (9, 'New_order', 300);
INSERT 0 0
postgres=# select * from orders;
 id |        title         | price 
----+----------------------+-------
  1 | War and peace        |   100
  2 | My little database   |   500
  3 | Adventure psql time  |   300
  4 | Server gravity falls |   300
  5 | Log gossips          |   123
  6 | WAL never lies       |   900
  7 | Me and my bash-pet   |   499
  8 | Dbiezdmin            |   501
  9 | New_order            |   300
(9 rows)

postgres=# select * from orders_2;
 id |   title   | price 
----+-----------+-------
  9 | New_order |   300
(1 row)

postgres=# select * from orders_1;
 id | title | price 
----+-------+-------
(0 rows)

postgres=# INSERT INTO orders VALUES (10, 'New_order', 600);
INSERT 0 0
postgres=# select * from orders;
 id |        title         | price 
----+----------------------+-------
  1 | War and peace        |   100
  2 | My little database   |   500
  3 | Adventure psql time  |   300
  4 | Server gravity falls |   300
  5 | Log gossips          |   123
  6 | WAL never lies       |   900
  7 | Me and my bash-pet   |   499
  8 | Dbiezdmin            |   501
 10 | New_order            |   600
  9 | New_order            |   300
(10 rows)

postgres=# select * from orders_1;
 id |   title   | price 
----+-----------+-------
 10 | New_order |   600
(1 row)

postgres=# select * from orders_2;
 id |   title   | price 
----+-----------+-------
  9 | New_order |   300
(1 row)



```

Можно ли было изначально исключить "ручное" разбиение при проектировании таблицы orders?

```bash

CREATE TABLE orders (
id SERIAL,
title VARCHAR,
price INT,
) ENGINE = INNODB
PARTITION BY RANGE ( price ) (
PARTITION big_orders( price > 499 ), 
PARTITION small_orders( price <= 499 )
);

```

## Задача 4

Используя утилиту `pg_dump` создайте бекап БД `test_database`.

```bash

root@a077a4625b1b:/# pg_dump -d test_database -f /var/lib/postgresql/postgresql/backup/test_database.sql -U postgres
root@a077a4625b1b:/# ls -la /var/lib/postgresql/postgresql/backup/test_database.sql
-rw-r--r-- 1 root root 541 Jun 13 19:04 /var/lib/postgresql/postgresql/backup/test_database.sql
root@a077a4625b1b:/# cat /var/lib/postgresql/postgresql/backup/test_database.sql
--
-- PostgreSQL database dump
--

-- Dumped from database version 13.7 (Debian 13.7-1.pgdg110+1)
-- Dumped by pg_dump version 13.7 (Debian 13.7-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- PostgreSQL database dump complete
--



root@a077a4625b1b:/# 

```
> Но так как таблица orders в бд postgres:

```bash

root@a077a4625b1b:/# pg_dump postgres -f /var/lib/postgresql/postgresql/backup/postgres.sql -U postgres
root@a077a4625b1b:/# cat /var/lib/postgresql/postgresql/backup/postgres.sql 
--
-- PostgreSQL database dump
--

-- Dumped from database version 13.7 (Debian 13.7-1.pgdg110+1)
-- Dumped by pg_dump version 13.7 (Debian 13.7-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    title character varying(80) NOT NULL,
    price integer DEFAULT 0
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- Name: orders_1; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders_1 (
    CONSTRAINT orders_1_price_check CHECK ((price > 499))
)
INHERITS (public.orders);


ALTER TABLE public.orders_1 OWNER TO postgres;

--
-- Name: orders_2; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders_2 (
    CONSTRAINT orders_2_price_check CHECK ((price <= 499))
)
INHERITS (public.orders);


ALTER TABLE public.orders_2 OWNER TO postgres;

--
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orders_id_seq OWNER TO postgres;

--
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Name: orders_1 id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders_1 ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Name: orders_1 price; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders_1 ALTER COLUMN price SET DEFAULT 0;


--
-- Name: orders_2 id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders_2 ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Name: orders_2 price; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders_2 ALTER COLUMN price SET DEFAULT 0;


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (id, title, price) FROM stdin;
1       War and peace   100
2       My little database      500
3       Adventure psql time     300
4       Server gravity falls    300
5       Log gossips     123
6       WAL never lies  900
7       Me and my bash-pet      499
8       Dbiezdmin       501
\.


--
-- Data for Name: orders_1; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders_1 (id, title, price) FROM stdin;
10      New_order       600
\.


--
-- Data for Name: orders_2; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders_2 (id, title, price) FROM stdin;
9       New_order       300
\.


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orders_id_seq', 8, true);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: orders orders_insert_to_1; Type: RULE; Schema: public; Owner: postgres
--

CREATE RULE orders_insert_to_1 AS
    ON INSERT TO public.orders
   WHERE (new.price > 499) DO INSTEAD  INSERT INTO public.orders_1 (id, title, price)
  VALUES (new.id, new.title, new.price);


--
-- Name: orders orders_insert_to_2; Type: RULE; Schema: public; Owner: postgres
--

CREATE RULE orders_insert_to_2 AS
    ON INSERT TO public.orders
   WHERE (new.price <= 499) DO INSTEAD  INSERT INTO public.orders_2 (id, title, price)
  VALUES (new.id, new.title, new.price);


--
-- PostgreSQL database dump complete
--

root@a077a4625b1b:/# 


```

Как бы вы доработали бэкап-файл, чтобы добавить уникальность значения столбца `title` для таблиц `test_database`?

> Добавил бы ограничение UNIQUE(title): 

```bash

CREATE TABLE public.orders (
    id integer NOT NULL,
    title character varying(80) NOT NULL,
    UNIQUE(title),
    price integer DEFAULT 0
);

---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
