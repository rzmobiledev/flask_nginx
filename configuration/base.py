import os
from dotenv import load_dotenv
from flask import Flask
from sqlalchemy.orm import DeclarativeBase
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

load_dotenv()


class Base(DeclarativeBase):
    pass


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")
db = SQLAlchemy(app=app, model_class=Base)
bcrypt = Bcrypt(app)


def encrypt(password: str):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    return hashed_password


def is_valid(password: str, encrypted_password) -> bool:
    return bcrypt.check_password_hash(encrypted_password, password)