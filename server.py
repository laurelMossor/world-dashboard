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
    # THIS CREATES AN ERROR EACH LOAD

    # TEST for session info
    session_test = session.get("current_user_email", None)
    # If a user is logged in, establish session deets from DB
    if session_test != None:
        user = crud.get_user_email(session["current_user_email"])

        session["current_user_email"] = user.email
        session["current_user_name"] = user.username
        session["current_user_lang"] = user.preferred_lang
        session["current_user_keyword"] = user.news_search
    else:
        session["current_user_email"] = None
        session["current_user_lang"] = None
        session["current_user_keyword"] = None
        session["current_user_name"] = None

    return render_template("homepage.html", 
    ALL_COUNTRIES_LIST=ALL_COUNTRIES_LIST)


#################### LOGGIN IN AND OUT #####################
@app.route("/logout")
def logout():

    session["current_user_email"] = None
    session["current_user_name"] = None
    session["current_user_lang"] = None
    session["curent_user_keyword"] = None
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
                # TODO: MOVE THIS UP TO HOME
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

    # Add to session
    session["current_user_lang"] = source_language_preference
    # Add to Database
    user = crud.get_user_email(session["current_user_email"])
    user.preferred_lang = source_language_preference
    db.session.add(user)
    db.session.commit()

    return redirect("/user-profile")

@app.route("/user-profile/keyword-search-term", methods=["POST"])
def keyword_search_term():
    """Adds keyword search term to database and session"""

    keyword_search_term = request.form.get("keyword-search")
    # Add to session 
    session["current_user_keyword"] = keyword_search_term
    # Add to database
    user = crud.get_user_email(session["current_user_email"])
    user.news_search = keyword_search_term
    db.session.add(user)
    db.session.commit()

    return redirect("/user-profile")

@app.route("/user-profile/reset-preferences")
def reset_preferences():
    """Resets the users preferences in the database and session"""

    user = crud.get_user_email(session["current_user_email"])
    user.news_search = None
    user.preferred_lang = None
    db.session.add(user)
    db.session.commit()

    session["current_user_keyword"] = None
    session["current_user_lang"] = None

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
    if session["current_user_keyword"] != None:
        payload["q"] = session["current_user_keyword"] + " " + country_name

    if session["current_user_lang"] != None:
        payload["language"] = session["current_user_lang"]

    news_res = requests.get(news_url, params=payload)
    print(news_res.url)
    news_data = news_res.json()
    articles = news_data["articles"]

    return jsonify(articles)


# @app.route("/api/world-map")
# def world_map():



#     return redirect("/")

###########################################################
if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug = True)