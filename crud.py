"""CRUD operations."""
import json

from model import db, connect_to_db, User

# Database is called 'dashboard-users'
# testuser = User(email="test@test.com", password="test")

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def check_user_email(x_email):
    
    return User.query.filter(User.email == x_email).first()

def get_user_password(x_email, x_password):

    x_user = User.query.filter(User.email == x_email).first()   
    return x_user.password



with open("world-countries.json") as file:
    all_countries_list = json.loads(file.read())

all_countries_dict = {}
# Loop over to create dictionary
for country in all_countries_list:
    all_countries_dict[country[1]] = country[0]



if __name__ == '__main__':
    from server import app
    connect_to_db(app)
