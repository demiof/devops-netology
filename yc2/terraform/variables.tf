# Заменить на ID своего облака
# https://console.cloud.yandex.ru/cloud?section=overview
variable "yandex_cloud_id" {
  default = "b1gtlo6uqrvrdckscbg8"
}

# Заменить на Folder своего облака
# https://console.cloud.yandex.ru/cloud?section=overview
variable "yandex_folder_id" {
  default = "b1g7jkg3844vv1nn5r1a"
}

variable "yandex_zone" {
  default = "ru-central1-b" 
}

variable "yandex_vpc_network" {
  default = "e2lclbkvfe9r5bd6m89g"
}

variable "yandex_v4_cidr_blocks" {
  default = [ "192.168.101.0/24", ]
}

# Заменить на ID своего образа
# ID можно узнать с помощью команды yc compute image list
variable "centos-7-base" {
  default = "fd8dib4t4ekaijvk09rp"
}

# url c img ubuntu 20.04.4 server amd64
variable "ubuntu-srv-amd64" {
  default = "https://releases.ubuntu.com/20.04/ubuntu-20.04.4-live-server-amd64.iso"
}
