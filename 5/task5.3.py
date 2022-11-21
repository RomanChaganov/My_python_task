import csv
import math
from datetime import datetime


def exit_with_print(line):
    print(line)
    exit()


currency_to_rub = {
    "AZN": 35.68,
    "BYR": 23.91,
    "EUR": 59.90,
    "GEL": 21.74,
    "KGS": 0.76,
    "KZT": 0.13,
    "RUR": 1,
    "UAH": 1.64,
    "USD": 60.66,
    "UZS": 0.0055,
}


class Salary:
    def __init__(self, salary_from, salary_to, salary_currency):
        salary = Salary.currency_translate(salary_from, salary_to, salary_currency)
        self.salary_ru = int((salary[0] + salary[1]) / 2)

    @staticmethod
    def currency_translate(salary_from, salary_to, salary_currency):
        salary_from = int(math.trunc(float(salary_from))) * currency_to_rub[salary_currency]
        salary_to = int(math.trunc(float(salary_to))) * currency_to_rub[salary_currency]
        return salary_from, salary_to


class Vacancy:
    def __init__(self, dictionary):
        self.name = dictionary['name']
        self.salary = Salary(dictionary['salary_from'], dictionary['salary_to'], dictionary['salary_currency'])
        self.area_name = dictionary['area_name']
        self.published_at = dictionary['published_at']


class DataSet:
    def __init__(self, file_name):
        self.file_name = file_name
        self.vacancies_objects = DataSet.prepare_data(file_name)

    @staticmethod
    def read_csv(file_name):
        reader_csv = csv.reader(open(file_name, encoding='utf_8_sig'))
        list_data = [x for x in reader_csv]
        if len(list_data) == 0:
            exit_with_print("Пустой файл")
        if len(list_data) == 1:
            exit_with_print("Нет данных")
        columns = list_data[0]
        vacancies = [x for x in list_data[1:] if len(x) == len(columns) and x.count('') == 0]
        return columns, vacancies

    @staticmethod
    def prepare_data(file_name):
        columns, vacancies = DataSet.read_csv(file_name)
        list_vacancies = []
        for row in vacancies:
            vacancy_dict = {}
            for i in range(len(row)):
                vacancy_dict[columns[i]] = row[i]
            list_vacancies.append(Vacancy(vacancy_dict))
        return list_vacancies


class InputConnect:
    def __init__(self):
        params = InputConnect.get_params()
        data_set = DataSet(params[0])
        InputConnect.print_data(data_set.vacancies_objects, params[1])

    @staticmethod
    def get_params():
        file_name = input('Введите название файла: ')
        job_name = input('Введите название профессии: ')
        return file_name, job_name


    @staticmethod
    def print_data(list_vacancies, job_name):
        years = set()
        for vacancy in list_vacancies:
            years.add(int(datetime.strptime(vacancy.published_at, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y')))
        years = sorted(list(years))
        years = list(range(min(years), max(years) + 1))

        salary_by_years = {year: [] for year in years}
        vacs_by_years = {year: 0 for year in years}
        job_salary_by_years = {year: [] for year in years}
        job_count_by_years = {year: 0 for year in years}
        area_dict = {}
        vacs_dict = {}

        for vacancy in list_vacancies:
            year = int(datetime.strptime(vacancy.published_at, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y'))
            salary_by_years[year].append(vacancy.salary.salary_ru)
            vacs_by_years[year] += 1
            if job_name in vacancy.name:
                job_salary_by_years[year].append(vacancy.salary.salary_ru)
                job_count_by_years[year] += 1
            if vacancy.area_name in area_dict:
                area_dict[vacancy.area_name].append(vacancy.salary.salary_ru)
            else:
                area_dict[vacancy.area_name] = [vacancy.salary.salary_ru]
            if vacancy.area_name in vacs_dict:
                vacs_dict[vacancy.area_name] += 1
            else:
                vacs_dict[vacancy.area_name] = 1

        salary_by_years = {key: int(sum(value) / len(value)) if len(value) != 0 else 0 for key, value in salary_by_years.items()}
        job_salary_by_years = {key: int(sum(value) / len(value)) if len(value) != 0 else 0 for key, value in job_salary_by_years.items()}

        area_list = area_dict.items()
        area_list = [x for x in area_list if len(x[1]) / len(list_vacancies) > 0.01]
        area_list = sorted(area_list, key=lambda x: sum(x[1]) / len(x[1]), reverse=True)
        salary_by_cities = {x[0]: int(sum(x[1]) / len(x[1])) for x in area_list[0: min(len(area_list), 10)]}

        vacs_count = {x: round(y / len(list_vacancies), 4) for x, y in vacs_dict.items()}
        vacs_count = {key: value for key, value in vacs_count.items() if value >= 0.01}
        vacs_by_cities = dict(sorted(vacs_count.items(), key=lambda x: x[1], reverse=True))
        vacs_by_cities = dict(list(vacs_by_cities.items())[:10])

        print('Динамика уровня зарплат по годам:', salary_by_years)
        print('Динамика количества вакансий по годам:', vacs_by_years)
        print('Динамика уровня зарплат по годам для выбранной профессии:', job_salary_by_years)
        print('Динамика количества вакансий по годам для выбранной профессии:', job_count_by_years)
        print('Уровень зарплат по городам (в порядке убывания):', salary_by_cities)
        print('Доля вакансий по городам (в порядке убывания):', vacs_by_cities)


InputConnect()
