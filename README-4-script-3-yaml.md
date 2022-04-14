### Как сдавать задания

Вы уже изучили блок «Системы управления версиями», и начиная с этого занятия все ваши работы будут приниматься ссылками на .md-файлы, размещённые в вашем публичном репозитории.

Скопируйте в свой .md-файл содержимое этого файла; исходники можно посмотреть [здесь](https://raw.githubusercontent.com/netology-code/sysadm-homeworks/devsys10/04-script-03-yaml/README.md). Заполните недостающие части документа решением задач (заменяйте `???`, ОСТАЛЬНОЕ В ШАБЛОНЕ НЕ ТРОГАЙТЕ чтобы не сломать форматирование текста, подсветку синтаксиса и прочее, иначе можно отправиться на доработку) и отправляйте на проверку. Вместо логов можно вставить скриншоты по желани.

# Домашнее задание к занятию "4.3. Языки разметки JSON и YAML"


## Обязательная задача 1
Мы выгрузили JSON, который получили через API запрос к нашему сервису:

```


{
    	"info": "Sample JSON output from our service\t",
    	"elements": [{
    			"name": "first",
    			"type": "server",
    			"ip": "7175"
    		},
    		{
    			"name": "second",
    			"type": "proxy",
    			"ip": "71.78.22.43"
    		}
    	]
    }

```

  Нужно найти и исправить все ошибки, которые допускает наш сервис

## Обязательная задача 2
В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: `{ "имя сервиса" : "его IP"}`. Формат записи YAML по одному сервису: `- имя сервиса: его IP`. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.

### Ваш скрипт:
```python



root@dev1-10:/home/demi/netol_do/devops-netology# cat test_4.3_1.py
#!/usr/bin/env python3

import os
import json
import yaml

log='last_dig_4.3_1.log'
log_err=False

#Если существует лог, прчитать структуру JSON dict из него
last_dig_json={}

if not os.access(log, os.R_OK):
    print("\nFailed to open log-file - does not exist!\n")
    log_err=True
elif os.stat(log).st_size != 0:
    with open(log) as f:
        last_dig_json = json.load(f)
else:
    print("\nFailed to open log-file - empty!\n")
    log_err=True


#Сервисы для проверки
Srvs=('drive.google.com','mail.google.com','google.com')

bash_command="dig +short  "
bash_command2=" | grep '^[.0-9]*$'"


dig_res_prn=''
dig_res=''
dig_json={}

f=open(log,'w')

for i in Srvs:

    j=os.popen(bash_command + i + bash_command2).read()
    j_split=j.split('\n')
    del j_split[-1]
    #print(j_split)

    dig_json[i]=[]

    json_inner_dict = {}
    num = 0
    for k in j_split:
        dig_res_prn=dig_res_prn+i+' - '+k+'\n'
        dig_res=dig_res+' '+k

        st1="ipv4_"+str(num)
        st2=k
        #print(st1)
        json_inner_dict.update({st1 : st2})
        num+=1
        #i=i.replace('\'','\"')
        #print(i)
        
        #ip=d.get(k)
        #ipl=dl.get(k)
        #if ip != ipl:
            #print('\n[ERROR] '+i+' IP mismath: Old ip  -> '+ip+' New ip -> '+ipl+'\n')

   
    dig_json[i].append(json_inner_dict)

#Проверка текущего резолва и резолва из лога

    d=dig_json.get(i)
    #print(d)
    
    if not log_err:
        dl=last_dig_json.get(i)
        #print(dl)

        
        for j in dig_json:

            print(j)

            if (j in last_dig_json) and (dig_json[j] != last_dig_json[j]):
                print('\n[ERROR] ip mismath: Old ip list-> '+str(last_dig_json[j])+' New ip list-> '+str(dig_json[j])+'\n')
            else:
                print('\n[OK] ips equals each other!\n')

    input('Press any key!')






st=str(dig_json)
st = st.replace('\'','\"')


#print(st)
f.write(st)


dig_res_splt=dig_res.split(' ')
del dig_res_splt[0]

print('\nWhole dictionary listing: \n')
#print(dig_res_prn)

print(dig_json)


#Преобразуемм json в yaml 

with open(r'store_file_4.3_1.yaml','w') as file:
    documents = yaml.dump(dig_json,file)



```

### Вывод скрипта при запуске при тестировании:
```
root@dev1-10:/home/demi/netol_do/devops-netology# ./test_4.3_1.py 

Failed to open log-file - does not exist!

Press any key!
Press any key!
Press any key!

Whole dictionary listing: 

{'drive.google.com': [{'ipv4_0': '142.251.1.194'}], 'mail.google.com': [{'ipv4_0': '64.233.165.19', 'ipv4_1': '64.233.165.18', 'ipv4_2': '64.233.165.83', 'ipv4_3': '64.233.165.17'}], 'google.com': [{'ipv4_0': '173.194.222.101', 'ipv4_1': '173.194.222.139', 'ipv4_2': '173.194.222.102', 'ipv4_3': '173.194.222.100', 'ipv4_4': '173.194.222.113', 'ipv4_5': '173.194.222.138'}]}

```

### json-файл(ы), который(е) записал ваш скрипт:
```json

root@dev1-10:/home/demi/netol_do/devops-netology# cat ./last_dig_4.3_1.log 
{"drive.google.com": [{"ipv4_0": "142.251.1.194"}], "mail.google.com": [{"ipv4_0": "64.233.165.19", "ipv4_1": "64.233.165.18", "ipv4_2": "64.233.165.83", "ipv4_3": "64.233.165.17"}], "google.com": [{"ipv4_0": "173.194.222.101", "ipv4_1": "173.194.222.139", "ipv4_2": "173.194.222.102", "ipv4_3": "173.194.222.100", "ipv4_4": "173.194.222.113", "ipv4_5": "173.194.222.138"}]}

```

### yml-файл(ы), который(е) записал ваш скрипт:
```yaml

root@dev1-10:/home/demi/netol_do/devops-netology# cat ./store_file_4.3_1.yaml 
drive.google.com:
- ipv4_0: 142.251.1.194
google.com:
- ipv4_0: 173.194.222.101
  ipv4_1: 173.194.222.139
  ipv4_2: 173.194.222.102
  ipv4_3: 173.194.222.100
  ipv4_4: 173.194.222.113
  ipv4_5: 173.194.222.138
mail.google.com:
- ipv4_0: 64.233.165.19
  ipv4_1: 64.233.165.18
  ipv4_2: 64.233.165.83
  ipv4_3: 64.233.165.17
root@dev1-10:/home/demi/netol_do/devops-netology# cat ./README-4-script-3-yaml.md 


```

## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так как команды в нашей компании никак не могут прийти к единому мнению о том, какой формат разметки данных использовать: JSON или YAML, нам нужно реализовать парсер из одного формата в другой. Он должен уметь:
   * Принимать на вход имя файла
   * Проверять формат исходного файла. Если файл не json или yml - скрипт должен остановить свою работу
   * Распознавать какой формат данных в файле. Считается, что файлы *.json и *.yml могут быть перепутаны
   * Перекодировать данные из исходного формата во второй доступный (из JSON в YAML, из YAML в JSON)
   * При обнаружении ошибки в исходном файле - указать в стандартном выводе строку с ошибкой синтаксиса и её номер
   * Полученный файл должен иметь имя исходного файла, разница в наименовании обеспечивается разницей расширения файлов

### Ваш скрипт:
```python

#!/bin/env python3


from decimal import InvalidContext
from pydoc import doc
from pyexpat.errors import messages
import sys
import os.path
from os.path import abspath
from typing import final
from xml.dom.minidom import Document
import yaml
import yaml.scanner
from yaml import Dumper, Loader, SafeLoader, StreamEndEvent, YAMLError, serialize, serialize_all
import json

class js_ym(yaml.YAMLObject):

    yaml_loader = SafeLoader
    yaml_dumper = Dumper
    
    
    trans_count = 0
    params = sys.argv
    file_to_check = ''
    file_to_transform = 'converted_to_json.json'
    YAML_event_structure = dict()
    YAML_token_structure = dict()
    JSON_structure = dict()
    YAML_structure = dict()

    message = ("I'm an js_ym class!",
    "\nNO Arguments given! Need remote name\nType -h,--help for help...\n",
    "\nWrong parametr type, no str!\n",
    "\nFile to convert exists!\n",
    "\nFile to convert does not exist!\n",
    f'''
    \n To much params!
    Please use: {abspath(__file__)} <path to file to convert, includes JSON or YAML structure inside>
    \n
    ''',
    f'''
    \n
    Please use: {abspath(__file__)} <path to file to convert, includes JSON or YAML structure inside>
    \n''',
    "\nUnknown params error!\n",
    )
    
    def __init__(self) -> None:
        js_ym.trans_count += 1

    
    def exclaim(self) -> None:
        print(self.message[0])
    
    def checkFExists(path) -> bool:
        if os.path.exists(path):
            return True
        else:
            return False


    @classmethod
    def checkArgs(cls) -> bool:

        if len(cls.params) <= 1:
            print(cls.message[2])
            return False
        
        elif len(cls.params) > 2:
            print(cls.message[5])
            return False
            
        elif cls.params[1]=='-h' or cls.params[1]=='--help':
            print(cls.message[6])
            return False
            
        elif type(cls.params[1])==str:
            
            if cls.checkFExists(cls.params[1]):
                print(cls.message[3])
                cls.file_to_check=cls.params[1]
                return True
            else:
                print(cls.message[4])
                return False

        else:
            print(cls.message[7])
            return False

    @classmethod
    def IfFileJson(cls, file_to_check) -> bool:
        
        try:
            with open(file_to_check,'r') as stream:
                cls.JSON_structure = json.load(stream)
        except ValueError as e:
            print('Invalid JSON!')
            return False
        else:
            print('Valid JSON!')
            return True
        finally:
            stream.close()

    @classmethod
    def IfFileYaml(cls, file_to_check) -> bool:
        
        try:
            with open(file_to_check, 'r') as stream:
                data_all = yaml.safe_load_all(stream)
                parsed_stream = yaml.parse(stream)
                scaned_stream = yaml.scan(stream, Loader=cls.yaml_loader)
                composed_stream =  yaml.compose(stream)
                #print('=====================')
                #print(stream)
                #print('=========Vgenerator_refV============')
                #print(scaned_stream)
                print('==========Vparsed eventsV============')
                for event in parsed_stream:
                    #if cls.yaml_loader.check_event(event):
                        print(event)
                    #else: 
                        #print('invalid event! -> '.event)
                print('==========Vscaned tokensV============')
                for token in scaned_stream:
                    print(token)
                print('==========Vcomposed streamV==========') 
                print(composed_stream)   
                print('=====================================')
        except ValueError as e:
            print('\nInvalid YAML\n')
            stream.close()
            sys.exit()
        except yaml.scanner.ScannerError:
            print('\nFailed while read pystream\n')
            #print(ge)
            return False
        else:
            print('\nRead pystream ok!\n')
            #cls.YAML_event_structure = parsed_stream
            cls.YAML_token_structure = scaned_stream
            return True
        finally:
            stream.close()

    @classmethod
    def TransYamlJson(cls, file_to_check, file_to_transform):
        
        try:
            with open(file_to_check, 'r') as fr:
                with open(file_to_transform, 'w') as fw:
                    cls.JSON_structure = json.dumps(yaml.load(fr,Loader=cls.yaml_loader))
                    json.dump(cls.JSON_structure,fw)
                    print("==============Vfile to transform nameV=============")
                    print(file_to_transform)
                    print("==============VTransformed JSON structureV=========")
                    print(cls.JSON_structure)
                    print("===================================================")
        except:
            print('\nFailed to transform file\n',file_to_check,'to',file_to_transform)
        else:
            print('\nTransformation succesfully!\n')
        finally:
            fw.close()
            fr.close()
    
    @classmethod
    def usage(cls):
        print("Class js_ym made ", cls.trans_count, " transformations.")


###########################################################################

if __name__ == "__main__":

    Converter = js_ym()

    if Converter.checkArgs():
        Converter.usage()
        if Converter.IfFileYaml(Converter.file_to_check):
            print('\nValid YAML!\n')
            Converter.JSON_structure = Converter.TransYamlJson(Converter.file_to_check,Converter.file_to_transform)
        elif Converter.IfFileJson(Converter.file_to_check):
            print('\nInvalid YAML!\n')
            Converter.JSON_structure = Converter.TransYamlJson(Converter.file_to_check,Converter.file_to_transform)
        else:
            print('\nUnknown file type: neither YAML, nor JSON!\n')
    else:
        print('\nBad args!\n')


```

### Пример работы скрипта:


```bash
root@dev1-10:/home/demi/netol_do/devops-netology/js_ym# ./js_ym.py non_yaml 

File to convert exists!

Class js_ym made  1  transformations.
Failed while read pystream/n
Invalid JSON!
Unknown file type: neither YAML, nor JSON!
root@dev1-10:/home/demi/netol_do/devops-netology/js_ym# ./js_ym.py non_yaml 

File to convert exists!

Class js_ym made  1  transformations.

Failed while read pystream

Invalid JSON!
Unknown file type: neither YAML, nor JSON!
root@dev1-10:/home/demi/netol_do/devops-netology/js_ym# ./js_ym.py non_yaml 

File to convert exists!

Class js_ym made  1  transformations.

Failed while read pystream

Invalid JSON!

Unknown file type: neither YAML, nor JSON!

root@dev1-10:/home/demi/netol_do/devops-netology/js_ym# ./js_ym.py test.yaml 

File to convert exists!

Class js_ym made  1  transformations.
==========Vparsed eventsV============
StreamStartEvent()
StreamEndEvent()
==========Vscaned tokensV============
StreamStartToken(encoding=None)
StreamEndToken()
==========Vcomposed streamV==========
MappingNode(tag='tag:yaml.org,2002:map', value=[(ScalarNode(tag='tag:yaml.org,2002:str', value='cloud'), MappingNode(tag='tag:yaml.org,2002:map', value=[(ScalarNode(tag='tag:yaml.org,2002:str', value='name'), ScalarNode(tag='tag:yaml.org,2002:str', value='MyCloudName')), (ScalarNode(tag='tag:yaml.org,2002:str', value='description'), ScalarNode(tag='tag:yaml.org,2002:str', value='Controller + N Compute Topology - x86 KVM')), (ScalarNode(tag='tag:yaml.org,2002:str', value='password'), ScalarNode(tag='tag:yaml.org,2002:str', value='MyCloudPassword')), (ScalarNode(tag='tag:yaml.org,2002:str', value='database_service_type'), ScalarNode(tag='tag:yaml.org,2002:str', value='db2')), (ScalarNode(tag='tag:yaml.org,2002:str', value='messaging_service_type'), ScalarNode(tag='tag:yaml.org,2002:str', value='rabbitmq')), (ScalarNode(tag='tag:yaml.org,2002:str', value='features'), MappingNode(tag='tag:yaml.org,2002:map', value=[(ScalarNode(tag='tag:yaml.org,2002:str', value='self_service_portal'), ScalarNode(tag='tag:yaml.org,2002:str', value='enabled')), (ScalarNode(tag='tag:yaml.org,2002:str', value='platform_resource_scheduler'), ScalarNode(tag='tag:yaml.org,2002:str', value='enabled'))])), (ScalarNode(tag='tag:yaml.org,2002:str', value='topology'), MappingNode(tag='tag:yaml.org,2002:map', value=[(ScalarNode(tag='tag:yaml.org,2002:str', value='database_node_name'), ScalarNode(tag='tag:yaml.org,2002:str', value='controller')), (ScalarNode(tag='tag:yaml.org,2002:str', value='controller_node_name'), ScalarNode(tag='tag:yaml.org,2002:str', value='controller')), (ScalarNode(tag='tag:yaml.org,2002:str', value='self_service_portal_node_name'), ScalarNode(tag='tag:yaml.org,2002:str', value='controller')), (ScalarNode(tag='tag:yaml.org,2002:str', value='kvm_compute_node_names'), ScalarNode(tag='tag:yaml.org,2002:str', value='kvm_compute'))]))])), (ScalarNode(tag='tag:yaml.org,2002:str', value='environment'), MappingNode(tag='tag:yaml.org,2002:map', value=[(ScalarNode(tag='tag:yaml.org,2002:str', value='base'), ScalarNode(tag='tag:yaml.org,2002:str', value='example-ibm-os-single-controller-n-compute')), (ScalarNode(tag='tag:yaml.org,2002:str', value='default_attributes'), ScalarNode(tag='tag:yaml.org,2002:null', value='')), (ScalarNode(tag='tag:yaml.org,2002:str', value='override_attributes'), ScalarNode(tag='tag:yaml.org,2002:null', value=''))])), (ScalarNode(tag='tag:yaml.org,2002:str', value='nodes'), SequenceNode(tag='tag:yaml.org,2002:seq', value=[MappingNode(tag='tag:yaml.org,2002:map', value=[(ScalarNode(tag='tag:yaml.org,2002:str', value='name'), ScalarNode(tag='tag:yaml.org,2002:str', value='controller')), (ScalarNode(tag='tag:yaml.org,2002:str', value='description'), ScalarNode(tag='tag:yaml.org,2002:str', value='Cloud controller node')), (ScalarNode(tag='tag:yaml.org,2002:str', value='fqdn'), ScalarNode(tag='tag:yaml.org,2002:str', value='controllername.company.com')), (ScalarNode(tag='tag:yaml.org,2002:str', value='password'), ScalarNode(tag='tag:yaml.org,2002:str', value='passw0rd')), (ScalarNode(tag='tag:yaml.org,2002:str', value='identity_file'), ScalarNode(tag='tag:yaml.org,2002:null', value='~')), (ScalarNode(tag='tag:yaml.org,2002:str', value='nics'), MappingNode(tag='tag:yaml.org,2002:map', value=[(ScalarNode(tag='tag:yaml.org,2002:str', value='management_network'), ScalarNode(tag='tag:yaml.org,2002:str', value='eth0')), (ScalarNode(tag='tag:yaml.org,2002:str', value='data_network'), ScalarNode(tag='tag:yaml.org,2002:str', value='eth1'))]))]), MappingNode(tag='tag:yaml.org,2002:map', value=[(ScalarNode(tag='tag:yaml.org,2002:str', value='name'), ScalarNode(tag='tag:yaml.org,2002:str', value='kvm_compute')), (ScalarNode(tag='tag:yaml.org,2002:str', value='description'), ScalarNode(tag='tag:yaml.org,2002:str', value='Cloud KVM compute node')), (ScalarNode(tag='tag:yaml.org,2002:str', value='fqdn'), ScalarNode(tag='tag:yaml.org,2002:str', value='kvmcomputename.company.com')), (ScalarNode(tag='tag:yaml.org,2002:str', value='password'), ScalarNode(tag='tag:yaml.org,2002:null', value='~')), (ScalarNode(tag='tag:yaml.org,2002:str', value='identity_file'), ScalarNode(tag='tag:yaml.org,2002:str', value='/root/identity.pem')), (ScalarNode(tag='tag:yaml.org,2002:str', value='nics'), MappingNode(tag='tag:yaml.org,2002:map', value=[(ScalarNode(tag='tag:yaml.org,2002:str', value='management_network'), ScalarNode(tag='tag:yaml.org,2002:str', value='eth0')), (ScalarNode(tag='tag:yaml.org,2002:str', value='data_network'), ScalarNode(tag='tag:yaml.org,2002:str', value='eth1'))])), (ScalarNode(tag='tag:yaml.org,2002:str', value='attribute_file'), ScalarNode(tag='tag:yaml.org,2002:null', value='~'))])]))])
=====================================

Read pystream ok!


Valid YAML!

==============Vfile to transform nameV=============
converted_to_json.json
==============VTransformed JSON structureV=========
{"cloud": {"name": "MyCloudName", "description": "Controller + N Compute Topology - x86 KVM", "password": "MyCloudPassword", "database_service_type": "db2", "messaging_service_type": "rabbitmq", "features": {"self_service_portal": "enabled", "platform_resource_scheduler": "enabled"}, "topology": {"database_node_name": "controller", "controller_node_name": "controller", "self_service_portal_node_name": "controller", "kvm_compute_node_names": "kvm_compute"}}, "environment": {"base": "example-ibm-os-single-controller-n-compute", "default_attributes": null, "override_attributes": null}, "nodes": [{"name": "controller", "description": "Cloud controller node", "fqdn": "controllername.company.com", "password": "passw0rd", "identity_file": null, "nics": {"management_network": "eth0", "data_network": "eth1"}}, {"name": "kvm_compute", "description": "Cloud KVM compute node", "fqdn": "kvmcomputename.company.com", "password": null, "identity_file": "/root/identity.pem", "nics": {"management_network": "eth0", "data_network": "eth1"}, "attribute_file": null}]}
===================================================

Transformation succesfully!

root@dev1-10:/home/demi/netol_do/devops-netology/js_ym# ./js_ym.py requirements.txt 

File to convert exists!

Class js_ym made  1  transformations.
==========Vparsed eventsV============
StreamStartEvent()
StreamEndEvent()
==========Vscaned tokensV============
StreamStartToken(encoding=None)
StreamEndToken()
==========Vcomposed streamV==========
ScalarNode(tag='tag:yaml.org,2002:str', value='pyyaml==5.3.1 jsonschema==4.4.0 pyrsistent==0.18.1')
=====================================

Read pystream ok!


Valid YAML!

==============Vfile to transform nameV=============
converted_to_json.json
==============VTransformed JSON structureV=========
"pyyaml==5.3.1 jsonschema==4.4.0 pyrsistent==0.18.1"
===================================================

Transformation succesfully!

root@dev1-10:/home/demi/netol_do/devops-netology/js_ym# ./js_ym.py requirements.txt 

File to convert exists!

Class js_ym made  1  transformations.
==========Vparsed eventsV============
StreamStartEvent()
StreamEndEvent()
==========Vscaned tokensV============
StreamStartToken(encoding=None)
StreamEndToken()
==========Vcomposed streamV==========
ScalarNode(tag='tag:yaml.org,2002:str', value='pyyaml==5.3.1 jsonschema==4.4.0 pyrsistent==0.18.1')
=====================================

Read pystream ok!


Valid YAML!

==============Vfile to transform nameV=============
converted_to_json.json
==============VTransformed JSON structureV=========
"pyyaml==5.3.1 jsonschema==4.4.0 pyrsistent==0.18.1"
===================================================

Transformation succesfully!

root@dev1-10:/home/demi/netol_do/devops-netology/js_ym# 

```
