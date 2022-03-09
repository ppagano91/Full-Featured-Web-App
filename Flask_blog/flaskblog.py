from flask import Flask, render_template,url_for,flash,redirect,request
from forms import RegistrationForm, LoginForm
import secrets


app = Flask(__name__)

# Clave secreta para proteger de cookies, peticiones cruzadas, amenazas, etc
# print(secrets.token_hex(16))
app.config['SECRET_KEY']='4ecf2a614169e0866af7ee9d2172644e'

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