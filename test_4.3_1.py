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

