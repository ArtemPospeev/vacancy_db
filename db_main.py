from datetime import datetime
from uuid import uuid4

from config import db_name, host, user, password, port
from sqlalchemy import String, Column, Boolean, Integer, DateTime, Enum
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import UUIDType
from sqlalchemy_utils import database_exists, create_database

Base = declarative_base()
if not port:
    URL = f"mysql+pymysql://{user}:{password}@{host}/{db_name}"
else:
    URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"

ENGINE = create_engine(URL, echo=True)
SESSION = sessionmaker(bind=ENGINE)()


class BaseModel(Base):
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
    __tablename__ = 'vacancies'

    name = Column(String(100), nullable=False)
    desc = Column(String(500), nullable=False)
    hard_skills = Column(String(300), nullable=False)
    salary = Column(Integer, nullable=False)
    employment = Column(Enum('удаленно', 'смешанный график', 'в офисе'))

    def __init__(self, name, desc, hard_skills, salary, employment):
        self.name = name
        self.desc = desc
        self.hard_skills = hard_skills
        self.salary = salary
        self.employment = employment


def save_in_db(data, session=SESSION):
    obj = Vacancy(**data)
    session.add(obj)
    session.commit()


def setup_db(url=URL, engine=ENGINE):
    meta = MetaData()
    if not database_exists(url):
        create_database(url)
    meta.create_all(engine)
    Base.metadata.create_all(engine)
