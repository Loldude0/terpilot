from flask import Flask, redirect
from flask import request
from flask import jsonify
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from datetime import datetime

import os
from dotenv import load_dotenv
load_dotenv()
connection_string = os.getenv("CONNECTION_STRING")

from upload_pipeline import upload_pipeline

from parse_query import parse_query
from predict_disease import predict_disease
from summary import summarize

from flask import current_app, g

from flask_cors import CORS

from sqlalchemy import text

app = Flask(__name__)

@app.route("/gettest", methods=["POST"])
def get_probable():
    data = request.json.get("data")
    data_string = str(data)
    print(data_string)