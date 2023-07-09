from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Date, PickleType
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()



class Films(Base):
    __tablename__ = 'films'
    id_film = Column(Integer, primary_key=True)
    name = Column(String(250))
    parental_control = Column(PickleType)
    country = Column(JSON)
    genre = Column(JSON)
    employees = Column(PickleType)

class Actor(Base):
    __tablename__ = 'actor'
    id_actor = Column(Integer, primary_key=True)
    name = Column(String(250))
    gender = Column(String(10))
    birthdate = Column(Date)
    #id_film = Column(Integer, ForeignKey('films.id_film'))
    id_film = Column(JSON)


class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(250))
    age = Column(Integer,default=0)
    reg_data = Column(Date)
    email = Column(String(50),default="Отсутствует")
    phone = Column(String(20),default="Отсутствует")
    history = Column(JSON)
    favourite = Column(JSON)
    points = Column(Integer, default=50)
    role = Column(String(20), default='User')
class Logs(Base):
    __tablename__ = 'logs'
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(250))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship('Users', backref='logs')
    message_text = Column(String(1000))
    message_time = Column(String(100))
