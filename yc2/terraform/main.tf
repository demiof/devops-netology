provider "yandex" {
  token     = "../../yc/src/terraform/key.json"
  cloud_id  = "${var.yandex_cloud_id}"
  folder_id = "${var.yandex_folder_id}"
  zone      = "${var.yandex_vpc_network}"
}


#resource "yandex_compute_image" "my-ubuntu-amd64" {
#  name       = "my-ubuntu-amd64"
#  source_url = "https://packages.debian.org/sid/linux-image-amd64"
#  source_url = "https://releases.ubuntu.com/20.04/ubuntu-20.04.4-live-server-amd64.iso"
#  image_id = "${var.centos-7-base}"
#  source_url = "${var.ubuntu-srv-amd64}"
#}
