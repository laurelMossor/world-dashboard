from flask import (Flask, redirect, request, 
            render_template, jsonify, flash, session)
from model import connect_to_db, db, User
import json
import os
import requests
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

NEWS_API_KEY = os.environ['NEWS_API_KEY']


@app.route("/")
def homepage():
    """App landing page"""

    return render_template("homepage.html")


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