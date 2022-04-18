from flask import (Flask, redirect, request, 
            render_template, jsonify, flash, session)
from model import connect_to_db, db, User
from jinja2 import StrictUndefined

import json
import os
import requests
import crud 
# Includes all_countries_list/dict

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

NEWS_API_KEY = os.environ['NEWS_API_KEY']


@app.route("/")
def homepage():
    """App landing page"""

    # session["current_user"] = None

    return render_template("homepage.html")

@app.route("/login-page")
def login():
    """Log in or create an account"""

    return render_template("login-page.html")

@app.route("/user-login", methods=["POST"])
def user_login():

    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.check_user_email(email)

    if user == None:
        flash("Please create an account.")
    else:
        if crud.get_user_password(email, password) == password:
            flash("You are logged in!")
            session["current_user"] = user.email
        else:
            flash("Those passwords don't match.")
    
    return redirect("/login-page")

@app.route("/create-account-page")
def create_account():

    return render_template("create-account-page.html")

@app.route("/create-account", methods=["POST"])
def create_user():

    email = request.form.get("email")
    password = request.form.get("password")
    output = crud.check_user_email(email)
    new_user = User(email=email, password=password)

    if output != None:
        flash("Oh no! That email is already in use.")
    else:
        flash("Great! You created an account. Now please log in.")
        db.session.add(new_user)
        db.session.commit()

    return redirect("/create-account-page")

@app.route("/user-profile")
def user_profile():

    return render_template("user-profile.html")

@app.route("/news-country")
def news_country():
    """Call the News API"""

    # 2-digit country code from form
    two_dig_country_code = request.args.get("twoDigCountryCode")

    # News API information gathering
    news_url = "https://newsapi.org/v2/top-headlines"
    news_payload = {
        "apikey": NEWS_API_KEY, 
        "country": two_dig_country_code,
        "pageSize": "5",
    }
    news_res = requests.get(news_url, params=news_payload)
    news_data = news_res.json()
    articles = news_data["articles"]

    return jsonify(articles)


    
if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug = True)