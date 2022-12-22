import enum
import logging

from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

from app.config import DATABASE

log = logging.getLogger('main.database')

Base = declarative_base()


class AdminStatus(enum.Enum):
    admin = 'Админ'
    super_admin = 'Супер Админ'


class Admin(Base):
    __tablename__ = "Admins"
    id = Column(Integer, autoincrement=True, primary_key=True)
    telegram_username = Column(String)
    telegram_id = Column(Integer)
    status = Column(Enum(AdminStatus), nullable=False)


class Village(Base):
    __tablename__ = "villages"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    card = relationship("Card", back_populates="village")


class Services(Base):
    __tablename__ = "services"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    type_service = relationship("TypeServices", back_populates="service")


class TypeServices(Base):
    __tablename__ = "type_services"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    services_id = Column(Integer, ForeignKey('services.id'))
    service = relationship("Services", back_populates="type_service")
    card = relationship("Card", back_populates="type_services")


class Card(Base):
    __tablename__ = "crads"
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String)
    description = Column(String)
    site_link = Column(String)
    picture_link = Column(String)
    type_service_id = Column(Integer, ForeignKey('type_services.id'))
    type_services = relationship("TypeServices", back_populates="card")
    village_id = Column(Integer, ForeignKey('villages.id'))
    village = relationship("Village", back_populates="card")
    active = Column(Boolean)


engine = create_engine(URL.create(**DATABASE), pool_size=10, max_overflow=30)
if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
