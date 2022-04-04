from flask import Flask, redirect, request, render_template
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


@app.route("/news-country", methods=['POST'])
def get_news_by_country():

    two_dig_country_code = request.form.get("country-code-select")

    url = "https://newsapi.org/v2/top-headlines"
    payload = {
        "apikey": NEWS_API_KEY, 
        "country": two_dig_country_code,
        "pageSize": "5",
    }

    url = "https://newsapi.org/v2/top-headlines"
    payload = {
        "apikey": NEWS_API_KEY, 
        "country": two_dig_country_code,
        "pageSize": "5",
    }

    res = requests.get(url, params=payload)
    data = res.json()
    articles = data["articles"]

    return render_template("/news-test-page.html", 
    articles=articles)


@app.route("/news-test-page")
def test_page():
    """Testing APIs"""

    url = "https://newsapi.org/v2/top-headlines"
    payload = {
        "apikey": NEWS_API_KEY, 
        "country": "us",
        "pageSize": "5",
    }

    res = requests.get(url, params=payload)
    data = res.json()
    articles = data["articles"]

    return render_template("news-test-page.html", 
    data=data, 
    articles=articles)





    
if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")