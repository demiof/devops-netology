#!/usr/bin/env python3

import os
import sys
import subprocess as sp


# Модель разработки - Магистральная
login_name='demiof'
master_branch_name = 'main'
new_branch_name = 'branch_api'
PAT_name = os.environ['PAT_git_bash']
auto_commit_message = 'autocommit'

github_base_url='https://api.github.com/'


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
output = sp.getoutput(bash_command)
print(output)
#result_os = os.popen(' && '.join(bash_command)).read()

#создать новую ветку



    #получить SHA тек. объекта
#bash_cmd_sha="curl -s -H 'Authorization: token "+PAT_name+"' https://api.github.com/repos/"+login_name+"/"+repo_name+"/git/refs/heads/"+master_branch_name+" | jq -r '.object.sha'"

#output_sha = sp.getoutput(bash_cmd_sha)

#print(output_sha)

#print(bash_cmd_sha)


#bash_cmd_new_branch="curl -s -X POST -H 'Authorization: token "+PAT_name+"' \
#https://api.github.com/repos/"+login_name+"/"+repo_name+"/git/refs \
#-d '{\"ref\": \"refs/heads/"+new_branch_name+"\", \
#\"sha\": \""+output_sha+"\"}'"


#output_new_branch = sp.getoutput(bash_cmd_new_branch)


#curl -X POST -H "Authorization: token $TOKEN" \
#-d  "{\"ref\": \"refs/heads/$New_branch_name\",\"sha\": \"$SHA\"}" \ "https://api.github.com/repos/<REPO>/git/refs"


#print(bash_cmd_new_branch)

#print(output_new_branch)


bash_command = "git checkout -b  "+new_branch_name#+" --track "+remote_name+"/"+new_branch_name
output = sp.getoutput(bash_command)
print(output)
#


#закомитить в ней изменения

bash_command = "git add *"
output = sp.getoutput(bash_command)
#print(output)
#
bash_command = "git commit -m "+auto_commit_message
output = sp.getoutput(bash_command)
print(output)
#
#bash_command = "git push "+remote_name+" "+new_branch_name
#output = sp.getoutput(bash_command)
#print(output)

#создать PR для вливания текущей ветки в main (с собщением из первого параметра скрипта)


    #получить SHA тек. объекта
#bash_cmd_sha="curl -s -H 'Authorization: token "+PAT_name+"' https://api.github.com/repos/"+login_name+"/"+repo_name+"/git/refs/heads/"+master_branch_name+" | jq -r '.object.sha'"

#output_sha = sp.getoutput(bash_cmd_sha)

#print(output_sha)
#print(bash_cmd_sha)


bash_cmd_new_pr=["curl -s -i -u "+login_name+":"+PAT_name+" "+github_base_url+"/users/"+login_name,
        "curl -s -X POST -H 'Accept: application/vnd.github.v3+json' "+github_base_url+"/repos/"+login_name+"/"+repo_name+"/pulls \
-d '{\"head\": \""+new_branch_name+"\", \
\"base\": \""+master_branch_name+"\"}'"]
#        "curl -s -X POST -H 'Authorization: token "+PAT_name+"' "+github_base_url+"/repos/"+login_name+"/"+repo_name+"/pulls \
#-d '{\"head\": \""+new_branch_name+"\", \
#\"base\": \""+master_branch_name+"\"}'"]



output_new_pr = sp.getoutput(bash_cmd_new_pr)
print(output_new_pr)







#замерджить с main

#если веток, кроме main более 3 - удалить





