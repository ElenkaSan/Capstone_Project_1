from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect this database to provided Flask app """
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User in the system """

    __tablename__ = 'users'

    id = db.Column(
         db.Integer,
         primary_key=True)

    username = db.Column(
               db.Text,
               nullable=False,
               unique=True)

    password = db.Column(
               db.Text,
               nullable=False)

    email = db.Column(
            db.Text,
            nullable=False,
            unique=True)

    notes = db.Column(
            db.Text)

    favorites = db.relationship('Favorite')

    
    @classmethod
    def serialize(self):
        """ Serialize User instance for JSON """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'notes': self.notes,
        }

    def __repr__(self):
        return f'<User #{self.id}: {self.username}, {self.email}>'

    @classmethod
    def signup(cls, username, email, password, notes):
        """Sign up user.
        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            notes=notes)

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.
        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.
        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

class Recipe(db.Model):
    __tablename__ = 'recipes' 

    id = db.Column(
         db.Integer,
         primary_key=True)
    
    title = db.Column(
            db.String,
            nullable=False)
   
    image = db.Column(
            db.String, 
            nullable=False)
    
    readyInMinutes = db.Column(
                     db.Integer)

    servings = db.Column(
               db.Integer)

    sourceName = db.Column(
                 db.String)

    sourceUrl = db.Column(
                db.String)

    users = db.relationship('User',
                            secondary='favorites',
                            backref='recipes', 
                            lazy=True)

    favorites = db.relationship('Favorite')

    @property
    def recipe_name(self):
       return f'{self.title}'

    def serialize(self):
        """Returns a dict representation of recipes which we can turn into JSON"""
        return {
            'id': self.id,
            'title': self.title,
            'img_url': self.image,
            'prep_time': self.readyInMinutes,
            'serves': self.servings,
            'source_name': self.sourceName,
            'source_url': self.sourceUrl
        }

    def __repr__(self):
        return f'<Recipe = id:{self.id}, title:{self.title}, source_name:{self.sourceName}>'

class Favorite(db.Model):
    """ Many to Many Users to Recipes """
    __tablename__ = "favorites"

    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='cascade'), 
                        primary_key=True)
    recipe_id = db.Column(db.Integer, 
                          db.ForeignKey('recipes.id', ondelete='cascade'),
                          primary_key=True)

    def __repr__(self):
        return f'<Favorite= user_id:{self.user_id} recipe_id:{self.recipe_id}>'

