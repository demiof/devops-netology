#!/usr/bin/env python3

import os

bash_command = ["cd /home/demi/netol_do/devops-netology", "git status --porcelain --ignored -uno "]
result_os = os.popen(' && '.join(bash_command)).read()
    

is_change = False

        
for result in result_os.split('\n'):

    if result.find('AM',0,2) != -1:
        prepare_result = result.replace('AM ', 'Добавлен/Изменен_файл/переменная: ')
        print(prepare_result)

    elif result.find('M',0,2) != -1:
        prepare_result = result.replace('M ', 'Изменен_файл/переменная: ')
        print(prepare_result)

    elif result.find('A',0,2) != -1:
        prepare_result = result.replace('A ', 'Добавлен_файл/переменная: ')
        print(prepare_result)

    else: break
    
    b=prepare_result.split(' ')
    if b != '':
        print('Путь местонахождения: ')
        bash_2='realpath '+b[-1]
        os.system(bash_2)
        print('---------------------------------------')
