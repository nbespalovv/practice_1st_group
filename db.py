from sqlalchemy import create_engine, select, Table, Column, Integer,   String, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    user_first_name = Column(String(250))


class Book(Base):
    __tablename__ = 'Books'

    id_book = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    genre = Column(String(250))
    price = Column(Integer, nullable=False)

class BotDB:
    def __init__(self,username,password,db):
        self.users = Users
        self.book = Book
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

    def user_add(self, user_id, user_first_name):
        user = self.users(user_id=user_id, user_first_name=user_first_name)
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

    def close(self):
        self.session.close()


