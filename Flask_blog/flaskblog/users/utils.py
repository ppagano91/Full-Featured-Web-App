import os
import secrets
from PIL import Image
# Se reemplaza app --> current_app
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

def save_picture(form_picture):
    # No se guarda el nombre original de la imagen porque podría suceder que ya existiera ese nombre
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path=os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # Resizing image to 125x125 px
    output_size = (125,125)
    i=Image.open(form_picture)
    i.thumbnail(output_size)


    i.save(picture_path)
    return picture_fn


def send_reset_email(user):
    token=user.get_reset_token()
    # print("token: ",token)
    # print("user.email: ", user.email)
    msg=Message('Password Reset Request',
                sender="pagano.patricio@gmail.com",
                recipients=[user.email])
    msg.body=f'''To Reset your password, visit the following link:
    {url_for('users.reset_token', token=token, _external=True)}

    If you did no make this request then simply ignore this email and no changes will be made.
    '''

    mail.send(msg)