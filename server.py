from flask import Flask, redirect, request, render_template, jsonify
import json
import os
import requests


app = Flask(__name__)

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
    app.debug = True
    app.run(host="0.0.0.0")