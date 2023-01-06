'''
В данном файле описана вся валидация
'''


def name_is_valid(name: str) -> bool:
    return False if (not name) or (len(name) < 3) or (name.strip() == '') else True


def desc_is_valid(desc: str) -> bool:
    return name_is_valid(desc)


def skills_is_valid(skills: str) -> bool:
    return name_is_valid(skills)


def salary_is_valid(salary: str) -> bool:
    try:
        salary = int(salary)
        return True
    except ValueError:
        return False


def employment_is_valid(employment: str) -> bool:
    if employment.startswith('удал') or employment.startswith('в оф') or employment.startswith('смеш'):
        return True
    return False


def employment_validator(employment: str) -> str:
    if employment.startswith('уд'):
        employment = 'удаленно'
    elif employment.startswith('в'):
        employment = 'в офисе'
    elif employment.startswith('см'):
        employment = 'смешанный'
    else:
        employment = 'не указано'
    return employment
