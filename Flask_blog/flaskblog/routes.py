import os
import secrets

from PIL import Image

from flask import Flask, render_template,url_for,flash,redirect,request, abort
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostsForm, RequestResetForm, ResetPasswordForm
from flaskblog.models.models import User,Post

# For Login
from flask_login import login_user, current_user, logout_user, login_required

# For mail
from flask_mail import Message



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
























