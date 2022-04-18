from flask import render_template,request,Blueprint
from flaskblog.models.models import Post

main=Blueprint('main',__name__)


@main.route("/")
@main.route("/home")
def home():
    # Obtener la página del html
    page=request.args.get('page',default=1,type=int)

    # Obtener todos los datos
    # posts=Post.query.all()

    # Obtener los datos por páginas, 5 post por página --> para ver: http://127.0.0.1:5000/?page=<number>
    # posts=Post.query.paginate(per_page=5,page=page)
    posts=Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5,page=page)
    return render_template("home.html", posts=posts)


@main.route("/about")
def about():
    return render_template("about.html", title="About")