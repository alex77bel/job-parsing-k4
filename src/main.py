from src.classes import *
from src.utils import *

JSON_FILENAME = 'data.json'


def main():
    file_interface = JSONFileInterface(JSON_FILENAME)  # создаем/находим файл для хранения данных
    is_file_ok = file_interface.validation()  # проверяем состояние файла
    if is_file_ok:  # есть годный файл
        print('Найден рабочий файл. Выберите:\n\t '
              '1 - использовать файл\n\t '
              '2 - загрузить данные с сервисов\n')
        while True:
            select = input()
            if select in ('1', '2'): break
    if not is_file_ok or select == '2':  # если нет файла или выбрана перезагрузка, загружаем данные с сайтов
        file_interface.datafile = []  # сбрасываем содержимое файла
        # получаем от пользователя данные для запроса
        user_input = user_input_for_request()  # (service=<1-HH,2-SJ,0-all>, keyword)
        if user_input == 'stop': return 0

        # Загружаем вакансии с сервиса, добавляет их в JSON файл
        if user_input[0] in ('0', '1'):  # если выбран НН или оба
            add_json(HH(), HHVacancy, user_input[1], file_interface)
        if user_input[0] in ('0', '2'):
            add_json(SJ(), SJVacancy, user_input[1], file_interface)

    # здесь имеем готовый файл для работы
    # запрашиваем у пользователя параметры фильтрации
    user_answer = user_menu_loaded()  # (фильтр по сервису 1-НН 2-SJ 0-оба, фильтр по зп 0-нет или число, фильтр по фразе)
    if user_answer == 'stop': return 0
    create_collection_from_file(file_interface.datafile)  # читаем файл и создаем коллекцию экземпляров
    if user_answer[0]: filter_by_service(user_answer[0])  # фильтруем по сервису
    if user_answer[1]: filter_by_salary(user_answer[1])  # фильтруем по зп
    if user_answer[2]: filter_by_requirement(user_answer[2])  # фильтруем по фразе в требованиях
    print_result()  # вывод результатов


main()
