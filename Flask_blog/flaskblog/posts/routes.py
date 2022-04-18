from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostsForm



posts=Blueprint('posts',__name__)



@posts.route("/posts/new", methods=['GET','POST'])
@login_required
def new_post():
    form=PostsForm()

    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!','success')
        return redirect(url_for('main.home'))

    return render_template('create_post.html', title='New Post', form=form, legened="New post")



@posts.route("/posts/<int:post_id>", methods=['GET','POST'])
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route("/posts/<int:post_id>/update", methods=['GET','POST'])
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
        return redirect(url_for('posts.post',post_id=post.id))

    elif request.method== "GET":
        # Inicializar los datos del formulario con lo que haya en la Tabla Posts de la BD
        form.title.data=post.title
        form.content.data=post.content


    return render_template('create_post.html', title="Update post", form=form, legened="Update post")


@posts.route("/posts/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)

    if post.author !=current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()

    flash("Your post has been deleted!","success")

    return redirect(url_for('main.home'))