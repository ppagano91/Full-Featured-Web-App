from dotenv import load_dotenv
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

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
login_manager.login_view='users.login'
login_manager.login_message_category='info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

# ENVIROMENT VARIABLES: https://www.youtube.com/watch?v=IolxqkL7cD8
load_dotenv()
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')

# Acceso de aplicaciones menos seguras en Google para enviar mail
mail=Mail(app)



# db.create_engine('postgresql+psycopg2://postgres@localhost/db_flaskblog',{})
# Crear una instancia del base de datos
# SQL Alchemy representa la estrucutra de base de datos mediante clases llamadas módulos
# Crear la Base de Datos

if not database_exists(engine.url):
    create_database(engine.url)

# Crear las tablas definidas como modelos
db.create_all()

from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)


