from this import d
from flask import Flask, render_template,url_for,flash,redirect,request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models.models import User,Post

# For Login
from flask_login import login_user


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
        # decode('utf-8'): para cambiar el hash de bytes a string
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your Account has been created! You are now able to log in','success')
        return redirect(url_for('login'))

    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=["POST","GET"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'You have been logged in!','success')
            return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check your email and password','danger')
    return render_template("login.html", title="Login", form=form)