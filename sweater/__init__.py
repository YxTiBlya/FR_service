import os


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.secret_key = 'SUPER PUPER SECRET KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@{os.environ.get('DB_ADDRES')}/{os.environ.get('POSTGRES_DB')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
manager = LoginManager(app)

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDIxMDgzNTQsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Inl4dGlibHlhIn0.WezPadhZhBfgtHnb_NOt8PVrtewVuGokNLjqAHOwifE"
service = "https://probe.fbrq.cloud/v1/send"