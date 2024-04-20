from flask import Flask, redirect
from flask import request
from flask import jsonify
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv
import json

from function_caller import FunctionCaller

from function_caller import *

load_dotenv()
connection_string = os.getenv("CONNECTION_STRING")

fc = FunctionCaller()

from flask import current_app, g

from flask_cors import CORS

from sqlalchemy import text

from function_caller import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

@app.route("/getresponse", methods=["POST"])
def get_response():
    data = request.json.get("message")
    response = fc.parse_query(data)
    print(response)     
    return jsonify({"message": response})

app.run(debug=True)