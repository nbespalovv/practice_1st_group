from sqlalchemy import create_engine, select, Table, Column, Integer, DateTime, String,Date,JSON,PickleType, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_nickname = Column(String(250))
    points = Column(Integer, default=50)
    role = Column(String(20), default='user')

class Films(Base):
    __tablename__ = 'films'
    id_film = Column(Integer, primary_key=True)
    name = Column(String(250))
    parental_control = Column(PickleType)
    country = Column(String(60))
    genre = Column(JSON)

class Actor(Base):
    __tablename__ = 'actor'
    id_actor = Column(Integer, primary_key=True)
    name = Column(String(250))
    gender = Column(String(10))
    birthdate = Column(Date)
    id_film = Column(Integer, ForeignKey('films.id_film'))


class Actor_Friend(Base):
    __tablename__ = 'actor_friend'
    id_friend_actor = Column(Integer, primary_key=True)
    name = Column(String(250))
    gender = Column(String(20))
    birthdate = Column(Date)
    id_actor = Column(Integer, ForeignKey('actor.id_actor'))

class Logs(Base):
    __tablename__ = 'logs'
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    user_nickname = Column(String(250))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    message_text = Column(String(1000))
    message_time = Column(String(100))


class BotDB:
    def __init__(self):
        self.films = Films
        self.actor = Actor
        self.actor_friend = Actor_Friend
        self.users = Users
        self.logs = Logs
        f = open('config.txt')
        username = f.readline().replace('\n', '')
        password = f.readline().replace('\n', '')
        db = f.readline().replace('\n', '')
        f.close()
        engine = create_engine(f"mysql+pymysql://{username}:{password}@{db}")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def user_exist(self, user_id):
        stmt = select(self.users).where(self.users.user_id == user_id)
        result = self.session.execute(stmt).fetchone()
        if result is not None:
            return True
        else:
            return False

    def user_add(self, user_id, user_nickname):
        user = self.users(user_id=user_id, user_nickname=user_nickname)
        self.session.add(user)
        self.session.commit()

    def get_user(self, user_id):
        user = self.session.query(self.users).filter_by(user_id=user_id).first()
        if user:
            return user.user_first_name
        else:
            return None

    def delete_user(self, user_id):
        user = self.session.query(self.users).filter_by(user_id=user_id).first()
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        else:
            return False

    def add_log(self, user_nickname, user_id, message_text, message_time):
        log = self.logs(user_nickname=user_nickname, user_id=user_id, message_text=message_text,
                        message_time=datetime.fromtimestamp(message_time).strftime('%H:%M - %m.%d.%Y'))
        self.session.add(log)
        self.session.commit()

    def close(self):
        self.session.close()
