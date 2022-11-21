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
    salary_from = math.trunc(float(salary_from))
    salary_to = math.trunc(float(salary_to))
    return f"{salary_from} - {salary_to} ({currency}) ({is_gross})"


return_line = lambda line: line

dict_names = {'name': return_line,
              'description': return_line,
              'key_skills': return_line,
              'experience_id': lambda line: experience_rus[line],
              'premium': return_line,
              'employer_name': return_line,
              'salary_from': salary_format,
              'area_name': return_line,
              'published_at': lambda date: datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z').strftime('%d.%m.%Y %H:%M:%S%z')}

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

rus_names = {'Название': 'name', 'Описание': 'description', 'Навыки': 'key_skills', 'Опыт работы': 'experience_id',
             'Премиум-вакансия': 'premium', 'Компания': 'employer_name', 'Оклад': 'salary_from',
             'Верхняя граница вилки оклада': 'salary_to', 'Оклад указан до вычета налогов': 'salary_gross',
             'Идентификатор валюты оклада': 'salary_currency', 'Название региона': 'area_name',
             'Дата публикации вакансии': 'published_at'}

currency_to_rub = {
    "Манаты": 35.68,
    "Белорусские рубли": 23.91,
    "Евро": 59.90,
    "Грузинский лари": 21.74,
    "Киргизский сом": 0.76,
    "Тенге": 0.13,
    "Рубли": 1,
    "Гривны": 1.64,
    "Доллары": 60.66,
    "Узбекский сум": 0.0055}


def exit_with_print(line):
    print(line)
    sys.exit()


def check_sort_parameter(line, source_list, result_line):
    if line == '':
        return line
    if line not in source_list:
        exit_with_print(result_line)
    return line


def check_parameter(line):
    if line == '':
        return []
    if ': ' not in line:
        exit_with_print('Формат ввода некорректен')
    filter_list = line.split(': ')
    if filter_list[0] not in list(rus_names.keys()):
        exit_with_print('Параметр поиска некорректен')
    return filter_list


def сsv_reader(file_name):
    reader_csv = csv.reader(open(file_name, encoding='utf_8_sig'))
    list_data = [x for x in reader_csv]
    if len(list_data) == 0:
        exit_with_print("Пустой файл")
    if len(list_data) == 1:
        exit_with_print("Нет данных")
    columns = list_data[0]
    vacancies = [x for x in list_data[1:] if len(x) == len(columns) and x.count('') == 0]
    return vacancies, columns


def edit_line(line):
    string = re.sub(r'<[^>]+>', '', line)
    if '\n' not in string:
        string = ' '.join(string.split())
    if string == 'True' or string == 'False':
        string = rus_true_false[string]
    return string


def csv_filer(reader, list_naming):
    resumes = []
    sentences = {}
    for resume in reader:
        for i in range(len(resume)):
            resume[i] = edit_line(resume[i])
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


def check_salary(line, filt):
    salary = line.split()
    salary_from = salary[0]
    salary_to = salary[2]
    return int(salary_from) <= int(filt) <= int(salary_to)


def check_skills(line, filt):
    parameters = filt.split(', ')
    list_skill = line.split('\n')
    k = 0
    for x in parameters:
        if x in list_skill:
            k = k + 1
    return k == len(parameters)


experience_sort = {'Нет опыта': 0, 'От 1 года до 3 лет': 1, 'От 3 до 6 лет': 2, 'Более 6 лет': 3}


def new_create_data(input_func):
    def output_func(data, filter_list, sort, reverse):
        is_reverse = False
        if reverse == 'Да':
            is_reverse = True

        def for_sort(row):
            if sort == 'Оклад':
                salary = row['salary_from'].split()
                #currency = row['salary_from'].split()[3].replace('(', '').replace(')', '')
                currency = re.search(r'\((.*?)\)', row['salary_from']).group(1)
                salary_from = int(salary[0]) * currency_to_rub[currency]
                salary_to = int(salary[2]) * currency_to_rub[currency]
                return (salary_from + salary_to) / 2
            if sort == 'Навыки':
                skills = row['key_skills'].split('\n')
                return len(skills)
            if sort == 'Дата публикации вакансии':
                return datetime.strptime(row['published_at'], '%d.%m.%Y %H:%M:%S%z')
            if sort == 'Опыт работы':
                return experience_sort[row['experience_id']]
            return row[rus_names[sort]]

        filtered_list = input_func(data, filter_list)
        if sort != '':
            filtered_list = sorted(filtered_list, key=for_sort, reverse=is_reverse)

        for i in range(len(filtered_list)):
            salary = filtered_list[i]['salary_from'].split()
            salary_from = '{0:,}'.format(int(salary[0])).replace(',', ' ')
            salary_to = '{0:,}'.format(int(salary[2])).replace(',', ' ')
            salary[0] = str(salary_from)
            salary[2] = str(salary_to)
            filtered_list[i]['salary_from'] = ' '.join(salary)
            filtered_list[i]['published_at'] = datetime.strptime(filtered_list[i]['published_at'], '%d.%m.%Y %H:%M:%S%z').strftime('%d.%m.%Y')

            new_list = list(filtered_list[i].values())
            for j in range(len(new_list)):
                if len(new_list[j]) > 100:
                    new_list[j] = new_list[j][:100] + '...'
            filtered_list[i] = new_list
            filtered_list[i].insert(0, str(i + 1))
        return filtered_list

    return output_func

filter_dict = {'Опыт работы': lambda line, filt: line == filt,
               'Идентификатор валюты оклада': lambda line, filt: line.split()[3].replace('(', '').replace(')', '') == filt,
               'Оклад': check_salary,
               'Дата публикации вакансии': lambda line, filt: datetime.strptime(line, '%d.%m.%Y %H:%M:%S%z').strftime('%d.%m.%Y') == filt,
               'Навыки': check_skills}


@new_create_data
def create_data(data, filter_list):
    result_list = []
    for i in range(len(data)):
        dictionary = formatter(data[i])
        result_list.append(dictionary)

    def for_filter(row):
        if filter_list == []:
            return True
        if filter_list[0] == 'Оклад':
            return filter_dict['Оклад'](row['salary_from'], filter_list[1])
        if filter_list[0] == 'Идентификатор валюты оклада':
            return filter_dict['Идентификатор валюты оклада'](row['salary_from'], filter_list[1])
        if filter_list[0] in list(filter_dict):
            return filter_dict[filter_list[0]](row[rus_names[filters[0]]], filter_list[1])
        return row[rus_names[filters[0]]] == filter_list[1]

    filtered_list = list(filter(for_filter, result_list))
    if filtered_list == []:
        exit_with_print('Ничего не найдено')
    return filtered_list


def print_vacancies(data_vacancies, filter_list, sort, reverse, indexes, fields_list):
    data = create_data(data_vacancies, filter_list, sort, reverse)
    table = PrettyTable()
    rus_list = list(rus_names.keys())
    table.field_names = ['№'] + rus_list[:7] + rus_list[10:]
    table.align = 'l'
    table.hrules = prettytable.ALL
    table.max_width = 20
    table.add_rows(data)

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


file_name = input('Введите название файла: ')
parameter = input('Введите параметр фильтрации: ')
sort_parametr = input('Введите параметр сортировки: ')
reverse_sort = input('Обратный порядок сортировки (Да / Нет): ')
start_end_index = input('Введите диапазон вывода: ').split()
fields_name = input('Введите требуемые столбцы: ').split(', ')

filters = check_parameter(parameter)
sort_parameter = check_sort_parameter(sort_parametr, list(rus_names.keys()), 'Параметр сортировки некорректен')
reverse_sort = check_sort_parameter(reverse_sort, list(rus_true_false.values()), 'Порядок сортировки задан некорректно')

data_tuple = сsv_reader(file_name)
resume_list = csv_filer(data_tuple[0], data_tuple[1])
print_vacancies(resume_list, filters, sort_parameter, reverse_sort, start_end_index, fields_name)
