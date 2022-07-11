# Домашнее задание к занятию "7.3. Основы и принцип работы Терраформ"

## Задача 1. Создадим бэкэнд в S3 (необязательно, но крайне желательно).

Если в рамках предыдущего задания у вас уже есть аккаунт AWS, то давайте продолжим знакомство со взаимодействием
терраформа и aws. 

1. Создайте s3 бакет, iam роль и пользователя от которого будет работать терраформ. Можно создать отдельного пользователя,
а можно использовать созданного в рамках предыдущего задания, просто добавьте ему необходимы права, как описано 
[здесь](https://www.terraform.io/docs/backends/types/s3.html).
1. Зарегистрируйте бэкэнд в терраформ проекте как описано по ссылке выше. 


## Задача 2. Инициализируем проект и создаем воркспейсы. 

1. Выполните `terraform init`:
    * если был создан бэкэнд в S3, то терраформ создат файл стейтов в S3 и запись в таблице 
dynamodb.
    * иначе будет создан локальный файл со стейтами.  
1. Создайте два воркспейса `stage` и `prod`.
1. В уже созданный `aws_instance` добавьте зависимость типа инстанса от вокспейса, что бы в разных ворскспейсах 
использовались разные `instance_type`.
1. Добавим `count`. Для `stage` должен создаться один экземпляр `ec2`, а для `prod` два. 

```bash

root@dev1-10:~/netol_do/yc-states-backends/terraform# terraform workspace list
  default
* prod
  stage

root@dev1-10:~/netol_do/yc-states-backends/terraform# terraform plan

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following
symbols:
  + create

Terraform will perform the following actions:

  # yandex_compute_instance.main[0] will be created
  + resource "yandex_compute_instance" "main" {
      + created_at                = (known after apply)
      + folder_id                 = (known after apply)
      + fqdn                      = (known after apply)
      + hostname                  = (known after apply)
      + id                        = (known after apply)
      + metadata                  = {
          + "ssh-keys" = <<-EOT
                ubuntu:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC/EBW4EvwnnNwWdOQ1j6YIOWB3vva9eirTQVKrRCytfctp9ywoprD4HyLUAY5nWwlepkD3JtMDQEsuPEZpm6ehqOX5oteK4NZ8Jp6aPwQLIyK5g2QetxJxnEHMpXW2nymnNBAen/2tX2c65rAVn0k7sDAY34+IerZaVKU1PKF2DjkK845CZRbYoIOnCjPZVGu4uIzlPMTPgPWTMP4qjIuq3kgnJsOBpTRIf7OpDKSKXKuKRfE/eILlBONPpRtFxkLZwmBw1B3KsNjbeAguIbkMgOoUmdzvxffcPR0Wsu0me52NQJ4srgVL5QTXGgUSLgoTv1L30fFi0jqFVwZVTCWF root@dev1
            EOT
        }
      + name                      = "vm-for-prod"
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

  # yandex_compute_instance.main[1] will be created
  + resource "yandex_compute_instance" "main" {
      + created_at                = (known after apply)
      + folder_id                 = (known after apply)
      + fqdn                      = (known after apply)
      + hostname                  = (known after apply)
      + id                        = (known after apply)
      + metadata                  = {
          + "ssh-keys" = <<-EOT
                ubuntu:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC/EBW4EvwnnNwWdOQ1j6YIOWB3vva9eirTQVKrRCytfctp9ywoprD4HyLUAY5nWwlepkD3JtMDQEsuPEZpm6ehqOX5oteK4NZ8Jp6aPwQLIyK5g2QetxJxnEHMpXW2nymnNBAen/2tX2c65rAVn0k7sDAY34+IerZaVKU1PKF2DjkK845CZRbYoIOnCjPZVGu4uIzlPMTPgPWTMP4qjIuq3kgnJsOBpTRIf7OpDKSKXKuKRfE/eILlBONPpRtFxkLZwmBw1B3KsNjbeAguIbkMgOoUmdzvxffcPR0Wsu0me52NQJ4srgVL5QTXGgUSLgoTv1L30fFi0jqFVwZVTCWF root@dev1
            EOT
        }
      + name                      = "vm-for-prod"
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

  # yandex_vpc_network.default will be created
  + resource "yandex_vpc_network" "default" {
      + created_at                = (known after apply)
      + default_security_group_id = (known after apply)
      + folder_id                 = (known after apply)
      + id                        = (known after apply)
      + labels                    = (known after apply)
      + name                      = "net"
      + subnet_ids                = (known after apply)
    }

  # yandex_vpc_subnet.default will be created
  + resource "yandex_vpc_subnet" "default" {
      + created_at     = (known after apply)
      + folder_id      = (known after apply)
      + id             = (known after apply)
      + labels         = (known after apply)
      + name           = "subnet"
      + network_id     = (known after apply)
      + v4_cidr_blocks = [
          + "192.168.101.0/24",
        ]
      + v6_cidr_blocks = (known after apply)
      + zone           = "ru-central1-b"
    }

Plan: 4 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + yc_cloud_id       = "b1gtlo6uqrvrdckscbg8"
  + yc_folder_id      = "b1g7jkg3844vv1nn5r1a"
  + yc_v4_cidr_blocks = [
      + "192.168.101.0/24",
    ]
  + yc_vpc_network    = "e2lclbkvfe9r5bd6m89g"
  + yc_zone           = "ru-central1-b"

───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

Note: You didn't use the -out option to save this plan, so Terraform can't guarantee to take exactly these actions if you run
"terraform apply" now.
root@dev1-10:~/netol_do/yc-states-backends/terraform# 


```


1. Создайте рядом еще один `aws_instance`, но теперь определите их количество при помощи `for_each`, а не `count`.
1. Что бы при изменении типа инстанса не возникло ситуации, когда не будет ни одного инстанса добавьте параметр
жизненного цикла `create_before_destroy = true` в один из рессурсов `aws_instance`.
1. При желании поэкспериментируйте с другими параметрами и рессурсами.

В виде результата работы пришлите:
* Вывод команды `terraform workspace list`.
* Вывод команды `terraform plan` для воркспейса `prod`.  

```bash

root@dev1-10:~/netol_do/yc-states-backends/terraform# terraform validate
Success! The configuration is valid.

root@dev1-10:~/netol_do/yc-states-backends/terraform# terraform workspace list
  default
* prod
  stage

```

```bash

root@dev1-10:~/netol_do/yc-states-backends/terraform# terraform apply
yandex_vpc_network.default: Refreshing state... [id=enpllvl1bj4m93jr0chb]
yandex_compute_instance.main["first_vm_for_prod"]: Refreshing state... [id=epdhbu9ahpvmjcfiflqo]
yandex_vpc_subnet.default: Refreshing state... [id=e2l9vngkh1botnhk19pb]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following
symbols:
  + create
  ~ update in-place

Terraform will perform the following actions:

  # yandex_compute_instance.main["first_vm_for_prod"] will be updated in-place
  ~ resource "yandex_compute_instance" "main" {
        id                        = "epdhbu9ahpvmjcfiflqo"
      - name                      = "vm-for-prod" -> null
        # (10 unchanged attributes hidden)





        # (5 unchanged blocks hidden)
    }

  # yandex_compute_instance.main["second_vm_for_prod"] will be created
  + resource "yandex_compute_instance" "main" {
      + created_at                = (known after apply)
      + folder_id                 = (known after apply)
      + fqdn                      = (known after apply)
      + hostname                  = (known after apply)
      + id                        = (known after apply)
      + metadata                  = {
          + "ssh-keys" = <<-EOT
                ubuntu:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC/EBW4EvwnnNwWdOQ1j6YIOWB3vva9eirTQVKrRCytfctp9ywoprD4HyLUAY5nWwlepkD3JtMDQEsuPEZpm6ehqOX5oteK4NZ8Jp6aPwQLIyK5g2QetxJxnEHMpXW2nymnNBAen/2tX2c65rAVn0k7sDAY34+IerZaVKU1PKF2DjkK845CZRbYoIOnCjPZVGu4uIzlPMTPgPWTMP4qjIuq3kgnJsOBpTRIf7OpDKSKXKuKRfE/eILlBONPpRtFxkLZwmBw1B3KsNjbeAguIbkMgOoUmdzvxffcPR0Wsu0me52NQJ4srgVL5QTXGgUSLgoTv1L30fFi0jqFVwZVTCWF root@dev1
            EOT
        }
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

Plan: 1 to add, 1 to change, 0 to destroy.

Do you want to perform these actions in workspace "prod"?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

yandex_compute_instance.main["second_vm_for_prod"]: Creating...
yandex_compute_instance.main["first_vm_for_prod"]: Modifying... [id=epdhbu9ahpvmjcfiflqo]
yandex_compute_instance.main["first_vm_for_prod"]: Modifications complete after 6s [id=epdhbu9ahpvmjcfiflqo]
yandex_compute_instance.main["second_vm_for_prod"]: Still creating... [10s elapsed]
yandex_compute_instance.main["second_vm_for_prod"]: Still creating... [20s elapsed]
yandex_compute_instance.main["second_vm_for_prod"]: Still creating... [30s elapsed]
yandex_compute_instance.main["second_vm_for_prod"]: Creation complete after 34s [id=epd3vbd3ejh5dslhiq0g]

Apply complete! Resources: 1 added, 1 changed, 0 destroyed.

Outputs:

yc_cloud_id = "b1gtlo6uqrvrdckscbg8"
yc_folder_id = "b1g7jkg3844vv1nn5r1a"
yc_v4_cidr_blocks = [
  "192.168.101.0/24",
]
yc_vpc_network = "enpbsku8oecgd8qfvc84"
yc_zone = "ru-central1-b"
root@dev1-10:~/netol_do/yc-states-backends/terraform# 

```

```bash

{
  "builders": [
    {
      "type":      "yandex",
      "token":     "${TF_VAR_token}",
      "folder_id": "${TF_VAR_folder_id}",
      "zone":      "ru-central1-b",

      "image_name":        "debian-9-nginx-{{isotime | clean_resource_name}}",
      "image_family":      "debian-web-server",
      "image_description": "my custom debian with nginx",

      "source_image_family": "debian-9",
      "subnet_id":           "${TF_VAR_vpc_subnet}",
      "use_ipv4_nat":        true,
      "disk_type":           "network-ssd",
      "ssh_username":        "debian"
    }
  ],
  "provisioners": [
    {
      "type": "shell",
      "inline": [
        "echo 'updating APT'",
        "sudo apt-get update -y",
        "sudo apt-get install -y nginx",
        "sudo su -",
        "sudo systemctl enable nginx.service",
        "curl localhost"
      ]
    }
  ]
} 

```

---

### Как cдавать задание

Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.

---
