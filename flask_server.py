from flask import Flask, redirect
from flask import request
from flask import jsonify
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

from function_caller import *

load_dotenv()
connection_string = os.getenv("CONNECTION_STRING")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)

@app.route("/getresponse", methods=["POST"])
def get_probable():
    data = request.json.get("message")
    print(type(data))
    print(data)
    response = parse_query(data)
    print(type(response))
    
    return jsonify({"response": response})

app.run(debug=True)