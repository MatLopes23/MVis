import pandas as pd
from git import Repo
import re
import random
import datetime

root_path = '/home/mateuslopes/Documentos/MVis'
root_path_repositories = '/home/mateuslopes/Documentos/Code-Smell'

def search_days_commits():
    df_history = pd.read_csv(root_path + '/Datasets/data_set_complexity_history_all_languages_top_complex.csv')
    
    df_history = df_history.drop_duplicates(subset=['project', 'sha'])
    df_weekdays = []

    for instance in df_history.iterrows():

        method = instance[1]

        date = method.date
        tz = date[19:25].replace(':','')
        date = datetime.datetime.strptime(date[0:19]+tz, '%Y-%m-%d %H:%M:%S%z')

        df_weekdays.append([method.language, date.isoweekday(), date.year])


    df_weekdays = pd.DataFrame(df_weekdays, columns=['language', 'weekday', 'year'])
    df_weekdays.sort_values(by=['language','weekday','year'], inplace=True)
    df_weekdays_grouped = []

    languages = df_weekdays.language.unique()
    days_week = df_weekdays.weekday.unique()
    min_year = df_weekdays.year.min()
    max_year = df_weekdays.year.max()

    for day in days_week:
        for language in languages:
            year = min_year
            count = 0
            while(year <= max_year):
                count += len(df_weekdays[(df_weekdays.language == language) &
                            (df_weekdays.weekday == day) &
                            (df_weekdays.year == year)])
                
                df_weekdays_grouped.append([language, day, year, count])
                year += 1
    

    dic = {1: "Segunda", 2: "Terça", 3:"Quarta", 4:"Quinta", 5:"Sexta", 6:"Sábado", 7:"Domingo"}
    df_weekdays_grouped = pd.DataFrame(df_weekdays_grouped, columns=['language', 'weekday', 'year', 'total'])

    df_weekdays_grouped.weekday.replace(dic, inplace=True)
    df_weekdays_grouped.to_csv(root_path + '/Datasets/data_set_weekdays.csv')


def main():
    search_days_commits()

if __name__ == '__main__':
    main()