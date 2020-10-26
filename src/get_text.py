import pandas as pd
from git import Repo
import re
import random

root_path = '/home/mateuslopes/Documentos/MVis'
root_path_repositories = '/home/mateuslopes/Documentos/Code-Smell'


def search_text_commits(language):
    df_history = pd.read_csv(root_path + '/Datasets/data_set_complexity_history_all_languages_top_complex.csv')
    df_history = df_history[df_history.language == language]
    
    df_history = df_history.drop_duplicates(subset=['project', 'sha'])
    text = ''

    for instance in df_history.iterrows():
        method = instance[1]
        sha = method['sha']

        repo_git = Repo.init(path= root_path_repositories + '/repositories/versao_saner2021/' + method['project'])
        
        git_show = repo_git.git.show('--pretty=format:%B','-s', sha)

        text += git_show
    
    with open(language+'_text_commit.txt', "w") as text_file:
        text_file.write(text)


def main():
    search_text_commits('JavaScript')


if __name__ == '__main__':
    main()