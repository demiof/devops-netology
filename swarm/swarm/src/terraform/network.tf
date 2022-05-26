# Network
resource "yandex_vpc_network" "default" {
  name = "net-swarm"
}

resource "yandex_vpc_subnet" "default" {
  name = "subnet-swarm"
  zone           = "ru-central1-b"
  network_id     = "${yandex_vpc_network.default.id}"
  v4_cidr_blocks = ["192.168.102.0/24"]
}
