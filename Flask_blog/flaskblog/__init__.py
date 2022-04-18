from dotenv import load_dotenv
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config
# import sqlalchemy
# import secrets
# from sqlalchemy import create_engine, MetaData

from sqlalchemy_utils import database_exists, create_database
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine




app = Flask(__name__)
app.config.from_object(Config)

# Configurar del Motor de base de datos (engine database)
engine = create_engine("postgresql+psycopg2://postgres@localhost/db_flaskblog")



db = SQLAlchemy(app)

# Bycrypt
bcrypt = Bcrypt(app)

# Login
login_manager = LoginManager(app)
# login_manager.login_view='<function name of a route>'
login_manager.login_view='users.login'
login_manager.login_message_category='info'



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


