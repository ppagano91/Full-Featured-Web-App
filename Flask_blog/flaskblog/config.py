import os
from dotenv import load_dotenv
class Config:
    # Clave secreta para proteger de cookies, peticiones cruzadas, amenazas, etc
    # print(secrets.token_hex(16))
    SECRET_KEY ='4ecf2a614169e0866af7ee9d2172644e'
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres@localhost/db_flaskblog"
    SQLALCHEMY_TRACK_MODIFICATIONS =False


    MAIL_SERVER  = 'smtp.googlemail.com'
    MAIL_PORT  = 587
    MAIL_USE_TLS  = True

    # ENVIROMENT VARIABLES: https://www.youtube.com/watch?v=IolxqkL7cD8
    load_dotenv()
    MAIL_USERNAME  = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD  = os.environ.get('EMAIL_PASSWORD')