    # Домашнее задание к занятию "6.3. MySQL"

## Введение

Перед выполнением задания вы можете ознакомиться с 
[дополнительными материалами](https://github.com/netology-code/virt-homeworks/tree/master/additional/README.md).

## Задача 1

Используя docker поднимите инстанс MySQL (версию 8). Данные БД сохраните в volume.

Изучите [бэкап БД](https://github.com/netology-code/virt-homeworks/tree/master/06-db-03-mysql/test_data) и 
восстановитесь из него.

Перейдите в управляющую консоль `mysql` внутри контейнера.

Используя команду `\h` получите список управляющих команд.

Найдите команду для выдачи статуса БД и **приведите в ответе** из ее вывода версию сервера БД.

```bash
8.0.29 MySQL Community Server - GPL
```
Подключитесь к восстановленной БД и получите список таблиц из этой БД.

**Приведите в ответе** количество записей с `price` > 300.

```bash

mysql> select * from orders where price > 300;
+----+----------------+-------+
| id | title          | price |
+----+----------------+-------+
|  2 | My little pony |   500 |
+----+----------------+-------+
1 row in set (0.01 sec)

mysql> 

```

В следующих заданиях мы будем продолжать работу с данным контейнером.

## Задача 2

Создайте пользователя test в БД c паролем test-pass, используя:
- плагин авторизации mysql_native_password
- срок истечения пароля - 180 дней 
- количество попыток авторизации - 3 
- максимальное количество запросов в час - 100
- аттрибуты пользователя:
    - Фамилия "Pretty"
    - Имя "James"

Предоставьте привелегии пользователю `test` на операции SELECT базы `test_db`.
    
Используя таблицу INFORMATION_SCHEMA.USER_ATTRIBUTES получите данные по пользователю `test` и 
**приведите в ответе к задаче**.

```bash

mysql> SELECT * FROM INFORMATION_SCHEMA.USER_ATTRIBUTES WHERE USER = 'test';
+------+-----------+----------------------------------------------+
| USER | HOST      | ATTRIBUTE                                    |
+------+-----------+----------------------------------------------+
| test | localhost | {"Lastname": "Pretty", "Firstname": "James"} |
+------+-----------+----------------------------------------------+
1 row in set (0.01 sec)

mysql> 

```


## Задача 3

Установите профилирование `SET profiling = 1`.
Изучите вывод профилирования команд `SHOW PROFILES;`.

```bash

mysql> SHOW PROFILES;
+----------+------------+-----------------------------+
| Query_ID | Duration   | Query                       |
+----------+------------+-----------------------------+
|        1 | 0.00858700 | SELECT @@profiling          |
|        2 | 0.00032075 | select * from x$processlist |
|        3 | 0.01300450 | show databases              |
|        4 | 0.00046725 | SELECT DATABASE()           |
|        5 | 0.00143450 | show databases              |
|        6 | 0.02450700 | show tables                 |
|        7 | 0.09450925 | select * from x$processlist |
+----------+------------+-----------------------------+
7 rows in set, 1 warning (0.00 sec)

mysql> 

```

> Соответственно слева направо: порядковый номер запроса, его длительность, и сам запрос.


Исследуйте, какой `engine` используется в таблице БД `test_db` и **приведите в ответе**.

> Ниже какие бывают: 9 типов - FEDERATED для хранилища; MEMORY для временного в памяти; InnoDB - поддерживает транзакции, блокирование на низклм уровне и внешних ключах,  PERFOMANCE_SCHEMA, MyIsam, MRG_MyIsam, BLACKHOLE, CSV, ARHIVE

```bash

mysql> SHOW ENGINES\G
*************************** 1. row ***************************
      Engine: FEDERATED
     Support: NO
     Comment: Federated MySQL storage engine
Transactions: NULL
          XA: NULL
  Savepoints: NULL
*************************** 2. row ***************************
      Engine: MEMORY
     Support: YES
     Comment: Hash based, stored in memory, useful for temporary tables
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 3. row ***************************
      Engine: InnoDB
     Support: DEFAULT
     Comment: Supports transactions, row-level locking, and foreign keys
Transactions: YES
          XA: YES
  Savepoints: YES
*************************** 4. row ***************************
      Engine: PERFORMANCE_SCHEMA
     Support: YES
     Comment: Performance Schema
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 5. row ***************************
      Engine: MyISAM
     Support: YES
     Comment: MyISAM storage engine
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 6. row ***************************
      Engine: MRG_MYISAM
     Support: YES
     Comment: Collection of identical MyISAM tables
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 7. row ***************************
      Engine: BLACKHOLE
     Support: YES
     Comment: /dev/null storage engine (anything you write to it disappears)
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 8. row ***************************
      Engine: CSV
     Support: YES
     Comment: CSV storage engine
Transactions: NO
          XA: NO
  Savepoints: NO
*************************** 9. row ***************************
      Engine: ARCHIVE
     Support: YES
     Comment: Archive storage engine
Transactions: NO
          XA: NO
  Savepoints: NO
9 rows in set (0.00 sec)

```

> база test_db имеем таблицу orders с движком InnoDB: 

```bash

mysql> SHOW CREATE TABLE orders;
+--------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table  | Create Table                                                                                                                                                                                                                              |
+--------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| orders | CREATE TABLE `orders` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(80) NOT NULL,
  `price` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci |
+--------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

mysql>

```

> Или так:

```bash

mysql> SELECT * FROM information_schema.TABLES WHERE TABLE_NAME = 'orders' ORDER BY ENGINE asc;
+---------------+--------------+------------+------------+--------+---------+------------+------------+----------------+-------------+-----------------+--------------+-----------+----------------+---------------------+---------------------+------------+--------------------+----------+----------------+---------------+
| TABLE_CATALOG | TABLE_SCHEMA | TABLE_NAME | TABLE_TYPE | ENGINE | VERSION | ROW_FORMAT | TABLE_ROWS | AVG_ROW_LENGTH | DATA_LENGTH | MAX_DATA_LENGTH | INDEX_LENGTH | DATA_FREE | AUTO_INCREMENT | CREATE_TIME         | UPDATE_TIME         | CHECK_TIME | TABLE_COLLATION    | CHECKSUM | CREATE_OPTIONS | TABLE_COMMENT |
+---------------+--------------+------------+------------+--------+---------+------------+------------+----------------+-------------+-----------------+--------------+-----------+----------------+---------------------+---------------------+------------+--------------------+----------+----------------+---------------+
| def           | test_db      | orders     | BASE TABLE | InnoDB |      10 | Dynamic    |          5 |           3276 |       16384 |               0 |            0 |         0 |              6 | 2022-06-05 19:17:41 | 2022-06-05 19:17:41 | NULL       | utf8mb4_0900_ai_ci |     NULL |                |               |
+---------------+--------------+------------+------------+--------+---------+------------+------------+----------------+-------------+-----------------+--------------+-----------+----------------+---------------------+---------------------+------------+--------------------+----------+----------------+---------------+
1 row in set (0.00 sec)

mysql> 

```

Измените `engine` и **приведите время выполнения и запрос на изменения из профайлера в ответе**:
- на `MyISAM`

```bash

mysql> use test_db;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> ALTER TABLE orders ENGINE = MyISAM;
Query OK, 5 rows affected (0.14 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM information_schema.TABLES WHERE TABLE_NAME = 'orders' ORDER BY ENGINE asc;
+---------------+--------------+------------+------------+--------+---------+------------+------------+----------------+-------------+-----------------+--------------+-----------+----------------+---------------------+---------------------+------------+--------------------+----------+----------------+---------------+
| TABLE_CATALOG | TABLE_SCHEMA | TABLE_NAME | TABLE_TYPE | ENGINE | VERSION | ROW_FORMAT | TABLE_ROWS | AVG_ROW_LENGTH | DATA_LENGTH | MAX_DATA_LENGTH | INDEX_LENGTH | DATA_FREE | AUTO_INCREMENT | CREATE_TIME         | UPDATE_TIME         | CHECK_TIME | TABLE_COLLATION    | CHECKSUM | CREATE_OPTIONS | TABLE_COMMENT |
+---------------+--------------+------------+------------+--------+---------+------------+------------+----------------+-------------+-----------------+--------------+-----------+----------------+---------------------+---------------------+------------+--------------------+----------+----------------+---------------+
| def           | test_db      | orders     | BASE TABLE | MyISAM |      10 | Dynamic    |          5 |           3276 |       16384 |               0 |            0 |         0 |              6 | 2022-06-12 01:22:32 | 2022-06-05 19:17:41 | NULL       | utf8mb4_0900_ai_ci |     NULL |                |               |
+---------------+--------------+------------+------------+--------+---------+------------+------------+----------------+-------------+-----------------+--------------+-----------+----------------+---------------------+---------------------+------------+--------------------+----------+----------------+---------------+
1 row in set (0.01 sec)

mysql> 

```


- на `InnoDB`

```bash

mysql> use test_db;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> ALTER TABLE orders ENGINE = MyISAM;
Query OK, 5 rows affected (0.14 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM information_schema.TABLES WHERE TABLE_NAME = 'orders' ORDER BY ENGINE asc;
+---------------+--------------+------------+------------+--------+---------+------------+------------+----------------+-------------+-----------------+--------------+-----------+----------------+---------------------+---------------------+------------+--------------------+----------+----------------+---------------+
| TABLE_CATALOG | TABLE_SCHEMA | TABLE_NAME | TABLE_TYPE | ENGINE | VERSION | ROW_FORMAT | TABLE_ROWS | AVG_ROW_LENGTH | DATA_LENGTH | MAX_DATA_LENGTH | INDEX_LENGTH | DATA_FREE | AUTO_INCREMENT | CREATE_TIME         | UPDATE_TIME         | CHECK_TIME | TABLE_COLLATION    | CHECKSUM | CREATE_OPTIONS | TABLE_COMMENT |
+---------------+--------------+------------+------------+--------+---------+------------+------------+----------------+-------------+-----------------+--------------+-----------+----------------+---------------------+---------------------+------------+--------------------+----------+----------------+---------------+
| def           | test_db      | orders     | BASE TABLE | MyISAM |      10 | Dynamic    |          5 |           3276 |       16384 |               0 |            0 |         0 |              6 | 2022-06-12 01:22:32 | 2022-06-05 19:17:41 | NULL       | utf8mb4_0900_ai_ci |     NULL |                |               |
+---------------+--------------+------------+------------+--------+---------+------------+------------+----------------+-------------+-----------------+--------------+-----------+----------------+---------------------+---------------------+------------+--------------------+----------+----------------+---------------+
1 row in set (0.01 sec)

mysql> 

```



## Задача 4 

Изучите файл `my.cnf` в директории /etc/mysql.

Измените его согласно ТЗ (движок InnoDB):
- Скорость IO важнее сохранности данных
- Нужна компрессия таблиц для экономии места на диске
- Размер буффера с незакомиченными транзакциями 1 Мб
- Буффер кеширования 30% от ОЗУ

```bash

root@dev1-10:~# free -mh
               total        used        free      shared  buff/cache   available
Mem:           3.8Gi       2.2Gi       346Mi        16Mi       1.2Gi       1.3Gi
Swap:          4.0Gi       560Mi       3.4Gi
root@dev1-10:~# docker exec -it mysql-virt-03 /bin/bash
```

- Размер файла логов операций 100 Мб



Приведите в ответе измененный файл `my.cnf`.

```bash
root@51fb1512bfc9:/# echo -e "\n[mysqld]\n\ninnodb-flush-method=O_DSYNC\n\ninnodb_file_per_table=ON\n\ninnodb-log-buffer-size=1048576\n\ninnodb_buffer_pool_chunk_size=128000000\ninnodb-buffer-pool-instances=9\ninnodb-buffer-pool-size=1152000000\n" > /etc/mysql/conf.d/mysql.cnf
root@51fb1512bfc9:/# cat /etc/mysql/conf.d/mysql.cnf 

[mysqld]

innodb-flush-method=O_DSYNC

innodb_file_per_table=ON

innodb-log-buffer-size=1048576

innodb_buffer_pool_chunk_size=128000000
innodb-buffer-pool-instances=9
innodb-buffer-pool-size=1152000000

root@51fb1512bfc9:/# 

```

```bash

mysql> SELECT @@innodb-buffer-pool-size;
ERROR 1193 (HY000): Unknown system variable 'innodb'
mysql> SELECT @@innodb_buffer_pool_size;
+---------------------------+
| @@innodb_buffer_pool_size |
+---------------------------+
|                 134217728 |
+---------------------------+
1 row in set (0.00 sec)

mysql> exit


root@dev1-10:~# docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED      STATUS      PORTS                 NAMES
51fb1512bfc9   mysql     "docker-entrypoint.s…"   6 days ago   Up 6 days   3306/tcp, 33060/tcp   mysql-virt-03
root@dev1-10:~# 
root@dev1-10:~# docker restart  mysql-virt-03
mysql-virt-03
root@dev1-10:~# docker exec -it mysql-virt-03 /bin/bash
root@51fb1512bfc9:/# mysql -u root -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 8.0.29 MySQL Community Server - GPL

Copyright (c) 2000, 2022, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> SELECT @@innodb_buffer_pool_size;
+---------------------------+
| @@innodb_buffer_pool_size |
+---------------------------+
|                1151336448 |
+---------------------------+
1 row in set (0.00 sec)

mysql> 

```

---

### Как оформить ДЗ?

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
