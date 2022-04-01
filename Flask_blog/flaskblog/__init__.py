from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# import sqlalchemy

# import secrets
# from sqlalchemy import create_engine, MetaData
from sqlalchemy_utils import database_exists, create_database
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


app = Flask(__name__)

# Configurar del Motor de base de datos (engine database)
engine = create_engine("postgresql+psycopg2://postgres@localhost/db_flaskblog")

# Clave secreta para proteger de cookies, peticiones cruzadas, amenazas, etc
# print(secrets.token_hex(16))
app.config['SECRET_KEY']='4ecf2a614169e0866af7ee9d2172644e'
app.config['SQLALCHEMY_DATABASE_URI']= "postgresql+psycopg2://postgres@localhost/db_flaskblog"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)

# Bycrypt
bcrypt = Bcrypt(app)

# Login
login_manager = LoginManager(app)
# login_manager.login_view='<function name of a route>'
login_manager.login_view='login'
login_manager.login_message_category='info'

# db.create_engine('postgresql+psycopg2://postgres@localhost/db_flaskblog',{})
# Crear una instancia del base de datos
# SQL Alchemy representa la estrucutra de base de datos mediante clases llamadas módulos
# Crear la Base de Datos

if not database_exists(engine.url):
    create_database(engine.url)

# Crear las tablas definidas como modelos
db.create_all()

from flaskblog import routes