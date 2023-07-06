from sqlalchemy import create_engine, select, Table, Column, Integer, DateTime, String,Date,JSON,PickleType, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import Users,Logs,Films,Actor,Actor_Friend,Base
from datetime import datetime
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
        session = sessionmaker(bind=engine)
        self.session = session()

    def user_exist(self, user_id):
        user = self.session.query(self.users).filter_by(user_id=user_id).first()
        if user:
            return True
        else:
            return False
    def user_add(self, user_id, username):
        user = self.users(user_id=user_id, username=username)
        self.session.add(user)
        self.session.commit()

    def get_user(self, user_id):
        user = self.session.query(self.users).filter_by(user_id=user_id).first()
        return user

    def delete_user(self, user_id):
        user = self.session.query(self.users).filter_by(user_id=user_id).first()
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        else:
            return False

    def add_log(self, username, user_id, message_text, message_time):
        log = Logs(username=username, user_id=user_id, message_text=message_text,
                   message_time=datetime.fromtimestamp(int(message_time)).strftime('%H:%M - %m.%d.%Y'))
        self.session.add(log)
        self.session.commit()

    def get_log(self, log_id):
        log = self.session.query(self.logs).filter_by(log_id=log_id).first()
        return log

    def delete_log(self, log_id):
        log = self.session.query(self.logs).filter_by(log_id=log_id).first()
        if log:
            self.session.delete(log)
            self.session.commit()
            return True
        else:
            return False

    def close(self):
        self.session.close()
