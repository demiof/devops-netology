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
???
```

### Пример работы скрипта:
???
