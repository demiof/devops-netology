#!/bin/env python3

import sys
import os
import subprocess as sp
import requests

# Модель разработки - Магистральная, т.е. нужны частые изменения - в виде PR, желательно не реже 1 раза в сутки 


login_name='demiof'
master_branch_name = 'main'
new_branch_name = 'branch_api'

auto_commit_message = 'autocommit'
github_base_url='https://api.github.com/'

help_message = """
pr-gh <branch> <message>

Создаст Pull-Request для текущего репозитория. 

Параметры для передачи:
    branch - выбранная ветка
    message - сообщение для PR
"""
help_message_wrong_type="""

Не верный тип аргумента(ов)!

"""

help_message_not_git="""

Это не git репозиторий!

"""

help_message_no_PAT_within_env="""

Не найден PAT  в переменых окружения!

"""

help_message_curepo_isouton_gh="""

Текущий репозиторий не найден на GitHub!

"""


def repo_name() -> str:
    return os.path.basename(os.getcwd())

def fatal(message: str) -> None:
    print(message)
    sys.exit(1)

def is_git_repo() -> bool:
    if os.path.isdir(".git"):
        return True
    return False

def get_current_branch() -> str:
    f = open('.git/HEAD')
    s = f.read().strip()
    return s.split('/')[-1]

class GithubClient():
    def __init__(self, gh_user: str, token: str) -> None:
        s = requests.Session()
        s.auth = (gh_user,token)

        self.session = s
        self.gh_url = github_base_url
    
    def is_github_repo(self, repo_name: str) -> bool:
       
        resp = self.session.get(f"{self.gh_url}repos/{login_name}/{repo_name}")
        if resp.status_code == 200:
            return True
        return False 
    def create_pr(self, repo_name: str, branch_name: str, message: str) -> str:
        resp = self.session.post(
                    f"{self.gh_url}repos/{login_name}/{repo_name}/pulls",
                    json={
                        "title": message,
                        "head": branch_name,
                        "base": "main"
                    },
                )

        if not resp.ok:
            raise Exception(resp.json())
        
        data=resp.json()
        return data["html_url"]

if __name__ == "__main__":

    # Определяем имя репозитория, проверяем в его ли папке и сущ-е .git

    A = sys.argv
    if len(A) <= 2: 
        fatal(help_message)
    elif A[1]=='-h' or A[1]=='--help':
        fatal(help_message)
    elif type(A[1])==str and type(A[2])==str:
        
        remote_name=A[1]
        pr_message=A[2]

        if not is_git_repo():
            fatal(help_message_not_git)
        else:
            print('\nИмя удаленного репозитория - '+str(remote_name)+'\n'+'Сообщение для pull request - '+A[2]+'\n')
    else: 
        fatal(help_message_wrong_type)

    if os.environ.get('PAT_git_bash', None) is None:
        fatal(help_message_no_PAT_within_env)
    else:
        PAT_name = os.environ.get('PAT_git_bash', None)

    gh_client = GithubClient(login_name,PAT_name)
    if not gh_client.is_github_repo(repo_name()):
        fatal(help_message_curepo_isouton_gh)


    branch_name = get_current_branch()
    print(branch_name)
    try:
        url = gh_client.create_pr(repo_name(), branch_name, pr_message)
    except Exception as e:
        fatal(f"{str(e)}")
    print(f"Ссылка на PR: {url}")
