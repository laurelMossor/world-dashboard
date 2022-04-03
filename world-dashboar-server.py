from flask import Flask, request, render_template
import json
import os
import requests


app = Flask(__name__)

NEWS_API_KEY = os.environ['NEWS_API_KEY']