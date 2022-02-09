# Домашнее задание к занятию "3.5. Файловые системы"

1. Узнайте о [sparse](https://ru.wikipedia.org/wiki/%D0%A0%D0%B0%D0%B7%D1%80%D0%B5%D0%B6%D1%91%D0%BD%D0%BD%D1%8B%D0%B9_%D1%84%D0%B0%D0%B9%D0%BB) (разряженных) файлах.

> Разряженный файл -  файл, в котором последовательности нулевых байтов заменены на информацию об этих последовательностях (список дыр). Дыра (англ. hole) — последовательность нулевых байт внутри файла, не записанная на диск. Информация о дырах (смещение от начала файла в байтах и количество байт) хранится в метаданных ФС.
> Преимущества: 
* экономия дискового пространства. Использование разрежённых файлов считается одним из способов сжатия данных на уровне файловой системы;
* отсутствие временных затрат на запись нулевых байт;
* увеличение срока службы запоминающих устройств.
> Недостатки:
* накладные расходы на работу со списком дыр;
* фрагментация файла при частой записи данных в дыры;
* невозможность записи данных в дыры при отсутствии свободного места на диске;
* невозможность использования других индикаторов дыр, кроме нулевых байт.

> Для реализации поддержки разрежённых файлов требуются:

* возможность записи метаданных в ФС;
* поддержка со стороны системного и прикладного ПО.

> Следующие ФС поддерживают разрежённые файлы: BTRFS, NILFS, ZFS, NTFS[2], ext2, ext3, ext4, XFS, JFS, ReiserFS, Reiser4, UFS, Rock Ridge, UDF, ReFS, APFS, F2FS.

> Создание разряженного файла:

```bash

dd if=/dev/zero of=./sparse-file bs=1 count=0 seek=200G
# или
truncate -s200G ./sparse-file
```
> Преобразование обычного файла в разрежённый (выполнение поиска дыр и записи их расположения (смещений и длин) в метаданные файла):

```bash
cp --sparse=always ./simple-file ./sparse-file
```

> Cохранение копии диска в разрежённый файл утилитой ddrescue:


```bash
ddrescue --sparse /dev/sdb ./sparse-file ./history.log
```




> Особенности:


* При чтении из дыры возвращаются нулевые байты; обращения к диску не происходит (предполагается, что карты расположения областей уже прочитаны с диска из метаданных файла и находятся в памяти).
* При записи в дыру запускается алгоритм поиска свободного места (свободных блоков) на диске. Если блоки найдены, данные будут записаны. Зачастую найденные блоки расположены на диске далеко от блоков с уже записанным содержимым файла; это приводит к фрагментации ФС. Если место на диске закончится, алгоритм не найдёт ничего и запись не будет выполнена (write() сообщит о нехватке свободного места, а, если файл использовался с помощью mmap(), произойдёт ошибка segmentation fault).
Запись в произвольное место разрежённого файла, как правило, приводит к большой фрагментации ФС.
* Разрежённые файлы не всегда корректно копируются; при копировании файла вместо информации о дырах на диск могут быть записаны нулевые байты. Для Linux правильное копирование выполняется командой cp с ключом --sparse. Реализовать правильное копирование можно двумя способами: 1) искать области, заполненные нулевыми байтами (дыры), и выполнять seek() (вместо записи нулей с помощью write()); 2) получить карту расположения файла на диске с помощью fibmap().
* Пометить произвольную область файла как дыру позволяет системный вызов fallocate() с флагом punch hole[3] («пробить дырку»). Системный вызов не только освободит место на диске, но ещё и выполнит команду TRIM у SSD-дисков для блоков указанной области.
* Так как адресация в большинстве ФС осуществляется с помощью блоков[4], то смещение и размер дыр не могут быть произвольными, а должны быть кратны размеру блока (выровнены по размеру блока). Размер блока постоянен для одного раздела. Таким образом, нельзя сделать «дыру» в пару байт; при такой попытке драйвер ФС запишет на диск нулевые байты.
* Утилиты для отображения размера файла обычно выводят реальный размер файла (в байтах) и размер, занимаемый файлом на диске (в блоках ФС[4] или байтах). Разрежённый файл может занимать меньше места на диске.
* Обратите внимание, что системный вызов fallocate() с флагом 0 выделяет блоки под файл и помечает их, как «заполненные нулевыми байтами». Это позволяет почти мгновенно создать большой файл без записи нулевых байтов на диск. Отличие от разрежённых файлов заключается в резервировании блоков; блоки под файл выделяются сразу; при записи в блок флаг «заполнен нулевыми байтами» снимается; если на диске закончится свободное место, при записи в область, содержащую нулевые байты, ошибки не возникнет. Команда TRIM у SSD-дисков вызывается и для этого случая.








 


2. Могут ли файлы, являющиеся жесткой ссылкой на один объект, иметь разные права доступа и владельца? Почему?



> Нет. Права относятся к сущности, которая уникально определяется с пом. inum. У файла однозначно определяемом с помощью inum может быть сколько угодно hardlinks и область на диске он будет занимать пока суествует последний hardlink.




> Ниже видим количество hardlinks (2) на файл test c inode 145698
```bash
root@dev1-10:/home/demi/netol_do/devops-netology# stat test
  File: test
  Size: 0               Blocks: 0          IO Block: 4096   regular empty file
Device: fe04h/65028d    Inode: 145698      Links: 2
Access: (0644/-rw-r--r--)  Uid: (    0/    root)   Gid: (    0/    root)
Access: 2022-02-08 06:35:36.728952322 +0300
Modify: 2022-01-26 11:17:53.881299611 +0300
Change: 2022-02-08 06:33:37.777315964 +0300
 Birth: 2022-01-19 11:07:03.849400841 +0300
root@dev1-10:/home/demi/netol_do/devops-netology# find ./ -inum 145698
./test
./test_hard_link
root@dev1-10:/home/demi/netol_do/devops-netology# 
```
> Пробуем еще:

```bash
root@dev1-10:/home/demi/netol_do/devops-netology# stat ./test_1_2.sh
  File: ./test_1_2.sh
  Size: 66              Blocks: 8          IO Block: 4096   regular file
Device: fe04h/65028d    Inode: 145727      Links: 1
Access: (0755/-rwxr-xr-x)  Uid: (    0/    root)   Gid: (    0/    root)
Access: 2022-01-28 11:38:18.112554935 +0300
Modify: 2022-01-21 22:12:15.525891646 +0300
Change: 2022-01-21 22:12:15.613891410 +0300
 Birth: 2022-01-21 22:12:15.525891646 +0300
root@dev1-10:/home/demi/netol_do/devops-netology# find / -inum 145727
^C
root@dev1-10:/home/demi/netol_do/devops-netology# find ./ -inum 145727
./test_1_2.sh
root@dev1-10:/home/demi/netol_do/devops-netology# find /root -inum 145727
^C
root@dev1-10:/home/demi/netol_do/devops-netology# find ./ -inum 145727
./test_1_2.sh
root@dev1-10:/home/demi/netol_do/devops-netology# ls -lah -inum 145727
ls: cannot access '145727': No such file or directory
root@dev1-10:/home/demi/netol_do/devops-netology# ls -lah ./test_1_2.sh
-rwxr-xr-x 1 root root 66 Jan 21 22:12 ./test_1_2.sh
root@dev1-10:/home/demi/netol_do/devops-netology# ln ./test_1_2.sh test_1_2.sh_hard_link
root@dev1-10:/home/demi/netol_do/devops-netology# ls -lah test_1_2.sh_hard_link
-rwxr-xr-x 2 root root 66 Jan 21 22:12 test_1_2.sh_hard_link
root@dev1-10:/home/demi/netol_do/devops-netology# stat ./test_1_2.sh
  File: ./test_1_2.sh
  Size: 66              Blocks: 8          IO Block: 4096   regular file
Device: fe04h/65028d    Inode: 145727      Links: 2
Access: (0755/-rwxr-xr-x)  Uid: (    0/    root)   Gid: (    0/    root)
Access: 2022-01-28 11:38:18.112554935 +0300
Modify: 2022-01-21 22:12:15.525891646 +0300
Change: 2022-02-08 06:47:04.422855473 +0300
 Birth: 2022-01-21 22:12:15.525891646 +0300
root@dev1-10:/home/demi/netol_do/devops-netology# 

```
3. Сделайте `vagrant destroy` на имеющийся инстанс Ubuntu. Замените содержимое Vagrantfile следующим:

    ```bash
    Vagrant.configure("2") do |config|
      config.vm.box = "bento/ubuntu-20.04"
      config.vm.provider :virtualbox do |vb|
        lvm_experiments_disk0_path = "/tmp/lvm_experiments_disk0.vmdk"
        lvm_experiments_disk1_path = "/tmp/lvm_experiments_disk1.vmdk"
        vb.customize ['createmedium', '--filename', lvm_experiments_disk0_path, '--size', 2560]
        vb.customize ['createmedium', '--filename', lvm_experiments_disk1_path, '--size', 2560]
        vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 1, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk0_path]
        vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 2, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk1_path]
      end
    end
    ```

    Данная конфигурация создаст новую виртуальную машину с двумя дополнительными неразмеченными дисками по 2.5 Гб.


```bash

PS C:\Users\demi\VirtualBox VMs\Vagrant> cat .\Vagrantfile
Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"
  config.vm.provider :virtualbox do |vb|
    lvm_experiments_disk0_path = "/tmp/lvm_experiments_disk0.vmdk"
    lvm_experiments_disk1_path = "/tmp/lvm_experiments_disk1.vmdk"
    vb.customize ['createmedium', '--filename', lvm_experiments_disk0_path, '--size', 2560]
    vb.customize ['createmedium', '--filename', lvm_experiments_disk1_path, '--size', 2560]
    vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 1, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk0_path]
    vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 2, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk1_path]
  end
end
PS C:\Users\demi\VirtualBox VMs\Vagrant> vagrant up
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Importing base box 'bento/ubuntu-20.04'...
==> default: Matching MAC address for NAT networking...
==> default: Checking if box 'bento/ubuntu-20.04' version '202112.19.0' is up to date...
==> default: Setting the name of the VM: Vagrant_default_1644337478550_37101
==> default: Clearing any previously set network interfaces...
==> default: Preparing network interfaces based on configuration...
    default: Adapter 1: nat
==> default: Forwarding ports...
    default: 22 (guest) => 2222 (host) (adapter 1)
==> default: Running 'pre-boot' VM customizations...
==> default: Booting VM...
==> default: Waiting for machine to boot. This may take a few minutes...
    default: SSH address: 127.0.0.1:2222
    default: SSH username: vagrant
    default: SSH auth method: private key
    default:
    default: Vagrant insecure key detected. Vagrant will automatically replace
    default: this with a newly generated keypair for better security.
    default:
    default: Inserting generated public key within guest...
    default: Removing insecure key from the guest if it's present...
    default: Key inserted! Disconnecting and reconnecting using new SSH key...
==> default: Machine booted and ready!
==> default: Checking for guest additions in VM...
==> default: Mounting shared folders...
    default: /vagrant => C:/Users/demi/VirtualBox VMs/Vagrant
PS C:\Users\demi\VirtualBox VMs\Vagrant> vagrant destroy
    default: Are you sure you want to destroy the 'default' VM? [y/N] y
==> default: Forcing shutdown of VM...
==> default: Destroying VM and associated drives...
PS C:\Users\demi\VirtualBox VMs\Vagrant> vagrant up
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Importing base box 'bento/ubuntu-20.04'...
==> default: Matching MAC address for NAT networking...
==> default: Checking if box 'bento/ubuntu-20.04' version '202112.19.0' is up to date...
==> default: Setting the name of the VM: Vagrant_default_1644338054559_30305
==> default: Clearing any previously set network interfaces...
==> default: Preparing network interfaces based on configuration...
    default: Adapter 1: nat
==> default: Forwarding ports...
    default: 22 (guest) => 2222 (host) (adapter 1)
==> default: Running 'pre-boot' VM customizations...
==> default: Booting VM...
==> default: Waiting for machine to boot. This may take a few minutes...
    default: SSH address: 127.0.0.1:2222
    default: SSH username: vagrant
    default: SSH auth method: private key
    default: Warning: Remote connection disconnect. Retrying...
    default: Warning: Connection aborted. Retrying...
    default:
    default: Vagrant insecure key detected. Vagrant will automatically replace
    default: this with a newly generated keypair for better security.
    default:
    default: Inserting generated public key within guest...
    default: Removing insecure key from the guest if it's present...
    default: Key inserted! Disconnecting and reconnecting using new SSH key...
==> default: Machine booted and ready!
==> default: Checking for guest additions in VM...
==> default: Mounting shared folders...
    default: /vagrant => C:/Users/demi/VirtualBox VMs/Vagrant
PS C:\Users\demi\VirtualBox VMs\Vagrant> cat .\Vagrantfile
Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"
  config.vm.provider :virtualbox do |vb|
    lvm_experiments_disk0_path = "/tmp/lvm_experiments_disk0.vmdk"
    lvm_experiments_disk1_path = "/tmp/lvm_experiments_disk1.vmdk"
    vb.customize ['createmedium', '--filename', lvm_experiments_disk0_path, '--size', 2560]
    vb.customize ['createmedium', '--filename', lvm_experiments_disk1_path, '--size', 2560]
    vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 1, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk0_path]
    vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 2, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk1_path]
  end
end
PS C:\Users\demi\VirtualBox VMs\Vagrant>




```


4. Используя `fdisk`, разбейте первый диск на 2 раздела: 2 Гб, оставшееся пространство.


```bash




Command (m for help): p
Disk /dev/sdb: 2.51 GiB, 2684354560 bytes, 5242880 sectors
Disk model: VBOX HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xd6a1c0d5

Device     Boot   Start     End Sectors  Size Id Type
/dev/sdb1          2048 5242879 5240832  2.5G  5 Extended
/dev/sdb5          4096 4198399 4194304    2G 83 Linux
/dev/sdb6       4200448 5242879 1042432  509M 83 Linux

Command (m for help): 




vagrant@vagrant:~$ lsblk
NAME                      MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
loop0                       7:0    0 70.3M  1 loop /snap/lxd/21029
loop1                       7:1    0 32.3M  1 loop /snap/snapd/12704
loop2                       7:2    0 55.4M  1 loop /snap/core18/2128
loop3                       7:3    0 43.4M  1 loop /snap/snapd/14549
loop4                       7:4    0 55.5M  1 loop /snap/core18/2284
loop5                       7:5    0 61.9M  1 loop /snap/core20/1328
loop6                       7:6    0 67.2M  1 loop /snap/lxd/21835
sda                         8:0    0   64G  0 disk 
├─sda1                      8:1    0    1M  0 part 
├─sda2                      8:2    0    1G  0 part /boot
└─sda3                      8:3    0   63G  0 part 
  └─ubuntu--vg-ubuntu--lv 253:0    0 31.5G  0 lvm  /
sdb                         8:16   0  2.5G  0 disk 
├─sdb1                      8:17   0    1K  0 part 
├─sdb5                      8:21   0    2G  0 part 
└─sdb6                      8:22   0  509M  0 part 
sdc                         8:32   0  2.5G  0 disk 
vagrant@vagrant:~$ 


```


5. Используя `sfdisk`, перенесите данную таблицу разделов на второй диск.


```bash


vagrant@vagrant:~$ lsblk
NAME                      MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
loop0                       7:0    0 70.3M  1 loop /snap/lxd/21029
loop1                       7:1    0 32.3M  1 loop /snap/snapd/12704
loop2                       7:2    0 55.4M  1 loop /snap/core18/2128
loop3                       7:3    0 43.4M  1 loop /snap/snapd/14549
loop4                       7:4    0 55.5M  1 loop /snap/core18/2284
loop5                       7:5    0 61.9M  1 loop /snap/core20/1328
loop6                       7:6    0 67.2M  1 loop /snap/lxd/21835
sda                         8:0    0   64G  0 disk 
├─sda1                      8:1    0    1M  0 part 
├─sda2                      8:2    0    1G  0 part /boot
└─sda3                      8:3    0   63G  0 part 
  └─ubuntu--vg-ubuntu--lv 253:0    0 31.5G  0 lvm  /
sdb                         8:16   0  2.5G  0 disk 
├─sdb1                      8:17   0    1K  0 part 
├─sdb5                      8:21   0    2G  0 part 
└─sdb6                      8:22   0  509M  0 part 
sdc                         8:32   0  2.5G  0 disk 
vagrant@vagrant:~$ sfdisk -l /dev/sdb
sfdisk: cannot open /dev/sdb: Permission denied
vagrant@vagrant:~$ sudo sfdisk -l /dev/sdb
Disk /dev/sdb: 2.51 GiB, 2684354560 bytes, 5242880 sectors
Disk model: VBOX HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xd6a1c0d5

Device     Boot   Start     End Sectors  Size Id Type
/dev/sdb1          2048 5242879 5240832  2.5G  5 Extended
/dev/sdb5          4096 4198399 4194304    2G 83 Linux
/dev/sdb6       4200448 5242879 1042432  509M 83 Linux
vagrant@vagrant:~$ 
vagrant@vagrant:~$ pwd
/home/vagrant
vagrant@vagrant:~$ sudo sfdisk --dump /dev/sdb > sdb.dump
vagrant@vagrant:~$ tail sdb.dump 
label: dos
label-id: 0xd6a1c0d5
device: /dev/sdb
unit: sectors

/dev/sdb1 : start=        2048, size=     5240832, type=5
/dev/sdb5 : start=        4096, size=     4194304, type=83
/dev/sdb6 : start=     4200448, size=     1042432, type=83
vagrant@vagrant:~$ sudo sfdisk -l /dev/sdc
Disk /dev/sdc: 2.51 GiB, 2684354560 bytes, 5242880 sectors
Disk model: VBOX HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
vagrant@vagrant:~$ sudo sfdisk /dev/sdc < sdb.dump 
Checking that no-one is using this disk right now ... OK

Disk /dev/sdc: 2.51 GiB, 2684354560 bytes, 5242880 sectors
Disk model: VBOX HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes

>>> Script header accepted.
>>> Script header accepted.
>>> Script header accepted.
>>> Script header accepted.
>>> Created a new DOS disklabel with disk identifier 0xd6a1c0d5.
/dev/sdc1: Created a new partition 1 of type 'Extended' and of size 2.5 GiB.
/dev/sdc2: Created a new partition 5 of type 'Linux' and of size 2 GiB.
/dev/sdc6: Created a new partition 6 of type 'Linux' and of size 509 MiB.
/dev/sdc7: Done.

New situation:
Disklabel type: dos
Disk identifier: 0xd6a1c0d5

Device     Boot   Start     End Sectors  Size Id Type
/dev/sdc1          2048 5242879 5240832  2.5G  5 Extended
/dev/sdc5          4096 4198399 4194304    2G 83 Linux
/dev/sdc6       4200448 5242879 1042432  509M 83 Linux

The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.
vagrant@vagrant:~$ sudo sfdisk -l /dev/sdc
Disk /dev/sdc: 2.51 GiB, 2684354560 bytes, 5242880 sectors
Disk model: VBOX HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0xd6a1c0d5

Device     Boot   Start     End Sectors  Size Id Type
/dev/sdc1          2048 5242879 5240832  2.5G  5 Extended
/dev/sdc5          4096 4198399 4194304    2G 83 Linux
/dev/sdc6       4200448 5242879 1042432  509M 83 Linux
vagrant@vagrant:~$ lsblk
NAME                      MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
loop0                       7:0    0 70.3M  1 loop /snap/lxd/21029
loop1                       7:1    0 32.3M  1 loop /snap/snapd/12704
loop2                       7:2    0 55.4M  1 loop /snap/core18/2128
loop3                       7:3    0 43.4M  1 loop /snap/snapd/14549
loop4                       7:4    0 55.5M  1 loop /snap/core18/2284
loop5                       7:5    0 61.9M  1 loop /snap/core20/1328
loop6                       7:6    0 67.2M  1 loop /snap/lxd/21835
sda                         8:0    0   64G  0 disk 
├─sda1                      8:1    0    1M  0 part 
├─sda2                      8:2    0    1G  0 part /boot
└─sda3                      8:3    0   63G  0 part 
  └─ubuntu--vg-ubuntu--lv 253:0    0 31.5G  0 lvm  /
sdb                         8:16   0  2.5G  0 disk 
├─sdb1                      8:17   0    1K  0 part 
├─sdb5                      8:21   0    2G  0 part 
└─sdb6                      8:22   0  509M  0 part 
sdc                         8:32   0  2.5G  0 disk 
├─sdc1                      8:33   0    1K  0 part 
├─sdc5                      8:37   0    2G  0 part 
└─sdc6                      8:38   0  509M  0 part 
vagrant@vagrant:~$ 


```



6. Соберите `mdadm` RAID1 на паре разделов 2 Гб.


```bash

vagrant@vagrant:~$ sudo mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sd[bc]5
mdadm: Note: this array has metadata at the start and
    may not be suitable as a boot device.  If you plan to
    store '/boot' on this device please ensure that
    your boot-loader understands md/v1.x metadata, or use
    --metadata=0.90
Continue creating array? n   
mdadm: create aborted.
vagrant@vagrant:~$ sudo mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sd[bc]5 --metadata=0.90
mdadm: array /dev/md0 started.
vagrant@vagrant:~$ lsblk /dev/md0
NAME MAJ:MIN RM SIZE RO TYPE  MOUNTPOINT
md0    9:0    0   2G  0 raid1 

```


7. Соберите `mdadm` RAID0 на второй паре маленьких разделов.



```bash


vagrant@vagrant:~$ lsblk /dev/sd*
NAME                      MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sda                         8:0    0   64G  0 disk  
├─sda1                      8:1    0    1M  0 part  
├─sda2                      8:2    0    1G  0 part  /boot
└─sda3                      8:3    0   63G  0 part  
  └─ubuntu--vg-ubuntu--lv 253:0    0 31.5G  0 lvm   /
sda1                        8:1    0    1M  0 part  
sda2                        8:2    0    1G  0 part  /boot
sda3                        8:3    0   63G  0 part  
└─ubuntu--vg-ubuntu--lv   253:0    0 31.5G  0 lvm   /
sdb                         8:16   0  2.5G  0 disk  
├─sdb1                      8:17   0    1K  0 part  
├─sdb5                      8:21   0    2G  0 part  
│ └─md0                     9:0    0    2G  0 raid1 
└─sdb6                      8:22   0  509M  0 part  
sdb1                        8:17   0    1K  0 part  
sdb5                        8:21   0    2G  0 part  
└─md0                       9:0    0    2G  0 raid1 
sdb6                        8:22   0  509M  0 part  
sdc                         8:32   0  2.5G  0 disk  
├─sdc1                      8:33   0    1K  0 part  
├─sdc5                      8:37   0    2G  0 part  
│ └─md0                     9:0    0    2G  0 raid1 
└─sdc6                      8:38   0  509M  0 part  
sdc1                        8:33   0    1K  0 part  
sdc5                        8:37   0    2G  0 part  
└─md0                       9:0    0    2G  0 raid1 
sdc6                        8:38   0  509M  0 part  
vagrant@vagrant:~$ sudo mdadm --create /dev/md1 --level=0 --raid-devices=2 /dev/sd[bc]6
mdadm: Defaulting to version 1.2 metadata
mdadm: array /dev/md1 started.
vagrant@vagrant:~$ lsblk /dev/sd*6
NAME  MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sdb6    8:22   0  509M  0 part  
└─md1   9:1    0 1014M  0 raid0 
sdc6    8:38   0  509M  0 part  
└─md1   9:1    0 1014M  0 raid0 
vagrant@vagrant:~$ 

```





8. Создайте 2 независимых PV на получившихся md-устройствах.






```bash

vagrant@vagrant:~$ sudo pvcreate /dev/md0
  Physical volume "/dev/md0" successfully created.
vagrant@vagrant:~$ 
vagrant@vagrant:~$ sudo pvcreate /dev/md1
  Physical volume "/dev/md1" successfully created.
vagrant@vagrant:~$ sudo pvs
  PV         VG        Fmt  Attr PSize    PFree   
  /dev/md0             lvm2 ---    <2.00g   <2.00g
  /dev/md1             lvm2 ---  1014.00m 1014.00m
  /dev/sda3  ubuntu-vg lvm2 a--   <63.00g  <31.50g
vagrant@vagrant:~$ 

```



9. Создайте общую volume-group на этих двух PV.



```bash

vagrant@vagrant:~$ sudo vgcreate vg01 /dev/md0 /dev/md1
  Volume group "vg01" successfully created
vagrant@vagrant:~$ 
vagrant@vagrant:~$ 
vagrant@vagrant:~$ sudo vgs
  VG        #PV #LV #SN Attr   VSize   VFree  
  ubuntu-vg   1   1   0 wz--n- <63.00g <31.50g
  vg01        2   0   0 wz--n-   2.98g   2.98g
vagrant@vagrant:~$ 

```



10. Создайте LV размером 100 Мб, указав его расположение на PV с RAID0.

```bash

vagrant@vagrant:~$ sudo vgs
  VG        #PV #LV #SN Attr   VSize   VFree  
  ubuntu-vg   1   1   0 wz--n- <63.00g <31.50g
  vg01        2   0   0 wz--n-   2.98g   2.98g
vagrant@vagrant:~$ sudo lvcreate -L 100m --name lv_md1 /dev/md1
  Volume group "md1" not found
  Cannot process volume group md1
vagrant@vagrant:~$ sudo lvcreate -L 100m -n lv_md1 vg01 /dev/md1
  Logical volume "lv_md1" created.
vagrant@vagrant:~$ sudo lvs
  LV        VG        Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  ubuntu-lv ubuntu-vg -wi-ao----  31.50g                                                    
  lv_md1    vg01      -wi-a----- 100.00m                                                    
vagrant@vagrant:~$ sudo lvdisplay
  --- Logical volume ---
  LV Path                /dev/ubuntu-vg/ubuntu-lv
  LV Name                ubuntu-lv
  VG Name                ubuntu-vg
  LV UUID                ftN15m-3lML-YH5x-R5P2-kLCd-kzW3-32dlqO
  LV Write Access        read/write
  LV Creation host, time ubuntu-server, 2021-12-19 19:37:44 +0000
  LV Status              available
  # open                 1
  LV Size                31.50 GiB
  Current LE             8064
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:0
   
  --- Logical volume ---
  LV Path                /dev/vg01/lv_md1
  LV Name                lv_md1
  VG Name                vg01
  LV UUID                hYri5N-XAfq-Vu6M-8Fjq-X9tb-0vcP-b5BVQe
  LV Write Access        read/write
  LV Creation host, time vagrant, 2022-02-09 06:29:55 +0000
  LV Status              available
  # open                 0
  LV Size                100.00 MiB
  Current LE             25
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     4096
  Block device           253:1

```





11. Создайте `mkfs.ext4` ФС на получившемся LV.





```bash

vagrant@vagrant:~$ sudo mkfs.ext4 /dev/vg01/lv_md1 
mke2fs 1.45.5 (07-Jan-2020)
Creating filesystem with 25600 4k blocks and 25600 inodes

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (1024 blocks): done
Writing superblocks and filesystem accounting information: done

vagrant@vagrant:~$ 

```




12. Смонтируйте этот раздел в любую директорию, например, `/tmp/new`.


```bash

vagrant@vagrant:~$ mkdir /tmp/new

vagrant@vagrant:~$ ls -la /tmp/new
total 8
drwxrwxr-x  2 vagrant vagrant 4096 Feb  9 06:37 .
drwxrwxrwt 12 root    root    4096 Feb  9 06:37 ..
vagrant@vagrant:~$ 
vagrant@vagrant:~$ mount /dev/vg01/lv_md1 /tmp/new/
mount: only root can do that
vagrant@vagrant:~$ sudo mount /dev/vg01/lv_md1 /tmp/new/
vagrant@vagrant:~$ ls -la /tmp/new/
total 24
drwxr-xr-x  3 root root  4096 Feb  9 06:36 .
drwxrwxrwt 12 root root  4096 Feb  9 06:37 ..
drwx------  2 root root 16384 Feb  9 06:36 lost+found
vagrant@vagrant:~$ 

```




13. Поместите туда тестовый файл, например `wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz`.




```bash

vagrant@vagrant:~$ sudo wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz
--2022-02-09 06:41:18--  https://mirror.yandex.ru/ubuntu/ls-lR.gz
Resolving mirror.yandex.ru (mirror.yandex.ru)... 213.180.204.183, 2a02:6b8::183
Connecting to mirror.yandex.ru (mirror.yandex.ru)|213.180.204.183|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 22293140 (21M) [application/octet-stream]
Saving to: ‘/tmp/new/test.gz’

/tmp/new/test.gz                         100%[==================================================================================>]  21.26M  5.90MB/s    in 4.2s    

2022-02-09 06:41:22 (5.11 MB/s) - ‘/tmp/new/test.gz’ saved [22293140/22293140]

vagrant@vagrant:~$ ls -la /tmp/new/
total 21796
drwxr-xr-x  3 root root     4096 Feb  9 06:41 .
drwxrwxrwt 12 root root     4096 Feb  9 06:37 ..
drwx------  2 root root    16384 Feb  9 06:36 lost+found
-rw-r--r--  1 root root 22293140 Feb  9 02:34 test.gz
vagrant@vagrant:~$ 

```



14. Прикрепите вывод `lsblk`.




```bash

vagrant@vagrant:~$ lsblk
NAME                      MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
loop0                       7:0    0 70.3M  1 loop  /snap/lxd/21029
loop1                       7:1    0 32.3M  1 loop  /snap/snapd/12704
loop2                       7:2    0 55.4M  1 loop  /snap/core18/2128
loop3                       7:3    0 43.4M  1 loop  /snap/snapd/14549
loop4                       7:4    0 55.5M  1 loop  /snap/core18/2284
loop5                       7:5    0 61.9M  1 loop  /snap/core20/1328
loop6                       7:6    0 67.2M  1 loop  /snap/lxd/21835
sda                         8:0    0   64G  0 disk  
├─sda1                      8:1    0    1M  0 part  
├─sda2                      8:2    0    1G  0 part  /boot
└─sda3                      8:3    0   63G  0 part  
  └─ubuntu--vg-ubuntu--lv 253:0    0 31.5G  0 lvm   /
sdb                         8:16   0  2.5G  0 disk  
├─sdb1                      8:17   0    1K  0 part  
├─sdb5                      8:21   0    2G  0 part  
│ └─md0                     9:0    0    2G  0 raid1 
└─sdb6                      8:22   0  509M  0 part  
  └─md1                     9:1    0 1014M  0 raid0 
    └─vg01-lv_md1         253:1    0  100M  0 lvm   /tmp/new
sdc                         8:32   0  2.5G  0 disk  
├─sdc1                      8:33   0    1K  0 part  
├─sdc5                      8:37   0    2G  0 part  
│ └─md0                     9:0    0    2G  0 raid1 
└─sdc6                      8:38   0  509M  0 part  
  └─md1                     9:1    0 1014M  0 raid0 
    └─vg01-lv_md1         253:1    0  100M  0 lvm   /tmp/new
vagrant@vagrant:~$ 



```


15. Протестируйте целостность файла:

    ```bash
    root@vagrant:~# gzip -t /tmp/new/test.gz
    root@vagrant:~# echo $?
    0
    ```


```bash

vagrant@vagrant:~$ gzip -t /tmp/new/
lost+found/ test.gz     
vagrant@vagrant:~$ gzip -t /tmp/new/test.gz 
vagrant@vagrant:~$ echo $?
0
vagrant@vagrant:~$ 

```






16. Используя pvmove, переместите содержимое PV с RAID0 на RAID1.



```bash

vagrant@vagrant:~$ sudo pvs
  PV         VG        Fmt  Attr PSize    PFree  
  /dev/md0   vg01      lvm2 a--    <2.00g  <2.00g
  /dev/md1   vg01      lvm2 a--  1012.00m 912.00m
  /dev/sda3  ubuntu-vg lvm2 a--   <63.00g <31.50g
vagrant@vagrant:~$ sudo pvmove /dev/md1 /dev/md0
  /dev/md1: Moved: 72.00%
  /dev/md1: Moved: 100.00%
vagrant@vagrant:~$ sudo pvdisplay
  --- Physical volume ---
  PV Name               /dev/sda3
  VG Name               ubuntu-vg
  PV Size               <63.00 GiB / not usable 0   
  Allocatable           yes 
  PE Size               4.00 MiB
  Total PE              16127
  Free PE               8063
  Allocated PE          8064
  PV UUID               sDUvKe-EtCc-gKuY-ZXTD-1B1d-eh9Q-XldxLf
   
  --- Physical volume ---
  PV Name               /dev/md0
  VG Name               vg01
  PV Size               <2.00 GiB / not usable <3.94 MiB
  Allocatable           yes 
  PE Size               4.00 MiB
  Total PE              511
  Free PE               486
  Allocated PE          25
  PV UUID               QyFbXq-ZzRq-IVtz-xuBs-vt0g-hCYT-dfsFdx
   
  --- Physical volume ---
  PV Name               /dev/md1
  VG Name               vg01
  PV Size               1014.00 MiB / not usable 2.00 MiB
  Allocatable           yes 
  PE Size               4.00 MiB
  Total PE              253
  Free PE               253
  Allocated PE          0
  PV UUID               1KHoDg-sTBq-RyBj-5VLQ-AaCe-Du7M-8NSKHS
   
vagrant@vagrant:~$


```


17. Сделайте `--fail` на устройство в вашем RAID1 md.







```bash


vagrant@vagrant:~$ sudo mdadm /dev/md0 --fail /dev/sdc5 
mdadm: set /dev/sdc5 faulty in /dev/md0
vagrant@vagrant:~$ cat /proc/mdstat 
Personalities : [linear] [multipath] [raid0] [raid1] [raid6] [raid5] [raid4] [raid10] 
md1 : active raid0 sdc6[1] sdb6[0]
      1038336 blocks super 1.2 512k chunks
      
md0 : active raid1 sdc5[2](F) sdb5[0]
      2097088 blocks [2/1] [U_]
      
unused devices: <none>
vagrant@vagrant:~$ sudo mdadm --detail /dev/md0
/dev/md0:
           Version : 0.90
     Creation Time : Wed Feb  9 05:15:33 2022
        Raid Level : raid1
        Array Size : 2097088 (2047.94 MiB 2147.42 MB)
     Used Dev Size : 2097088 (2047.94 MiB 2147.42 MB)
      Raid Devices : 2
     Total Devices : 2
   Preferred Minor : 0
       Persistence : Superblock is persistent

       Update Time : Wed Feb  9 07:19:37 2022
             State : clean, degraded 
    Active Devices : 1
   Working Devices : 1
    Failed Devices : 1
     Spare Devices : 0

Consistency Policy : resync

              UUID : d22e6b8d:c446bbfd:88e93fb0:875bd5f8 (local to host vagrant)
            Events : 0.20

    Number   Major   Minor   RaidDevice State
       0       8       21        0      active sync   /dev/sdb5
       -       0        0        1      removed

       2       8       37        -      faulty   /dev/sdc5
vagrant@vagrant:~$ 



```















18. Подтвердите выводом `dmesg`, что RAID1 работает в деградированном состоянии.


```bash

vagrant@vagrant:~$ sudo dmesg -TH --level crit,err
[Feb 9 07:19] md/raid1:md0: Disk failure on sdc5, disabling device.
              md/raid1:md0: Operation continuing on 1 devices.
vagrant@vagrant:~$ 

```
19. Протестируйте целостность файла, несмотря на "сбойный" диск он должен продолжать быть доступен:

    ```bash
    root@vagrant:~# gzip -t /tmp/new/test.gz
    root@vagrant:~# echo $?
    0
    ```


```bash

vagrant@vagrant:~$ gzip -t /tmp/new/test.gz 
vagrant@vagrant:~$ echo $?
0
vagrant@vagrant:~$ 
```



20. Погасите тестовый хост, `vagrant destroy`.


```bash
PS C:\Users\demi\VirtualBox VMs\Vagrant> vagrant destroy
    default: Are you sure you want to destroy the 'default' VM? [y/N] y
==> default: Forcing shutdown of VM...
==> default: Destroying VM and associated drives...
PS C:\Users\demi\VirtualBox VMs\Vagrant>

```








 
 ---

## Как сдавать задания

Обязательными к выполнению являются задачи без указания звездочки. Их выполнение необходимо для получения зачета и диплома о профессиональной переподготовке.

Задачи со звездочкой (*) являются дополнительными задачами и/или задачами повышенной сложности. Они не являются обязательными к выполнению, но помогут вам глубже понять тему.

Домашнее задание выполните в файле readme.md в github репозитории. В личном кабинете отправьте на проверку ссылку на .md-файл в вашем репозитории.

Также вы можете выполнить задание в [Google Docs](https://docs.google.com/document/u/0/?tgif=d) и отправить в личном кабинете на проверку ссылку на ваш документ.
Название файла Google Docs должно содержать номер лекции и фамилию студента. Пример названия: "1.1. Введение в DevOps — Сусанна Алиева".

Если необходимо прикрепить дополнительные ссылки, просто добавьте их в свой Google Docs.

Перед тем как выслать ссылку, убедитесь, что ее содержимое не является приватным (открыто на комментирование всем, у кого есть ссылка), иначе преподаватель не сможет проверить работу. Чтобы это проверить, откройте ссылку в браузере в режиме инкогнито.

[Как предоставить доступ к файлам и папкам на Google Диске](https://support.google.com/docs/answer/2494822?hl=ru&co=GENIE.Platform%3DDesktop)

[Как запустить chrome в режиме инкогнито ](https://support.google.com/chrome/answer/95464?co=GENIE.Platform%3DDesktop&hl=ru)

[Как запустить  Safari в режиме инкогнито ](https://support.apple.com/ru-ru/guide/safari/ibrw1069/mac)

Любые вопросы по решению задач задавайте в чате Slack.

---
