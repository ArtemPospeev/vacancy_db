'''
В данном файле описано все взаимодействие с базой данных, включая описание моделей
'''

from datetime import datetime
from typing import Any
from uuid import uuid4

from sqlalchemy.future import Engine

from config import URL
from sqlalchemy import String, Column, Boolean, Integer, DateTime, Enum, select
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy_utils import UUIDType
from sqlalchemy_utils import database_exists, create_database

Base = declarative_base()

ENGINE = create_engine(URL, echo=True)
SESSION = sessionmaker(bind=ENGINE)()


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
    employment = Column(Enum('удаленно', 'смешанный график', 'в офисе', 'не указано'))

    def __init__(self, name: str, desc: str, hard_skills: str, salary: int, employment: str, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.name = name
        self.desc = desc
        self.hard_skills = hard_skills
        self.salary = salary
        self.employment = employment


def connect_db(url: str = URL, engine: Engine = ENGINE) -> None:
    '''
    Установка подключения к базе. Если база не создана - создает
    :param url: url до базы (формируется автоматически из конфигов)
    :param engine:
    :return:
    '''
    meta = MetaData()
    if not database_exists(url):
        create_database(url)
    meta.create_all(engine)
    Base.metadata.create_all(engine)


def save_in_db(data: dict, session: Session = SESSION) -> None:
    '''
    Сохранение данных в базу
    :param data: dict - данные для сохранения в базу
    :param session: сессия
    '''
    obj = Vacancy(**data)
    session.add(obj)
    session.commit()


def search_in_db(obj: str, session: Session = SESSION, table: BaseModel = Vacancy):
    selected_vacancies = session.scalar(select(table).filter_by(name=obj))
    print(selected_vacancies)
