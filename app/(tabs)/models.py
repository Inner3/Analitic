from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Определение моделей базы данных с русскими именами
class Заявка(Base):
    __tablename__ = 'Заявка'
    id = Column(Integer, primary_key=True)
    дата_создания = Column(DateTime)
    дата_начала_работ = Column(DateTime)
    дата_закрытия = Column(DateTime)
    статус = Column(String)
    стоимость = Column(Float)

class ГрафикРаботы(Base):
    __tablename__ = 'График_работы'
    id = Column(Integer, primary_key=True)
    дата = Column(DateTime)
    сотрудник_id = Column(Integer, ForeignKey('Сотрудник.id'))
    тип_времени_id = Column(Integer, ForeignKey('Тип_времени.id'))
    сотрудник = relationship("Сотрудник")
    тип_времени = relationship("ТипВремени")

class Сотрудник(Base):
    __tablename__ = 'Сотрудник'
    id = Column(Integer, primary_key=True)
    фамилия = Column(String)
    имя = Column(String)
    отчество = Column(String)

class ТипВремени(Base):
    __tablename__ = 'Тип_времени'
    id = Column(Integer, primary_key=True)
    название = Column(String)