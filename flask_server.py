from flask import Flask, redirect
from flask import request
from flask import jsonify
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv
from flask_cors import CORS

#fuck cors we allow every single thing, EVERY SINGLE THING SO EVERYTHING WORKS



from function_caller import *

load_dotenv()
connection_string = os.getenv("CONNECTION_STRING")

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
app.config["SQLALCHEMY_ECHO"] = True
db = SQLAlchemy(app)
fc = FunctionCaller()

@app.route("/getresponse", methods=["POST"])
def get_response():
    print("got response")
    data = request.json.get("message")
    response, response_type = fc.parse_query(data)
    print(response)
    return jsonify({"type":response_type,"message": response})



app.run(debug=True)