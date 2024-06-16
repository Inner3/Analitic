from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api, Resource
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import LargeBinary ,DECIMAL,Text,DATE


app = Flask(__name__)
CORS(app)  # Включение CORS для всех маршрутов
api = Api(app)

# Настройка подключения к базе данных
DATABASE_URI = 'postgresql://postgres:123@localhost:5432/manager'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Определение моделей базы данных с русскими именами
class Должность(Base):
    __tablename__ = 'Должность'
    id = Column(Integer, primary_key=True)
    Должность = Column(String, nullable=False)

class Команда(Base):
    __tablename__ = 'Команда'
    id = Column(Integer, primary_key=True)
    Команда = Column(String, nullable=False)

class Сотрудник(Base):
    __tablename__ = 'Сотрудник'
    id = Column(Integer, primary_key=True)
    Должность_id = Column(Integer, ForeignKey('Должность.id'))
    Команда_id = Column(Integer, ForeignKey('Команда.id'))
    Фамилия = Column(String, nullable=False)
    Имя = Column(String, nullable=False)
    Отчество = Column(String)
    номер_телефона = Column(String(20))
    Фото = Column(LargeBinary)
    Паспортные_данные = Column(Text)
    Должность = relationship("Должность")
    Команда = relationship("Команда")

class ГрафикРаботы(Base):
    __tablename__ = 'График_работы'
    id = Column(Integer, primary_key=True)
    Дата = Column(DateTime, nullable=False)
    Сотрудник_id = Column(Integer, ForeignKey('Сотрудник.id'))
    Тип_времени_id = Column(Integer, ForeignKey('Тип_времени.id'))
    Сотрудник = relationship("Сотрудник")
    Тип_времени = relationship("ТипВремени")

class ТипВремени(Base):
    __tablename__ = 'Тип_времени'
    id = Column(Integer, primary_key=True)
    Название = Column(String, nullable=False)

class Заявка(Base):
    __tablename__ = 'Заявка'
    id = Column(Integer, primary_key=True)
    Объект_id = Column(Integer)
    Статус_id = Column(Integer, ForeignKey('Статус.id'))
    Дата_создания = Column(DateTime)
    Дата_начала_работ = Column(DateTime)
    Дата_закрытия = Column(DateTime)
    Менеджер_id = Column(Integer, ForeignKey('Сотрудник.id'))
    Клиент_id = Column(Integer, ForeignKey('Клиент.id'))
    Комментарий = Column(Text)
    Стоимость = Column(DECIMAL)
    Статус = relationship("Статус")
    Менеджер = relationship("Сотрудник", foreign_keys=[Менеджер_id])
    Клиент = relationship("Клиент")

class Статус(Base):
    __tablename__ = 'Статус'
    id = Column(Integer, primary_key=True)
    Статус = Column(String, nullable=False)

class Клиент(Base):
    __tablename__ = 'Клиент'
    id = Column(Integer, primary_key=True)
    Фамилия = Column(String, nullable=False)
    Имя = Column(String, nullable=False)
    Отчество = Column(String)
    Мобильный_телефон = Column(String(20))

# Ресурс для получения данных о заявках
class ЗаявкиResource(Resource):
    def get(self):
        заявки = session.query(Заявка).all()
        result = []
        for з in заявки:
            result.append({
                'id': з.id,
                'Дата_создания': з.Дата_создания.isoformat() if з.Дата_создания else None,
                'Дата_начала_работ': з.Дата_начала_работ.isoformat() if з.Дата_начала_работ else None,
                'Дата_закрытия': з.Дата_закрытия.isoformat() if з.Дата_закрытия else None,
                'Статус': з.Статус.Статус,
                'Стоимость': з.Стоимость,
                'Менеджер': f"{з.Менеджер.Фамилия} {з.Менеджер.Имя} {з.Менеджер.Отчество}",
                'Клиент': f"{з.Клиент.Фамилия} {з.Клиент.Имя} {з.Клиент.Отчество}"
            })
        return jsonify(result)

# Ресурс для получения данных о графике работы
class ГрафикРаботыResource(Resource):
    def get(self):
        график_работы = session.query(ГрафикРаботы).all()
        result = []
        for г in график_работы:
            result.append({
                'Дата': г.Дата.isoformat() if г.Дата else None,
                'Сотрудник': f"{г.Сотрудник.Фамилия} {г.Сотрудник.Имя} {г.Сотрудник.Отчество}",
                'Тип_времени': г.Тип_времени.Название
            })
        return jsonify(result)

api.add_resource(ЗаявкиResource, '/заявки')
api.add_resource(ГрафикРаботыResource, '/график_работы')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
