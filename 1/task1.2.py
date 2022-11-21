import math
vacancy = input('Введите название вакансии: ')
description = input('Введите описание вакансии: ')
experience = int(input('Введите требуемый опыт работы (лет): '))
min_salary = int(input('Введите нижнюю границу оклада вакансии: '))
max_salary = int(input('Введите верхнюю границу оклада вакансии: '))
schedule = input('Есть ли свободный график (да / нет): ')
premium = input('Является ли данная вакансия премиум-вакансией (да / нет): ')

print(vacancy)
print(f'Описание: {description}')

def Declination(number, line,  first, second, third):
    a = number % 10
    b = number % 100
    if a == 1 and b != 11:
        print(f'{line} {number} {first}')
    elif a >= 2 and a <= 4 and (b < 10 or b >=20):
        print(f'{line} {number} {second}')
    else:
        print(f'{line} {number} {third}')

Declination(experience, 'Требуемый опыт работы:', 'год', 'года', 'лет')
Declination(math.trunc((min_salary + max_salary) / 2), 'Средний оклад:', 'рубль', 'рубля', 'рублей')

print(f'Свободный график: {schedule}')
print(f'Премиум-вакансия: {premium}')
