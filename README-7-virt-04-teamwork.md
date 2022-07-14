# Домашнее задание к занятию "7.4. Средства командной работы над инфраструктурой."

## Задача 1. Настроить terraform cloud (необязательно, но крайне желательно).

В это задании предлагается познакомиться со средством командой работы над инфраструктурой предоставляемым
разработчиками терраформа. 

1. Зарегистрируйтесь на [https://app.terraform.io/](https://app.terraform.io/).
(регистрация бесплатная и не требует использования платежных инструментов).
1. Создайте в своем github аккаунте (или другом хранилище репозиториев) отдельный репозиторий с
 конфигурационными файлами прошлых занятий (или воспользуйтесь любым простым конфигом).
1. Зарегистрируйте этот репозиторий в [https://app.terraform.io/](https://app.terraform.io/).
1. Выполните plan и apply. 

В качестве результата задания приложите снимок экрана с успешным применением конфигурации.

```bash

root@dev1-10:~/netol_do/test-for-app-terraform/yc-states-backends/terraform# terraform apply
Running apply in Terraform Cloud. Output will stream here. Pressing Ctrl-C
will cancel the remote apply if it's still pending. If the apply started it
will stop streaming the logs, but will not stop the apply running remotely.

Preparing the remote apply...

To view this run in a browser, visit:
https://app.terraform.io/app/demiof/test/runs/run-MJtiQ2MNJhsorJUa

Waiting for the plan to start...

Terraform v1.2.4
on linux_amd64
Initializing plugins and modules...
yandex_vpc_subnet.default: Refreshing state... [id=e2lkg9vdhpe9vng8ne4g]
yandex_vpc_network.default: Refreshing state... [id=enpllvl1bj4m93jr0chb]

Terraform used the selected providers to generate the following execution
plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # yandex_compute_instance.main["first_vm_for_test"] will be created
  + resource "yandex_compute_instance" "main" {
      + created_at                = (known after apply)
      + folder_id                 = (known after apply)
      + fqdn                      = (known after apply)
      + hostname                  = (known after apply)
      + id                        = (known after apply)
      + network_acceleration_type = "standard"
      + platform_id               = "standard-v1"
      + service_account_id        = (known after apply)
      + status                    = (known after apply)
      + zone                      = (known after apply)

      + boot_disk {
          + auto_delete = true
          + device_name = (known after apply)
          + disk_id     = (known after apply)
          + mode        = (known after apply)

          + initialize_params {
              + block_size  = (known after apply)
              + description = (known after apply)
              + image_id    = "fd8q7cikvj0mggcs886d"
              + name        = (known after apply)
              + size        = (known after apply)
              + snapshot_id = (known after apply)
              + type        = "network-hdd"
            }
        }

      + network_interface {
          + index              = (known after apply)
          + ip_address         = (known after apply)
          + ipv4               = true
          + ipv6               = (known after apply)
          + ipv6_address       = (known after apply)
          + mac_address        = (known after apply)
          + nat                = true
          + nat_ip_address     = (known after apply)
          + nat_ip_version     = (known after apply)
          + security_group_ids = (known after apply)
          + subnet_id          = "e2lclbkvfe9r5bd6m89g"
        }

      + placement_policy {
          + host_affinity_rules = (known after apply)
          + placement_group_id  = (known after apply)
        }

      + resources {
          + core_fraction = 100
          + cores         = 2
          + memory        = 2
        }

      + scheduling_policy {
          + preemptible = (known after apply)
        }
    }

  # yandex_compute_instance.main["second_vm_for_test"] will be created
  + resource "yandex_compute_instance" "main" {
      + created_at                = (known after apply)
      + folder_id                 = (known after apply)
      + fqdn                      = (known after apply)
      + hostname                  = (known after apply)
      + id                        = (known after apply)
      + network_acceleration_type = "standard"
      + platform_id               = "standard-v1"
      + service_account_id        = (known after apply)
      + status                    = (known after apply)
      + zone                      = (known after apply)

      + boot_disk {
          + auto_delete = true
          + device_name = (known after apply)
          + disk_id     = (known after apply)
          + mode        = (known after apply)

          + initialize_params {
              + block_size  = (known after apply)
              + description = (known after apply)
              + image_id    = "fd8q7cikvj0mggcs886d"
              + name        = (known after apply)
              + size        = (known after apply)
              + snapshot_id = (known after apply)
              + type        = "network-hdd"
            }
        }

      + network_interface {
          + index              = (known after apply)
          + ip_address         = (known after apply)
          + ipv4               = true
          + ipv6               = (known after apply)
          + ipv6_address       = (known after apply)
          + mac_address        = (known after apply)
          + nat                = true
          + nat_ip_address     = (known after apply)
          + nat_ip_version     = (known after apply)
          + security_group_ids = (known after apply)
          + subnet_id          = "e2lclbkvfe9r5bd6m89g"
        }

      + placement_policy {
          + host_affinity_rules = (known after apply)
          + placement_group_id  = (known after apply)
        }

      + resources {
          + core_fraction = 100
          + cores         = 2
          + memory        = 2
        }

      + scheduling_policy {
          + preemptible = (known after apply)
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.


Do you want to perform these actions in workspace "test"?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

yandex_compute_instance.main["second_vm_for_test"]: Creating...
yandex_compute_instance.main["first_vm_for_test"]: Creating...
yandex_compute_instance.main["second_vm_for_test"]: Still creating... [10s elapsed]
yandex_compute_instance.main["first_vm_for_test"]: Still creating... [10s elapsed]
yandex_compute_instance.main["second_vm_for_test"]: Still creating... [20s elapsed]
yandex_compute_instance.main["first_vm_for_test"]: Still creating... [20s elapsed]
yandex_compute_instance.main["second_vm_for_test"]: Still creating... [30s elapsed]
yandex_compute_instance.main["first_vm_for_test"]: Still creating... [30s elapsed]
yandex_compute_instance.main["second_vm_for_test"]: Still creating... [40s elapsed]
yandex_compute_instance.main["first_vm_for_test"]: Still creating... [40s elapsed]
yandex_compute_instance.main["second_vm_for_test"]: Still creating... [50s elapsed]
yandex_compute_instance.main["first_vm_for_test"]: Still creating... [50s elapsed]
yandex_compute_instance.main["second_vm_for_test"]: Still creating... [1m0s elapsed]
yandex_compute_instance.main["first_vm_for_test"]: Still creating... [1m0s elapsed]
yandex_compute_instance.main["second_vm_for_test"]: Still creating... [1m10s elapsed]
yandex_compute_instance.main["first_vm_for_test"]: Still creating... [1m10s elapsed]
yandex_compute_instance.main["second_vm_for_test"]: Still creating... [1m20s elapsed]
yandex_compute_instance.main["first_vm_for_test"]: Still creating... [1m20s elapsed]
yandex_compute_instance.main["second_vm_for_test"]: Still creating... [1m30s elapsed]
yandex_compute_instance.main["first_vm_for_test"]: Still creating... [1m30s elapsed]
yandex_compute_instance.main["second_vm_for_test"]: Still creating... [1m40s elapsed]
yandex_compute_instance.main["first_vm_for_test"]: Still creating... [1m40s elapsed]
yandex_compute_instance.main["second_vm_for_test"]: Still creating... [1m50s elapsed]
yandex_compute_instance.main["first_vm_for_test"]: Still creating... [1m50s elapsed]
yandex_compute_instance.main["second_vm_for_test"]: Still creating... [2m0s elapsed]
yandex_compute_instance.main["first_vm_for_test"]: Still creating... [2m0s elapsed]
yandex_compute_instance.main["first_vm_for_test"]: Creation complete after 2m2s [id=epdqvk5rv295uts6ccas]
yandex_compute_instance.main["second_vm_for_test"]: Creation complete after 2m4s [id=epdrni005gimdqjfj7dv]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.

Outputs:

yc_cloud_id = "b1gtlo6uqrvrdckscbg8"
yc_folder_id = "b1g7jkg3844vv1nn5r1a"
yc_v4_cidr_blocks = [
  "192.168.101.0/24",
]
yc_vpc_network = "enpbsku8oecgd8qfvc84"
yc_zone = "ru-central1-b"
root@dev1-10:~/netol_do/test-for-app-terraform/yc-states-backends/terraform# 

```

## Задача 2. Написать серверный конфиг для атлантиса. 

Смысл задания – познакомиться с документацией 
о [серверной](https://www.runatlantis.io/docs/server-side-repo-config.html) конфигурации и конфигурации уровня 
 [репозитория](https://www.runatlantis.io/docs/repo-level-atlantis-yaml.html).

Создай `server.yaml` который скажет атлантису:
1. Укажите, что атлантис должен работать только для репозиториев в вашем github (или любом другом) аккаунте.
1. На стороне клиентского конфига разрешите изменять `workflow`, то есть для каждого репозитория можно 
будет указать свои дополнительные команды. 
1. В `workflow` используемом по-умолчанию сделайте так, что бы во время планирования не происходил `lock` состояния.

Создай `atlantis.yaml` который, если поместить в корень terraform проекта, скажет атлантису:
1. Надо запускать планирование и аплай для двух воркспейсов `stage` и `prod`.
1. Необходимо включить автопланирование при изменении любых файлов `*.tf`.

В качестве результата приложите ссылку на файлы `server.yaml` и `atlantis.yaml`.

## Задача 3. Знакомство с каталогом модулей. 

1. В [каталоге модулей](https://registry.terraform.io/browse/modules) найдите официальный модуль от aws для создания
`ec2` инстансов. 
2. Изучите как устроен модуль. Задумайтесь, будете ли в своем проекте использовать этот модуль или непосредственно 
ресурс `aws_instance` без помощи модуля?
3. В рамках предпоследнего задания был создан ec2 при помощи ресурса `aws_instance`. 
Создайте аналогичный инстанс при помощи найденного модуля.   

В качестве результата задания приложите ссылку на созданный блок конфигураций. 

---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
