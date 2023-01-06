from typing import Callable

from db_setup import save_in_db, filling_testing_data, search_by_name
from validators import name_validator, desc_validator, skills_validator, salary_validator, employment_validator, \
    CustomValidationError

import argparse


def create_parser():
    parser = argparse.ArgumentParser(
        description='Консольное приложение для работы с базой данных',
        epilog='Тестовое задание выполнено Поспеевым А. В.')
    parser.add_argument('fill', help='Заполняет базу тестовыми данными')
    parser.add_argument('info', help='Выдает справочную информацию по работе с приложением')
    return parser


def give_user_answer(question: str, validator: Callable[[str], str | int]) -> str | int:
    '''
    Запрашивает овтет у пользователя, пока ответ не пройдет валидацию.
    Принимает вопрос и валидатор, возвращает прошедшие валидацию данные
    :param question: вопрос
    :param validator: валидатор
    :return: отвалидированные данные
    '''
    while True:
        answer = input(f'{question}: ')
        try:
            return validator(answer)
        except CustomValidationError as err:
            print(err.message)
        except Exception:
            print('Что-то пошло не так, попробуйте ещё раз')


def request_vacancy_data() -> dict:
    '''
    Запрашивает данные по вакансии у пользователя, возвращает словарь
    :return: dict -> словарь с описанием вакансии для сохранения
    '''
    name = give_user_answer('Введите название вакансии', name_validator)
    description = give_user_answer('Введите описание вакансии', desc_validator)
    hard_skills = give_user_answer('Введите ключевые навыки', skills_validator)
    salary = give_user_answer('Введите зарплату в рублях', salary_validator)
    employment = give_user_answer('Введите тип занятости(удаленно, в офисе, смешанный)', employment_validator)

    return {
        'name': name,
        'desc': description,
        'hard_skills': hard_skills,
        'salary': salary,
        'employment': employment
    }


def printing_query_result(query: list) -> None:
    '''
    Печатает на экране в читаемом варианте ответ пользователю
    :param query:
    :return:
    '''
    if not query:
        print('По вашему запросу ничего не найдено :(\n '
              'Попробуйте вернуться позже, возможно, вакансии по вашему запросу обновятся')
        return
    for el in query:
        print(f'\nНазвание вакансии: {el["name"]}\n'
              f'Описание вакансии: {el["desc"]}\n'
              f'Ключевые навыки: {el["hard_skills"]}\n'
              f'Заработная плата: {el["salary"]}\n'
              f'Тип занятости: {el["employment"]}\n'
              f'Дата добавления вакансии: {el["date"]}\n',
              '-' * 50,
              '\n')


def main():
    parser = create_parser()
    args = parser.parse_args()
    if 'fill' in args:
        filling_testing_data('test_data.json')
        exit(1)

    print('Приветствую в приложении Job Assistant. С радостью помогу Вам в поиске вакансий!')
    while True:
        answ = input('Выберите действие:\n'
                     '1 | добавить | add - Добавить вакансию в базу\n'
                     '2 | найти | search | поиск - Поиск в базе по названию вакансии\n'
                     '0 - для выхода\n')
        if answ.lower() in ('1', 'добавить', 'add'):
            data = request_vacancy_data()
            save_in_db(data)
        elif answ.lower() in ('2', 'найти', 'поиск', 'search'):
            search_obj = input('Введите ключевое слово для поиска: ')
            query_result = search_by_name(search_obj)
            printing_query_result(query_result)
        elif answ.lower() in ('0', 'exit', 'выход'):
            exit(1)


if __name__ == '__main__':
    main()
