import os
import secrets

from PIL import Image

from flask import Flask, render_template,url_for,flash,redirect,request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostsForm, RequestResetForm, ResetPasswordForm
from flaskblog.models.models import User,Post

# For Login
from flask_login import login_user, current_user, logout_user, login_required



#  Dummy data
# posts=[{
#     "author":"Corey Schafer",
#     "title":"Blog post 1",
#     "content":"First post content",
#     "date_posted":"April 20,2018"
# },
# {
#     "author":"Jane Doe",
#     "title":"Blog post 2",
#     "content":"Second post content",
#     "date_posted":"April 21,2018"
# }]



@app.route("/")
@app.route("/home")
def home():
    # Obtener la página del html
    page=request.args.get('page',default=1,type=int)

    # Obtener todos los datos
    # posts=Post.query.all()

    # Obtener los datos por páginas, 5 post por página --> para ver: http://127.0.0.1:5000/?page=<number>
    # posts=Post.query.paginate(per_page=5,page=page)
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5,page=page)
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


# REGISTER
@app.route("/register", methods=["POST","GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # Se crea una instancia de la clase RegistrationForm, la cual se utiliza para hacer el formulario (labels e inputs) en register.html
    form=RegistrationForm()

    # Si el formulario es válido, todos los campos requeridos están completos, este if es True
    # En caso contrario aparecerán los avisos de campos incompletos
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page=request.args.get('next')
            flash(f'You have been logged in!','success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessful. Please check your email and password','danger')
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    # No se guarda el nombre original de la imagen porque podría suceder que ya existiera ese nombre
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path=os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    # Resizing image to 125x125 px
    output_size = (125,125)
    i=Image.open(form_picture)
    i.thumbnail(output_size)


    i.save(picture_path)
    return picture_fn

@app.route("/account", methods=["POST","GET"])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file=picture_file

        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash("Your account has been updated!","success")
        return redirect(url_for('account'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
    image_file=url_for('static', filename='profile_pics/'+current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/posts/new", methods=['GET','POST'])
@login_required
def new_post():
    form=PostsForm()

    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!','success')
        return redirect(url_for('home'))

    return render_template('create_post.html', title='New Post', form=form, legened="New post")



@app.route("/posts/<int:post_id>", methods=['GET','POST'])
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/posts/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)

    if post.author !=current_user:
        abort(403)

    form = PostsForm()

    if form.validate_on_submit():
        # Guardar/Actualizar los datos en la BD
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash('Your post has been updated!',"success")
        return redirect(url_for('post',post_id=post.id))

    elif request.method== "GET":
        # Inicializar los datos del formulario con lo que haya en la Tabla Posts de la BD
        form.title.data=post.title
        form.content.data=post.content


    return render_template('create_post.html', title="Update post", form=form, legened="Update post")


@app.route("/posts/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)

    if post.author !=current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()

    flash("Your post has been deleted!","success")

    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page=request.args.get('page',default=1,type=int)
    user=User.query.filter_by(username=username).first_or_404()
    posts=Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(per_page=5,page=page)
    return render_template("user_posts.html", posts=posts, user=user)


def send_reset_email(user):
    pass

@app.route("/reset_password", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form=RequestResetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password','info')
        return redirect(url_for('login'))

    return render_template('reset_request.html', title="Reset Password", form=form)


@app.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    user=User.verify_reset_token(token)

    if user is None:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for('reset_request'))

    form = ResetPasswordForm()
    return render_template('reset_token.html', title="Reset Password", form=form)

