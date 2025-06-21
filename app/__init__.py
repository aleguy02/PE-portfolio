import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
url = os.getenv("URL")


@app.route('/')
def index():
    return render_template('index.html', title="Alejandro Villate", url=url)
