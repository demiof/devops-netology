# Описание кода - playbook для ansible:
## Общее описание:
> В данном файле описывается скрипт на языке ansible выполняющий деплой виртуальных машин заданного кол-ва и необходимой конфигурации с использоваинем ansible, модуля ansible community.general.proxmox_kvm и др., кластера на proxmox.
# Структура
> Скрипт поделен логические на разделы, которые можно вызвать с помощью пакета ansible-playbook, указав после опции -t (tags) в необходимом наборе:
* Checking if VMs exists `vms_check`
* Cloning VMs `vms_clon`
* Creating VMs `vms_creating`
* Configuring VMs `vms_conf`
* Starting VMs `vms_start`
* Downloading `*_get`
* Installing & configuring `*_conf`
* Starting `*_start`
> Для того, чтобы проиграть (выполнить) любой из разделов кода, при необходимости используем следующие теги, которые относятся к одному из развертываемых сервисов, из списка:
* VMs - создание шаблона виртуальных машин (колонирование/создание и деплой виртуальных машин)
* Elasticsearch - деплой сервиса Elasticsearch, заданной версии и платформы
* Kibana - деплой сервиса Kiabana, заданной версии и платформы 
> Теги построены из префикса и суффикса, соединенными символом \'_\', в суффиксе содержится имя сервиса, в префиксе - имя действия, например:
* vms_check - проверяется существуют ли виртуальные машины из inventory
* vms_clon - клогирование виртуальной(ых) машин(ы) из ранее созданного шаблона
* vms_creating - создание виртуальной(ых) машин(ы) по указанным атрибутам к модулю community.general.proxmox
* vms_conf - конфигурирование созданных/склонированной(ых) виртуальной(ых) машин(ы)
* vms_start - запуск виртуальной(ых) машин(ы)
* elastic_get - получение дистрибутивов, с автоматическим установлением vpn соединения
* kibana_get
* jvm_install - распаковка дистрибутивов
* elastic_install
* kibana_install
* jvm_conf - конфигурирование дистрибутивов
* elastic_conf
* kibana_conf
* elastic_start - запуск сервисов
* kibana_start
# Используемые модули:
* community.general.proxmox
* community.general.proxmox_kvm
* ansible.builtin.copy
* ansible.builtin.shell
* ansible.builtin.get_url
* ansible.builtin.copy
* ansible.builtin.user
* ansible.builtin.group
* ansible.builtin.file
* ansible.builtin.unarchive
* ansible.builtin.template
* ansible.builtin.command
* ansible.builtin.systemd
# Обратить внимание:
> Особенно, на порядок использование блоков разделов кода с помощью использования тегов - недопускать нелогичной последовательности, например, использование раздела конфигурирования до создаиния, или заполнения переменных
> В переменных group_vars прописать версию пакетов, параметры шаблона(ов) и т.д.
> Переменные так же используются в inventory 
> В случае, если виртальная(ые) машина(ы) создана(ы) код клонирования/создания будет пропущен по условию (существует проверка в блоки кода с тегом vms_check).
...
