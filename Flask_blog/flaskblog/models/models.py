from datetime import datetime
from flaskblog import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    # min 23:30 SEGUIR

# Una vez que se establecieron los tipos de datos no se pueden cambiar. Cambiar desde SQL
class User(db.Model):
    __tablename__="Users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    image_file = db.Column(db.String(20), default="default.jpg")

    # El password será hasheado por lo tanto necesita más caracteres
    password = db.Column(db.String(100), nullable=False)

    # relationship('Post'...): hace referencia al modelo creado, no a la tabla, por lo tanto va en mayúsucla.
    posts = db.relationship("Post", backref="author", lazy=True)


    def __repr__(self):
        return f"User('{self.username}', User'{self.email}', User'{self.image_file}')"


class Post(db.Model):
    __tablename__="Posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    # Especificar las llaves mediante las cuales se relacionan las clases
    # user.id: el user hace referencia a la tabla creada por el modelo User, por lo tanto va en minúscula.
    user_id = db.Column(db.Integer, db.ForeignKey("Users.id"), nullable=False)
    # user = db.relationship('User', backref="Posts", lazy=True)

    def __repr__(self):
        return f"User('{self.title}', User'{self.date_posted}')"


# Crea las tablas de la base de datos. En caso de que exista no se ejecutará ni borrará la existente
# db.create_all()
