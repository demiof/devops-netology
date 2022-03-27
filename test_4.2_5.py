#!/usr/bin/env python3

import os
import sys
import subprocess as sp


# Модель разработки - Магистральная

master_branch_name = 'main'

# Определяем имя репозитория, проверяем в его ли папке и сущ-е .git

A = sys.argv
if len(A) <= 1: 
    print('\nNO Arguments given! Need remote name\nType -h,--help for help...\n')
    sys.exit()
elif A[1]=='-h' or A[1]=='--help':
    print('\nUse {this program name} {remote name}, execute in repo dir!\n')
    sys.exit()
elif type(A[1])==str:
    
    remote_name=A[1]
    repo_name_cmd="basename -s .git `git config --get remote."+remote_name+".url`"
    repo_name=sp.getoutput(repo_name_cmd)

    check_path=os.path.exists('../'+repo_name)
    if check_path:
        print('\nGit repo dir of remote= \"'+remote_name+'\" exists!\n')
        check_path=os.path.exists('./.git')
        if check_path==False:
            print('This is not git repository! Please, choose another one!\n');
            sys.exit()
        elif repo_name=='':
            print('/nFailed to get repo name!/n')
        else:
            print('Repo name is '+str(repo_name) )
    else:
        print('Git repo path/file of remote= \"'+remote_name+'\" does not exist!\n')
        sys.exit()
else: 
    print('Wrong argument type!\n')
    sys.exit()


#bash_command = ["git pull ", "git status --porcelain --ignored -uno "]
#result_os = os.popen(' && '.join(bash_command)).read()


#перенос изменений с сервера в локальный репозиторий

bash_command = ["git pull "+remote_name+" "+master_branch_name]
result_os = os.popen(' && '.join(bash_command)).read()



#создать новую ветку
#закомитить в ней изменения
#создать PR для вливания текущей ветки в main (с собщением из первого параметра скрипта)
#замерджить с main
#если веток, кроме main более 3 - удалить

