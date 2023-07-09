import os
from os import getenv
from os.path import exists
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DOTENV_PATH = "../.env"

if exists(DOTENV_PATH):
    load_dotenv(DOTENV_PATH)

USER = getenv("DB_USER") or "root" #os.environ.get("POSTGRES_USER")
PASSWORD = getenv("DB_PASSWORD") or "password" #os.environ.get("POSTGRES_PASSWORD")
DB_NAME = getenv("DB_NAME") or "" #os.environ.get("POSTGRES_DB")
HOST = getenv("DB_URL") or "localhost"
DB_PORT = "3306"

db_url = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{DB_PORT}/{DB_NAME}" #DB_NAME не нужен возможно, также в .env

print(db_url)


engine = create_engine(db_url, pool_size=20, max_overflow=0)
session = sessionmaker(engine)