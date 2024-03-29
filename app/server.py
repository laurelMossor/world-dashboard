from flask import (Flask, redirect, request, 
            render_template, jsonify, flash, session)
from model import connect_to_db, db, User
from jinja2 import StrictUndefined

import google.oauth2.id_token as g_id_token
import google.auth.transport.requests as g_requests

import json
import os
import requests
import crud 

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY'] 

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an error.
app.jinja_env.undefined = StrictUndefined

NEWS_API_KEY = os.environ['NEWS_API_KEY']
ALL_COUNTRIES_LIST = crud.all_countries_list
ALL_COUNTRIES_DICT = crud.all_countries_dict
NEWS_LANGUAGES = crud.NEWS_LANGUAGES
WORLD_CURRENCIES = crud.world_currencies



@app.route("/")
def homepage():
    """App landing page and establish session details"""

    # Establish session details

    # TEST for session info
    session_test = session.get("current_user_email", None)
    # If a user is logged in, establish session deets from DB
    if session_test != None:
        user = crud.get_user_email(session["current_user_email"])

        # If there is a user, establish session details from db
        session["current_user_email"] = user.email
        session["current_user_name"] = user.username
        session["current_user_lang"] = user.preferred_lang
        session["current_user_currency"] = user.preferred_currency
    else:
        # Else, establish empty session
        session["current_user_email"] = None
        session["current_user_lang"] = None
        session["current_user_name"] = None
        session["current_user_currency"] = "USD"

    return render_template("homepage.html", 
    ALL_COUNTRIES_LIST=ALL_COUNTRIES_LIST)


#################### LOGGIN IN AND OUT #####################
@app.route("/logout")
def logout():

    session["current_user_email"] = None
    session["current_user_name"] = None
    session["current_user_lang"] = None
    session["current_user_currency"] = "USD"
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

@app.route("/login-page/google-oauth", methods=["POST"])
def google_OAuth():

    CLIENT_ID = "152475116532-5c55rrlp6uds24c9lhkn8d3g70o8vu8r.apps.googleusercontent.com"
    # Recieve the credential: Encrypted JWT
    ID_TOKEN = request.form["credential"]

    # Verify that token comes in cookie and body, and they are the same
    csrf_token_cookie = request.cookies.get('g_csrf_token')
    if not csrf_token_cookie:
        print("***ERROR: No CSRF token in Cookie***")
    csrf_token_body = request.form.get('g_csrf_token')
    if not csrf_token_body:
        print("***ERROR: No CSRF token in post body***")
    if csrf_token_cookie != csrf_token_body:
        print("***ERROR: Failed to verify double submit cookie.")

    # The verify_oauth2_token function verifies the JWT signature, the aud claim, and the exp claim. 
    try:
        # Gets the decoded JWT using Google API client lib
        g_idinfo = g_id_token.verify_oauth2_token(ID_TOKEN, g_requests.Request(), CLIENT_ID)

        # ----- INTERNAL OPERATIONS ---
        # ID token is valid. Get the user's Google Account ID from the decoded token.
        g_userid = g_idinfo['sub'] # Will operate as password
        g_email = g_idinfo['email'] # User email
        g_nickname = g_idinfo['given_name'] # User name

        # Check if email already exists in DB
        user = crud.get_user_email(g_email) 
        # If not in DB
        if user == None:
            # Add to DB
            new_user = User(username=g_nickname, email=g_email, password=g_userid)
            db.session.add(new_user)
            db.session.commit()

            # Add to session
            session["current_user_email"] = g_email
            session["current_user_name"] = g_nickname
            # Flash: Welcome, logged in
            flash(f"Welcome to the World Report, {g_nickname}! You've been logged in.")

        # If exists, just add to session
        else:
            session["current_user_email"] = g_email
            session["current_user_name"] = g_nickname
            # Flash: Logged In
            flash("You are logged in!")


    except ValueError:
        # Invalid token
        print("****ERROR: Invalid Token*****")
        # pass

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
    NEWS_LANGUAGES=NEWS_LANGUAGES, WORLD_CURRENCIES=WORLD_CURRENCIES)

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

@app.route("/user-profile/currency-preference", methods=["POST"])
def choose_currency():
    """User can choose the preferred default exchange rate currency
    Sets this preference in the DB and the session"""

    language_preference = request.form.get("currency-dropdown")
    # Add to session
    session["current_user_currency"] = language_preference
    # Add to DB
    user = crud.get_user_email(session["current_user_email"])
    user.preferred_currency = language_preference
    db.session.add(user)
    db.session.commit()


    return redirect("/user-profile")

@app.route("/user-profile/reset-preferences")
def reset_preferences():
    """Resets the users preferences in the database and session"""

    user = crud.get_user_email(session["current_user_email"])
    user.preferred_lang = None
    user.preferred_currency = "USD"
    db.session.add(user)
    db.session.commit()

    session["current_user_lang"] = None
    session["current_user_currency"] = "USD"

    return redirect("/user-profile")


###################### CALLING APIs #############################
def new_api_call(country_param, lang=None):
    news_url = "https://newsapi.org/v2/everything"

    payload = {
        "apikey": NEWS_API_KEY, 
        "q": country_param,
        "sortBy": "relevancy",
        "pageSize": "5",
    }

    if lang:
        payload["language"] = lang

    news_res = requests.get(news_url, params=payload)
    news_data = news_res.json()
    articles = news_data["articles"]

    return jsonify(articles)

@app.route("/api/news-by-country-name")
def news_by_country_name():
    """Call the News API with the NAME"""

    country_name = request.args.get("countryName")
    lang = session.get("current_user_lang", None)
    
    return new_api_call(country_name, keyword, lang)

@app.route("/api/exchange-rate")
def exchange_rate_API():

    currency_code = request.args.get("currencyCode")
    currency_preference = session["current_user_currency"]
    exchange_rate_url = f'https://api.exchangerate.host/convert?from={currency_preference}&to={currency_code}&places=2'
    response = requests.get(exchange_rate_url)
    data = response.json()

    return jsonify(data)

@app.route("/api/v1/ISO-dashboard/<params>")
def api_results(params=None):

    if not params:
        params = "United States of America"
    
    # take in ALPHA code, 
    # use code to call REST countries, store only some info
        # use the currency code to call exchange rate

    # EXAMPLE POSSIBILITY to make requests and wait w/out error
    # result = None
    # while result is None:
    #     try:
    #         # connect
    #         result = get_data(...)
    #     except:
    #         pass
    
    return new_api_call(params)

@app.route("/api/param-test/<param>")
def test_api_query(param):
    print(param)

    return jsonify(param)



###########################################################
if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
    # In debug mode, page will be updated when code is changed, change to debug=True/False