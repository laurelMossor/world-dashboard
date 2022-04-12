from flask import Flask, redirect, request, render_template, jsonify
import json
import os
import requests


app = Flask(__name__)

NEWS_API_KEY = os.environ['NEWS_API_KEY']

COUNTRY_CODES = ['ae', 'ar', 'at', 'au', 'be', 'bg', 
'br', 'ca', 'ch', 'cn', 'co', 'cu', 'cz', 'de', 
'eg', 'fr', 'gb', 'gr', 'hk', 'hu', 'id', 'ie', 
'il', 'in', 'it', 'jp', 'kr', 'lt', 'lv', 'ma', 
'mx', 'my', 'ng', 'nl', 'no', 'nz', 'ph', 'pl', 
'pt', 'ro', 'rs', 'ru', 'sa', 'se', 'sg', 'si', 
'sk', 'th', 'tr', 'tw', 'ua', 'us', 've', 'za']


@app.route("/")
def homepage():
    """App landing page"""

    return render_template("homepage.html",
    country_codes=COUNTRY_CODES)


@app.route("/news-country")
def test_react():
    """Copying the lecture and example materials"""

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