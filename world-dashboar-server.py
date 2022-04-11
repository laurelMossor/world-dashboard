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

@app.route("/test-home")
def test_home():

    return render_template("test-home.html", 
    country_codes=COUNTRY_CODES, 
    NEWS_API_KEY=NEWS_API_KEY)

@app.route("/news-country-test")
def test_react():
    """Copying the lecture and example materials"""

    # 2-digit country code from form
    two_dig_country_code = request.args.get("twoDigCountryCode")
    print("******************")
    print(two_dig_country_code)
    print("******************")

    # News API information gathering
    news_url = "https://newsapi.org/v2/top-headlines"
    news_payload = {
        "apikey": NEWS_API_KEY, 
        "country": two_dig_country_code,
        "pageSize": "5",
    }
    news_res = requests.get(news_url, params=news_payload)
    print("******************")
    print(news_res.url)
    print("******************")
    news_data = news_res.json()
    # articles = news_data["articles"]

    # return jasonify(articles)
    return jsonify(news_data)



@app.route("/news-country", methods=['POST'])
def get_news_by_country():
    """Processes the form from homepage.html and grabs News
    OLD PAGE"""
    
    # 2-digit country code from form
    two_dig_country_code = request.form.get("country-code-select")

    # News API information gathering
    news_url = "https://newsapi.org/v2/top-headlines"
    news_payload = {
        "apikey": NEWS_API_KEY, 
        "country": two_dig_country_code,
        "pageSize": "5",
    }
    news_res = requests.get(news_url, params=news_payload)
    print("******************")
    print(news_res.url)
    print("******************")

    news_data = news_res.json()
    articles = news_data["articles"]

    return render_template("/dashboard.html", 
    articles=articles)



@app.route("/dashboard")
def test_page():
    """Testing APIs
    Shows US top headlines"""

    url = "https://newsapi.org/v2/top-headlines"
    payload = {
        "apikey": NEWS_API_KEY, 
        "country": "us",
        "pageSize": "5",
    }

    res = requests.get(url, params=payload)
    data = res.json()
    articles = data["articles"]

    return render_template("dashboard.html", 
    articles=articles)





    
if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0")