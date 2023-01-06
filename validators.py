'''
В данном файле описана вся валидация.
'''


class CustomValidationError(Exception):
    def __init__(self, *args):
        self.message = args[0]

    def __str__(self):
        return f'Ошибка ввода. {self.message} '


def name_validator(name: str) -> str:
    if (not name) or (name.strip() == ''):
        raise CustomValidationError('Название вакансии не может быть пустым')
    return name


def desc_validator(desc: str) -> str:
    if (not desc) or (desc.strip() == ''):
        raise CustomValidationError('Описание вакансии не может быть пустым')
    return desc


def skills_validator(skills: str) -> str:
    if (not skills) or (skills.strip() == ''):
        raise CustomValidationError('Введите хотя бы один ключевой навык')
    return skills


def salary_validator(salary: str) -> int:
    try:
        return int(salary)
    except ValueError:
        raise CustomValidationError('Вы ввели не число, попробуйте ещё раз')


def employment_validator(employment: str) -> str:
    employment = employment.lower()
    if employment.startswith('уд'):
        employment = 'удаленно'
    elif employment.startswith('в'):
        employment = 'в офисе'
    elif employment.startswith('см'):
        employment = 'смешанный'
    else:
        raise CustomValidationError('Выберите один из трех типов: удаленный, смешанный или в офисе')
    return employment
