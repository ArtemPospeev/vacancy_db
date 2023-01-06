from db_setup import setup_db, save_in_db
from validators import name_is_valid, desc_is_valid, skills_is_valid, salary_is_valid, employment_is_valid, \
    employment_validator


def request_vacancy_data() -> dict:
    '''
    Запрашивает данные у пользователя
    :return: dict -> словарь с описанием вакансии для сохранения
    '''
    while True:
        name = input('Введите наименование вакансии: ')
        if name_is_valid(name):
            break
        print('Название вакансии не может быть пустым')
    while True:
        description = input('Описание вакансии: ')
        if desc_is_valid(description):
            break
        print('Описание не может быть пустым')
    while True:
        hard_skills = input('Введите ключевые навыки: ')
        if skills_is_valid(hard_skills):
            break
        print('Необходимо указать хотя бы один ключевой навык')
    while True:
        salary = input('Введите зарплату в рублях: ')
        if salary_is_valid(salary):
            salary = int(salary)
            break
        print('Вы ввели не число, попробуйте ещё раз')
    while True:
        employment = input('Введите тип занятости(удаленно, в офисе, смешанный): ').lower()
        if employment_is_valid(employment):
            employment = employment_validator(employment)
            break
        print('Выберите один из трех: удаленно, в офисе или смешанный')
    return {
        'name': name,
        'hard_skills': hard_skills,
        'description': description,
        'salary': salary,
        'employment': employment
    }


def main():
    setup_db()
    data = request_vacancy_data()
    save_in_db(data)


if __name__ == '__main__':
    main()
