from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
    
class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(250))
    points = Column(Integer, default=50)
    role = Column(String(20), default='user')
class Logs(Base):
    __tablename__ = 'logs'
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(250))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship('Users', backref='logs')
    message_text = Column(String(1000))
    message_time = Column(String(100))