from sqlalchemy import create_engine, select, Table, Column, Integer, DateTime, String, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_nickname = Column(String(250))


class Logs(Base):
    __tablename__ = 'logs'
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    user_nickname = Column(String(250))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    message_text = Column(String(1000))
    message_time = Column(String(100))


class BotDB:
    def __init__(self):
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
