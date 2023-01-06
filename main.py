from typing import Callable

from db_setup import save_in_db, search_in_db, filling_testing_data
from validators import name_validator, desc_validator, skills_validator, salary_validator, employment_validator, \
    CustomValidationError


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
        'hard_skills': hard_skills,
        'desc': description,
        'salary': salary,
        'employment': employment
    }


def main_save_data_in_db():
    data = request_vacancy_data()
    save_in_db(data)


if __name__ == '__main__':
    # main_save_data_in_db()
    search_in_db('python')
    # filling_testing_data('test_data.json')
