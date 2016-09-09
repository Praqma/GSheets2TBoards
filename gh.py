from __future__ import print_function
from github import Github
import fileinput


def main():
    print('Welcome to GSheets2TBoards converter')
    gh_usrname = input('Github username:')
    gh_password = input('Github password')
    gh_repo=input('Github repository name')
    # First create a Github instance:
    g = Github(gh_usrname, gh_password)
    # Then play with your Github objects:
    repo = g.get_user().get_repo(gh_repo)

#    for repo in g.get_user().get_repos():
        # repo.create_issue
 #       for issue in repo.get_issues():
  #          print(issue.title)
    repo.create_issue('Title')
    for issue in repo.get_issues():
        print(issue.title)

        #repo.edit(has_wiki=False)
if __name__ == '__main__':
    main()
