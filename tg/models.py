from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()



class Films(Base):
    __tablename__ = 'films'
    id_film = Column(Integer, primary_key=True)
    name = Column(String(250))

class Film_Country(Base):
    __tablename__ = 'film_country'
    id_film_country = Column(Integer, primary_key=True, autoincrement=True)
    id_film = Column(Integer, ForeignKey('films.id_film'))
    country = Column(String(100))

class Film_Genre(Base):
    __tablename__ = 'film_genre'
    id_film_genre = Column(Integer, primary_key=True, autoincrement=True)
    id_film = Column(Integer, ForeignKey('films.id_film'))
    genre = Column(String(100))

class Parental_Control(Base):
    __tablename__ = 'parental_control'
    id_parental_control = Column(Integer, primary_key=True, autoincrement=True)
    id_film = Column(Integer, ForeignKey('films.id_film'))
    danger = Column(String(100))
    level = Column(String(20))

class Actor(Base):
    __tablename__ = 'actor'
    id_actor = Column(Integer, primary_key=True)
    name = Column(String(250))
    gender = Column(String(10))
    birthdate = Column(Date)
    is_checked = Column(Boolean, default=False)

class Film_Actor(Base):
    __tablename__ = 'film_actor'
    id_film_actor = Column(Integer, primary_key=True, autoincrement=True)
    id_actor = Column(Integer, ForeignKey('actor.id_actor'))
    id_film = Column(Integer, ForeignKey('films.id_film'))
    amplua = Column(String(40))


class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(250))
    age = Column(Integer,default=0)
    reg_data = Column(Date)
    email = Column(String(50),default="Отсутствует")
    phone = Column(String(20),default="Отсутствует")
    points = Column(Integer, default=50)
    role = Column(String(20), default='User')

class History(Base):
    __tablename__ = 'history'
    id_history = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    request = Column(String(250))
    date = Column(Date)
    is_favourite = Column(Boolean, default=False)
class Logs(Base):
    __tablename__ = 'logs'
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(250))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship('Users', backref='logs')
    message_text = Column(String(1000))
    message_time = Column(String(100))
