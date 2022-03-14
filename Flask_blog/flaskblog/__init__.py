from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# import sqlalchemy

# import secrets
# from sqlalchemy import create_engine, MetaData
# from sqlalchemy_utils import database_exists, create_database
# from sqlalchemy.ext.declarative import declarative_base


app = Flask(__name__)

# Clave secreta para proteger de cookies, peticiones cruzadas, amenazas, etc
# print(secrets.token_hex(16))
app.config['SECRET_KEY']='4ecf2a614169e0866af7ee9d2172644e'
app.config['SQLALCHEMY_DATABASE_URI']= "postgresql+psycopg2://postgres@localhost/db_flaskblog"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
# db.create_engine('postgresql+psycopg2://postgres@localhost/db_flaskblog',{})
# Crear una instancia del base de datos
# SQL Alchemy representa la estrucutra de base de datos mediante clases llamadas módulos


from flaskblog import routes