import csv
import math
import re
import sys
from datetime import datetime

import prettytable
from prettytable import PrettyTable

rus_names = {'name': 'Название',
             'description': 'Описание',
             'key_skills': 'Навыки',
             'experience_id': 'Опыт работы',
             'premium': 'Премиум-вакансия',
             'employer_name': 'Компания',
             'salary_from': 'Оклад',
             'area_name': 'Название региона',
             'published_at': 'Дата публикации вакансии'}

rus_true_false = {'True': 'Да', 'False': 'Нет'}

experience_rus = {'noExperience': 'Нет опыта',
                  'between1And3': 'От 1 года до 3 лет',
                  'between3And6': 'От 3 до 6 лет',
                  'moreThan6': 'Более 6 лет'}

currency_rus = {'AZN': 'Манаты',
                'BYR': 'Белорусские рубли',
                'EUR': 'Евро',
                'GEL': 'Грузинский лари',
                'KGS': 'Киргизский сом',
                'KZT': 'Тенге',
                'RUR': 'Рубли',
                'UAH': 'Гривны',
                'USD': 'Доллары',
                'UZS': 'Узбекский сум'}

def сsv_reader(file_name):
    reader_csv = csv.reader(open(file_name, encoding='utf_8_sig'))
    list_data = [x for x in reader_csv]
    if len(list_data) == 0:
        print("Пустой файл")
        sys.exit()
    if len(list_data) == 1:
        print("Нет данных")
        sys.exit()
    columns = list_data[0]
    vacancies = [x for x in list_data[1:] if len(x) == len(columns) and x.count('') == 0]
    return vacancies, columns


def csv_filer(reader, list_naming):
    resumes = []
    sentences = {}
    for resume in reader:
        for i in range(len(resume)):
            resume[i] = re.sub(r'<[^>]+>', '', resume[i])
            if not('\n' in resume[i]):
                resume[i] = ' '.join(resume[i].split())
            if resume[i] == 'True' or resume[i] == 'False':
                resume[i] = rus_true_false[resume[i]]
            if len(resume[i]) > 100:
                resume[i] = resume[i][:100] + '...'
            sentences[list_naming[i]] = resume[i]
        resumes.append(sentences.copy())
    return resumes

def formatter(row):
    new_dict = {}
    row['salary_currency'] = currency_rus[row['salary_currency']]
    row['experience_id'] = experience_rus[row['experience_id']]
    date = row['published_at']
    row['published_at'] = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').strftime('%d.%m.%Y')
    if row['salary_gross'] == 'Нет':
        is_gross = 'С вычетом налогов'
    else:
        is_gross = 'Без вычета налогов'
    row['salary_from'] = '{0:,}'.format(math.trunc(float(row['salary_from']))).replace(',', ' ')
    row['salary_to'] = '{0:,}'.format(math.trunc(float(row['salary_to']))).replace(',', ' ')
    salary = f"{row['salary_from']} - {row['salary_to']} ({row['salary_currency']}) ({is_gross})"
    del row['salary_to']
    del row['salary_currency']
    del row['salary_gross']
    row['salary_from'] = salary
    for key in row:
        new_dict[rus_names[key]] = row[key]
    return new_dict


def print_vacancies(data_vacancies, dic_naming):
    table = PrettyTable()
    field_list = list(dic_naming.values())
    field_list.insert(0, '№')
    table.field_names = field_list
    table.align = 'l'
    table.max_width = 20
    table.hrules = prettytable.ALL

    for i in range(len(data_vacancies)):
        dictionary = formatter(data_vacancies[i])
        new_list = []
        new_list.append(str(i + 1))
        for key, value in dictionary.items():
            new_list.append(value)
        table.add_row(new_list)

    print(table)


data_tuple = сsv_reader(input())
resume_list = csv_filer(data_tuple[0], data_tuple[1])
print_vacancies(resume_list, rus_names)
