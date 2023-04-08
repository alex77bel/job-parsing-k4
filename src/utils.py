from src.classes import *


def create_collection_from_file(vacancies):  # создает коллекцию Vacancy.all
    Vacancy.all.clear()
    for vacancy in vacancies:
        Vacancy.all.append(HHVacancy(vacancy) if vacancy['service_name'] == 'HeadHunter' else SJVacancy(vacancy))


def filter_by_salary(salary: int):  # фильтрует коллекцию Vacancy.all по зарплате salary
    result = []
    for vacancy in Vacancy.all:
        salary_from = vacancy.salary_from if vacancy.salary_from else 0
        salary_to = vacancy.salary_to if vacancy.salary_to else 0
        if salary >= salary_from:  # если salary удовлетворят
            if not salary_to or salary <= salary_to:  # зарплате в вакансии
                result.append(vacancy)  # сохраняем промежуточный список
    Vacancy.all = result


def filter_by_service(service: int):  # фильтрует коллекцию Vacancy.all по сервису: 1-НН 2-SJ
    result = []
    for vacancy in Vacancy.all:
        if service == 1:  # оставляем только НН
            if vacancy.service_name == 'HeadHunter':
                result.append(vacancy)
        else:  # оставляем только SJ
            if vacancy.service_name == 'SuperJob':
                result.append(vacancy)
    Vacancy.all = result


def filter_by_requirement(word: str):  # фильтрует коллекцию Vacancy.all по фразе в поле requirement
    result = []
    for vacancy in Vacancy.all:
        if word in vacancy.requirement:
            result.append(vacancy)
    Vacancy.all = result


def get_top(n: int):  # оставляет top n вакансий в коллекции all
    Vacancy.all = Vacancy.all[len(Vacancy.all) - n:]


def user_input_for_request():  # функция для получения от пользователя данных для запроса
    while True:
        service = input(
            f'На каком сервисе будем искать? ("1" - HeadHunter | "2" - SuperJob | "0" - на всех | "stop" - выход): ')
        if service == 'stop': return 'stop'
        if service in ('0', '1', '2'): break

    keyword = input('Введите поисковый запрос("stop" - выход): ')
    if keyword == 'stop': return 'stop'
    return service, keyword


def user_menu_loaded():  # меню пользователя для выбора действий с загруженными данными
    print('Выберите действия с данными:')
    while True:
        service = input(
            '\t- Фильтровать вакансии по сервису ("1" - только Head Hunter | "2" - только Super Job | "0" - оба | "stop" - выход):\n')
        if service in ('0', '1', '2', 'stop'): break
    if service == 'stop': return 'stop'
    service = int(service)

    while True:
        salary = input('\t- Фильтровать вакансии по зарплате ("1" - да | "0" - нет | "stop" - выход):\n')
        if salary in ('0', '1', 'stop'): break
    if salary == 'stop': return 'stop'
    if salary == '1':
        while True:
            salary = input(f'Введите размер заработной платы:\n')
            if salary.isdigit(): break
    salary = int(salary)

    while True:
        req = input('\t- Искать фразу в требованиях к вакансии ("1" - да | "0" - нет | "stop" - выход):\n')
        if req in ('0', '1', 'stop'): break
    if req == 'stop': return 'stop'
    if req == '1':
        req = input(f'Введите фразу:\n')
    else:
        req = 0

    return service, salary, req


def add_json(srv: HH | SJ, vcn: HHVacancy | SJVacancy, keyword: str, file: JSONFileInterface):
    """
    Загружает вакансии с сервиса, добавляет их в JSON файл
    """
    items = srv.get_request(keyword)  # получаем вакансии с сервиса в виде списка
    print(f'Найдено {len(items)} вакансий на', 'HeadHunter' if srv.__class__.__name__ == 'HH' else 'SuperJob')
    print('Обработка результатов...')
    for item in items:  # сохраняем данные в файл
        file.insert(vcn(item))


def print_result():  # вывод результатов
    print(f'Найдено {len(Vacancy.all)} вакансий.')
    while True:
        select = input('\t- Отсортировать результат по зарплате?  '
                       '("1" - да | "0" - нет | "stop" - выход):\n')
        if select in ('0', '1', 'stop'): break
    if select == 'stop': return 0
    if select == '1':
        Vacancy.all.sort()

        while True:
            select = input('\t- Вывести:'
                           '("0" - все отсортированные | "1" - top n | "stop" - выход):\n')
            if select in ('0', '1', 'stop'): break
        if select == 'stop': return 'stop'
        if select == '1':
            while True:
                select = input(f'Введите n (max {len(Vacancy.all)}): ')
                if select.isdigit():
                    if int(select) <= len(Vacancy.all):
                        get_top(int(select))
                        break

    [print(i) for i in Vacancy.all]
