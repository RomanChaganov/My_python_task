import math

def StrNotEmpty(line):
    while True:
        a = input(line)
        if len(a) != 0:
            return a
        else:
            print('Данные некорректны, повторите ввод')

def StrToInteger(line):
    while True:
        a = input(line)
        try:
            return int(a)
        except:
            print('Данные некорректны, повторите ввод')

def Declination(number, line, first, second, third):
    a = number % 10
    b = number % 100
    if a == 1 and b != 11:
        print(f'{line} {number} {first}')
    elif a >= 2 and a <= 4 and (b < 10 or b >= 20):
        print(f'{line} {number} {second}')
    else:
        print(f'{line} {number} {third}')

def StrToBool(line):
    while True:
        a = input(line)
        if a == 'да' or a == 'нет':
            return a
        else:
            print('Данные некорректны, повторите ввод')

vacancy = StrNotEmpty('Введите название вакансии: ')
description = StrNotEmpty('Введите описание вакансии: ')
experience = StrToInteger('Введите требуемый опыт работы (лет): ')
min_salary = StrToInteger('Введите нижнюю границу оклада вакансии: ')
max_salary = StrToInteger('Введите верхнюю границу оклада вакансии: ')

schedule = StrToBool('Есть ли свободный график (да / нет): ')
premium = StrToBool('Является ли данная вакансия премиум-вакансией (да / нет): ')

print(vacancy)
print(f'Описание: {description}')

Declination(experience, 'Требуемый опыт работы:', 'год', 'года', 'лет')
Declination(math.trunc((min_salary + max_salary) / 2), 'Средний оклад:', 'рубль', 'рубля', 'рублей')

print(f'Свободный график: {schedule}')
print(f'Премиум-вакансия: {premium}')
