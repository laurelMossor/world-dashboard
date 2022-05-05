"""Models for world dashboard app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_to_db(flask_app, db_uri="postgresql:///dashboard-users", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

# Database is called 'dashboard-users'
# testuser = User(email="test@test.com", password="test")

class User(db.Model):
    """A user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, 
                        autoincrement=True, 
                        primary_key=True)
    username = db.Column(db.String(25), unique=False, default="Friend")
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    preferred_currency = db.Column(db.String(50), default="USD")
    preferred_lang = db.Column(db.String(50), default="None")
    news_search = db.Column(db.String(50), default="None")

    def __repr__(self):
        return f'<User: user_id={self.user_id} email={self.email}>'



if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
