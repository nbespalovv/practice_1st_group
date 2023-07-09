from sqlalchemy import create_engine, select, Table, Column, Integer, DateTime, String,Date,JSON,PickleType, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import Users,Logs,Films,Actor,Base
from datetime import datetime
import json
class BotDB:
    def __init__(self):
        self.films = Films
        self.actors = Actor
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
    def user_add(self, user_id, username,role):
        user = self.users(user_id=user_id, username=username,role=role, reg_data=datetime.now())
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
    def user_update(self, user):
        user_db = self.session.query(self.users).filter_by(user_id=user.user_id).first()
        user_db = user
        self.session.commit()

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
    def film_exist(self, id_film):
        film = self.session.query(self.films).filter_by(id_film=id_film).first()
        if film:
            return True
        else:
            return False
    def add_film(self, info_films):
        film = Films(name =info_films[0] ,id_film=info_films[1] ,parental_control = info_films[2],country = info_films[3], genre = info_films[4], employees = info_films[5])
        self.session.add(film)
        self.session.commit()

    def actor_exist(self, id_actor):
        actor = self.session.query(self.actors).filter_by(id_actor=id_actor).first()
        if actor:
            return True
        else:
            return False
    def add_actor(self, info_actor):
        actor = Actor(id_actor = info_actor[0][0], name =info_actor[1], gender =info_actor[2], birthdate =info_actor[3], id_film =info_actor[4])
        self.session.add(actor)
        self.session.commit()

    #def add_actor_friend(self, info_actor):
        #    actor = Actor(id_actor = info_actor[0][0], name =info_actor[1], gender =info_actor[2], birthdate =info_actor[3], id_actor = info_actor[4][0])
        #    self.session.add(actor)
    #   self.session.commit()

    def close(self):
        self.session.close()
