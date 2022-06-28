#!/usr/bin/env python3

import os
import sys
import time

A = sys.argv
if len(A) <= 1: 
    print('\nPlease use: Path (str) to Repository where search updates!\n')
    sys.exit()
elif type(A[1])==str:
    check_path=os.path.exists(A[1])
    if check_path:
        print('\nPath exists!\n')
        check_path=os.path.exists(A[1]+'/.git')
        if check_path==False:
            print('This is not git Repository! Please, choose another one!\n');
            sys.exit()
    else:
        print('Path or file does not exist!\n')
        sys.exit()
else: 
    print('Wrong argument type!\n')
    sys.exit()

bash_command = ["cd /home/demi/netol_do/devops-netology", "git status --porcelain --ignored -uno "]
result_os = os.popen(' && '.join(bash_command)).read()
    

from alive_progress import alive_bar

l = len(result_os.split('\n'))-1
mylist=range(0,l,1)

#print(list(mylist))

P="\n\nРезультаты поиска в "+A[1]+":\n\n---------------------------------------\n"

with alive_bar(l) as bar:
        
    for result in result_os.split('\n'):


        if result.find('AM',0,2) != -1:
            prepare_result = result.replace('AM ', 'Добавлен/Изменен_файл/переменная: ')
            P=P+prepare_result+'\n'

        elif result.find('M',0,2) != -1:
            prepare_result = result.replace('M ', 'Изменен_файл/переменная: ')
            P=P+prepare_result+'\n'

        elif result.find('A',0,2) != -1:
            prepare_result = result.replace('A ', 'Добавлен_файл/переменная: ')
            P=P+prepare_result+'\n'
        

        else: break
        
        b=prepare_result.split(' ')
        if b != '':
            P=P+'Путь местонахождения: \n'
            bash_2='realpath '+b[-1]
            bash_2_res=os.popen(bash_2).read()
    #        print(bash_2_res)
            P=P+bash_2_res+'\n'
            P=P+'---------------------------------------\n'

        bar()
        time.sleep(1)

print(P)
