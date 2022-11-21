import csv
import re

rus_names = {'name': 'Название',
             'description': 'Описание',
             'key_skills': 'Навыки',
             'experience_id': 'Опыт работы',
             'premium': 'Премиум-вакансия',
             'employer_name': 'Компания',
             'salary_from': 'Нижняя граница вилки оклада',
             'salary_to': 'Верхняя граница вилки оклада',
             'salary_gross': 'Оклад указан до вычета налогов',
             'salary_currency': 'Идентификатор валюты оклада',
             'area_name': 'Название региона',
             'published_at': 'Дата и время публикации вакансии'}

rus_true_false = {'True': 'Да', 'False': 'Нет'}


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


def print_vacancies(data_vacancies, dic_naming):
    for sentence in data_vacancies:
        for key, value in sentence.items():
            print(f'{dic_naming[key]}: {value}')
        print()


data_tuple = сsv_reader(input())
resume_list = csv_filer(data_tuple[0], data_tuple[1])
print_vacancies(resume_list, rus_names)
