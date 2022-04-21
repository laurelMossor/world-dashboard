from flask import (Flask, redirect, request, 
            render_template, jsonify, flash, session)
from model import connect_to_db, db, User
from jinja2 import StrictUndefined

import json
import os
import requests
import crud 

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

NEWS_API_KEY = os.environ['NEWS_API_KEY']
ALL_COUNTRIES_LIST = crud.all_countries_list
ALL_COUNTRIES_DICT = crud.all_countries_dict
NEWS_LANGUAGES = crud.NEWS_LANGUAGES



@app.route("/")
def homepage():
    """App landing page and establish session details"""

    # Establish session details
    user = crud.get_user_email(session["current_user_email"])
    # If a user is logged in, establish session deets from DB
    if user != None:
        session["current_user_email"] = user.email
        session["current_user_name"] = user.username
        session["current_user_lang"] = user.preferred_lang
    else:
        session["current_user_lang"] = None
        session["current_user_email"] = None

    return render_template("homepage.html", 
    ALL_COUNTRIES_LIST=ALL_COUNTRIES_LIST)


#################### LOGGIN IN AND OUT #####################
@app.route("/logout")
def logout():

    session["current_user_email"] = None
    session["current_user_name"] = None
    session["current_user_lang"] = None
    flash("You have been logged out.")

    return redirect("/")

@app.route("/login-page")
def login():
    """Log in or create an account"""

    return render_template("login-page.html")

@app.route("/login-page/user-login", methods=["POST"])
def user_login():

    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_email(email)

    if user == None:
        flash("Please create an account.")
    else:
        if crud.get_user_password(email) == password:
            flash("You are logged in!")
            session["current_user_email"] = user.email
            if crud.check_for_username(user.email) == None:
                session["current_user_name"] = "Friend"
            else:
                session["current_user_name"] = crud.check_for_username(user.email)
        else:
            flash("Those passwords don't match.")
    
    return redirect("/login-page")

@app.route("/create-account-page")
def create_account():

    return render_template("create-account-page.html")

@app.route("/create-account-page/create-account", methods=["POST"])
def create_user():

    email = request.form.get("email")
    password = request.form.get("password")
    output = crud.get_user_email(email)
    new_user = User(email=email, password=password)

    if output != None:
        flash("Oh no! That email is already in use. Try logging in.")
    else:
        flash("Great! You created an account. Now please log in.")
        db.session.add(new_user)
        db.session.commit()

    return redirect("/create-account-page")

#################### PROFILE AND PREFERENCES #####################
@app.route("/user-profile")
def user_profile():

    return render_template("user-profile.html", 
    NEWS_LANGUAGES=NEWS_LANGUAGES)

@app.route("/user-profile/create-username", methods=["POST"])
def create_username():
    """Adds username to database and session"""

    new_username = request.form.get("create-username")
    flash(f"Wonderful, we'll call you {new_username}.")
    session["current_user_name"] = new_username

    user = crud.get_user_email(session["current_user_email"])
    user.username = new_username
    db.session.add(user)
    db.session.commit()

    return redirect("/user-profile")

@app.route("/user-profile/source-language", methods=["POST"])
def source_language():
    """Adds language preference to database and session"""

    source_language_preference = request.form.get("language-dropdown")

    # Add to session, here and at logout
    session["current_user_lang"] = source_language_preference
    # Add to Database
    user = crud.get_user_email(session["current_user_email"])
    user.preferred_lang = source_language_preference
    db.session.add(user)
    db.session.commit()

    # Have news reflect change 

    return redirect("/user-profile")

###################### CALLING APIs #############################
@app.route("/api/news-by-country-name")
def news_by_country_name():
    """Call the News API with the NAME"""

    two_dig_country_code = request.args.get("twoDigCountryCode")
    country_name = ALL_COUNTRIES_DICT[two_dig_country_code.upper()]

    news_url = "https://newsapi.org/v2/everything"

    payload = {
        "apikey": NEWS_API_KEY, 
        "q": country_name,
        "sortBy": "relevancy",
        "pageSize": "5",
    }
    # IF there are keywords or language preferences,
    # Add them to the payload dict 
        # payload["language"] = "en"
    
    if session["current_user_lang"] != None:
        payload["language"] = session["current_user_lang"]

    news_res = requests.get(news_url, params=payload)
    news_data = news_res.json()
    print(news_res.url)
    articles = news_data["articles"]

    return jsonify(articles)

###########################################################
if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug = True)