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
import json

from function_caller import FunctionCaller


load_dotenv()
connection_string = os.getenv("CONNECTION_STRING")

fc = FunctionCaller()

from flask import current_app, g

from flask_cors import CORS

from sqlalchemy import text

from function_caller import *

app = Flask(__name__)

CORS(app)

@app.route("/getresponse", methods=["POST"])
def get_probable():
    data = request.json.get("message")
    print(type(data))
    print(data)
    response = fc.parse_query(data)
    print(type(response))
    
    return jsonify({"response": response})

app.run(debug=True)