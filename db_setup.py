'''
В данном файле описано все взаимодействие с базой данных, включая описание моделей
'''
from contextlib import contextmanager
from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import String, Column, Boolean, Integer, DateTime, Enum
from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import NoSuchModuleError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import UUIDType
from sqlalchemy_utils import database_exists, create_database

import json
from config import URL, JSON_DIR, DEBUG

Base = declarative_base()

try:
    ENGINE = create_engine(URL, echo=DEBUG)
    DBSession = sessionmaker(bind=ENGINE)
except NoSuchModuleError:
    print('Проблема с подключением к базе данных. Проверьте файл config.py.\nДанные не внесены.')
    exit(2)


class BaseModel(Base):
    '''Абстрактный класс для наследования'''
    __abstract__ = True
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid4)
    created_at = Column(DateTime, nullable=False, default=datetime.now())
    updated_at = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())
    is_deleted = Column(Boolean, nullable=False, default=False)

    def delete(self):
        self.is_deleted = True

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


class Vacancy(BaseModel):
    '''Сущность вакансий'''
    __tablename__ = 'vacancies'

    name = Column(String(100), nullable=False)
    desc = Column(String(500), nullable=False)
    hard_skills = Column(String(300), nullable=False)
    salary = Column(Integer, nullable=False)
    employment = Column(Enum('удаленно', 'смешанный график', 'в офисе'))

    def __init__(self, name: str, desc: str, hard_skills: str, salary: int, employment: str, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.name = name
        self.desc = desc
        self.hard_skills = hard_skills
        self.salary = salary
        self.employment = employment


def connect_db(url: str, engine: Engine) -> None:
    '''
    Установка подключения к базе
    :param url: url до базы (формируется автоматически из конфигов)
    :param engine:
    :return:
    '''
    meta = MetaData()
    if not database_exists(url):
        create_database(url)
    meta.create_all(engine)
    Base.metadata.create_all(engine)


@contextmanager
def session_scope():
    '''
    Генератор сессий для подключений к базе
    :return:
    '''
    session = DBSession()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def save_in_db(data: dict | list[dict]) -> None:
    '''
    Сохранение данных в базу
    :param data: dict or list[dict] - данные для сохранения в базу
    :param session: сессия
    '''
    with session_scope() as s:
        connect_db(URL, ENGINE)
        if isinstance(data, list):
            for el in data:
                obj = Vacancy(**el)
                s.add(obj)
        else:
            obj = Vacancy(**data)
            s.add(obj)


def filling_testing_data(file_name: str) -> None:
    '''
    Заполняет базу данными из файла
    :param file_name: имя файла в папке json в корне проекта
    :return: None
    '''
    connect_db(URL, ENGINE)
    with open(JSON_DIR / file_name, 'r', encoding='UTF-8') as f:
        data = json.load(f)
    save_in_db(data)


def search_by_name(search_obj: str, table: BaseModel = Vacancy) -> list | None:
    '''
    Поиск в базе данных по названию вакансии
    :param search_obj: объект поиска
    :param table: таблица для поиска
    :return: list[dict] | None - список словарей с данными по вакансиям.
    '''
    result = []
    connect_db(URL, ENGINE)
    with session_scope() as s:
        selected_vacancies = s.query(table).filter(table.name.ilike(f'%{search_obj}%')).order_by(table.salary)
        for el in selected_vacancies:
            result.append({
                'name': el.name,
                'desc': el.desc,
                'hard_skills': el.hard_skills,
                'salary': el.salary,
                'employment': el.employment,
                'date': str(el.created_at)[:-7],
            })
        return result if result else None


def select_all_from_table(table: BaseModel = Vacancy) -> list | None:
    '''
    Показать все неудаленные вакансии
    :param table: таблица для поиска
    :return: list[dict] | None - список словарей с данными по вакансиям.
    '''
    result = []
    connect_db(URL, ENGINE)
    with session_scope() as s:
        selected_vacancies = s.query(table).filter(table.is_deleted == 0).order_by(table.salary)
        for el in selected_vacancies:
            result.append({
                'name': el.name,
                'desc': el.desc,
                'hard_skills': el.hard_skills,
                'salary': el.salary,
                'employment': el.employment,
                'date': str(el.created_at)[:-7],
            })
        return result if result else None
