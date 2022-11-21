import csv
import re
import math
from datetime import datetime

rus_names = {'name': 'Название',
             'description': 'Описание',
             'key_skills': 'Навыки',
             'experience_id': 'Опыт работы',
             'premium': 'Премиум-вакансия',
             'employer_name': 'Компания',
             'salary_from': 'Оклад',
             'salary_to': 'Верхняя граница вилки оклада',
             'salary_gross': 'Оклад указан до вычета налогов',
             'salary_currency': 'Идентификатор валюты оклада',
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
    columns = list_data[0]
    vacancies = [x for x in list_data[1:] if len(x) == len(columns) and x.count('') == 0]
    return vacancies, columns


def csv_filer(reader, list_naming):
    resumes = []
    sentences = {}
    for resume in reader:
        for i in range(len(resume)):
            resume[i] = ', '.join(resume[i].split('\n'))
            resume[i] = re.sub(r'<[^>]+>', '', resume[i])
            resume[i] = ' '.join(resume[i].split())
            if resume[i] == 'True' or resume[i] == 'False':
                resume[i] = rus_true_false[resume[i]]
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
    for sentence in data_vacancies:
        dictionary = formatter(sentence)
        for key, value in dictionary.items():
            print(f'{key}: {value}')
        print()


data_tuple = сsv_reader(input())
resume_list = csv_filer(data_tuple[0], data_tuple[1])
print_vacancies(resume_list, rus_names)
