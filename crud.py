"""CRUD operations."""
import json
from model import db, connect_to_db, User


##### Create all_countries_list and all_countries_dict #####
with open("world-countries.json") as file:
    all_countries_list = json.loads(file.read())
    # The LIST is county[0], code[1]

all_countries_dict = {}
for country in all_countries_list:
    all_countries_dict[country[1]] = country[0].lower()
    # The DICT is code[0], country[1]

NEWS_LANGUAGES = [["None", "[Default/None]"], ["ar", "Arabic"], 
["de", "German"], ["en", "English"], 
["es", "Spanish"], ["fr", "French"], 
["he", "Hebrew"], ["it", "Italian"], ["nl", "Dutch"], 
["no", "Norwegian"], ["pt", "Portuguese"], 
["ru", "Russian"], ["se", "Swedish"], 
["ud", "Ukrainian"], ["zh", "Chinese"]]


# Database is called 'dashboard-users'
# testuser = User(email="test@test.com", password="test")
def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)
    return user

def get_user_email(x_email):
    """Returns the first user with the email provided"""
    
    return User.query.filter(User.email == x_email).first()

def get_user_password(x_email):
    """Returns the PASSWORD of the user w/ the provided email"""

    x_user = User.query.filter(User.email == x_email).first()   
    return x_user.password

    
def check_for_username(x_email):
    """Returns the USERNAME of the user w/ provided email"""

    user = User.query.filter(User.email == x_email).first()
    return user.username






if __name__ == '__main__':
    from server import app
    connect_to_db(app)
