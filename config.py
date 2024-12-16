from peewee import *
from flask import Flask

import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config.from_object(__name__)

app.secret_key = 'SECRET_KEY'

db = PostgresqlDatabase(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

class model(Model):
    class Meta:
        database = db

    def to_dict(self):
        return {key: value for key, value in self.__data__.items()}