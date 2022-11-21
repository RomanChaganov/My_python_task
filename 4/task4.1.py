import csv
import math
import re
import sys
from datetime import datetime
import prettytable
from prettytable import PrettyTable


def salary_format(salary_from, salary_to, salary_gross, salary_currency):
    currency = currency_rus[salary_currency]
    if salary_gross == 'Нет':
        is_gross = 'С вычетом налогов'
    else:
        is_gross = 'Без вычета налогов'
    salary_from = '{0:,}'.format(math.trunc(float(salary_from))).replace(',', ' ')
    salary_to = '{0:,}'.format(math.trunc(float(salary_to))).replace(',', ' ')
    return f"{salary_from} - {salary_to} ({currency}) ({is_gross})"


dict_names = {'name': lambda line: line,
              'description': lambda line: line,
              'key_skills': lambda line: line,
              'experience_id': lambda line: experience_rus[line],
              'premium': lambda line: line,
              'employer_name': lambda line: line,
              'salary_from': salary_format,
              'area_name': lambda line: line,
              'published_at': lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').strftime('%d.%m.%Y')}

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
            if not ('\n' in resume[i]):
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
    for key in dict_names:
        if key == 'salary_from':
            new_dict[key] = dict_names[key](row['salary_from'], row['salary_to'], row['salary_gross'],
                                            row['salary_currency'])
            continue
        new_dict[key] = dict_names[key](row[key])
    return new_dict

def create_list_for_table(data):
    result_list = []
    for i in range(len(data)):
        dictionary = formatter(data[i])
        new_list = []
        new_list.append(str(i + 1))
        for key, value in dictionary.items():
            new_list.append(value)
        result_list.append(new_list)
    return  result_list

def create_table(data_vacancies):
    table = PrettyTable()
    table.field_names = ['№', 'Название', 'Описание', 'Навыки', 'Опыт работы', 'Премиум-вакансия', 'Компания', 'Оклад',
                         'Название региона', 'Дата публикации вакансии']
    table.align = 'l'
    table.max_width = 20
    table.hrules = prettytable.ALL
    table.add_rows(create_list_for_table(data_vacancies))
    return table
    

def print_vacancies(data_vacancies, indexes, fields_list):
    table = create_table(data_vacancies)

    try:
        indexes[0] = int(indexes[0]) - 1
        indexes[1] = int(indexes[1]) - 1
    except:
        if len(indexes) == 0:
            indexes.append(0)
            indexes.append(len(data_vacancies))
        if len(indexes) == 1:
            indexes.append(len(data_vacancies))

    if len(fields_list) == 1:
        if fields_list[0] == '':
            print(table.get_string(start=indexes[0], end=indexes[1]))
        else:
            fields_list.insert(0, '№')
            print(table.get_string(start=indexes[0], end=indexes[1], fields=fields_list))
    else:
        fields_list.insert(0, '№')
        print(table.get_string(start=indexes[0], end=indexes[1], fields=fields_list))


file_name = input()
start_end_index = input().split()
fields_name = input().split(', ')

data_tuple = сsv_reader(file_name)
resume_list = csv_filer(data_tuple[0], data_tuple[1])
print_vacancies(resume_list, start_end_index, fields_name)
