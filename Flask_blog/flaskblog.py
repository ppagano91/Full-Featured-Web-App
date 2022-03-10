from flask import Flask, render_template,url_for,flash,redirect,request
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from forms import RegistrationForm, LoginForm
import secrets

from datetime import datetime

from sqlalchemy import create_engine, MetaData
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base


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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), default='default.jpg')

    #El password será hasheado por lo tanto necesita más caracteres
    password = db.Column(db.String(60), nullable=False)

    # relationship('Post'...): hace referencia al modelo creado, no a la tabla, por lo tanto va en mayúsucla.

    posts = db.relationship("Post",backref="author",
    lazy="True")



    def __repr__(self):
        return f"User('{self.username}', User'{self.email}', User'{self.email}', User'{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    # Especificar las llaves mediante las cuales se relacionan las clases
    # user.id: el user hace referencia a la tabla creada por el modelo User, por lo tanto va en minúscula.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.title}', User'{self.date_posted}')"


posts=[{
    "author":"Corey Schafer",
    "title":"Blog post 1",
    "content":"First post content",
    "data_posted":"April 20,2018"
},
{
    "author":"Jane Doe",
    "title":"Blog post 2",
    "content":"Second post content",
    "data_posted":"April 21,2018"
}]


# Crea las tablas de la base de datos. En caso de que exista no se ejecutará ni borrará la existente
db.create_all()



@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/register", methods=["POST","GET"])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('home'))

    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=["POST","GET"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "password":
            flash(f'You hava been logged in!','success')
            return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check your username and password','danger')
    return render_template("login.html", title="Login", form=form)

if __name__== '__main__':
    app.run(debug=True)