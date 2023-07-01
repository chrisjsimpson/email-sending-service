from flask import render_template, jsonify
from apiflask import APIFlask, Schema, HTTPTokenAuth
from apiflask.fields import String, List, Email
from db import get_db, close_db
import sqlalchemy
from logger import log
from email.message import EmailMessage
from dotenv import load_dotenv
import os
from time import time

load_dotenv(verbose=True)

EMAIL_FOLDER = os.getenv("EMAIL_FOLDER", None)


app = APIFlask(__name__, docs_ui="elements")
auth = HTTPTokenAuth()
app.teardown_appcontext(close_db)


class Email(Schema):
    SUBJECT = String(required=False)
    FROM = Email(required=True)
    TO = List(Email, required=False)  # Either TO or BCC is required
    BODY = String(required=False)
    CC = List(Email, required=False)
    BCC = List(Email, required=False)


class User():
    def get_roles(self):
        return ["api_user"]

@auth.verify_token
def verify_token(token):
    return User()



@auth.get_user_roles
def get_user_roles(user):
    return user.get_roles()

@app.route("/")
def index():
    return render_template("index.html")


@app.post("/send-email")
@app.input(Email, location="json")
@app.auth_required(auth, roles="api_user")
def send_email(email):
    msg = EmailMessage()
    msg.set_content(email["BODY"])

    msg["Subject"] = email["SUBJECT"]
    msg["From"] = email["FROM"]
    msg["To"] = email["TO"]
    with open(f"{EMAIL_FOLDER}{time()}", "w") as fp:
        fp.write(msg.as_string())
    return {"response": "OK. Email submitted"}


@app.route("/health")
@app.auth_required(auth)
def health():
    log.info("Checking /health")
    error = False
    msg = "OK"
    try:
        db = get_db()
    except ValueError as e:
        error = True
        msg = f"Database likely invalid config {e}"
        return return_error(msg)

    try:
        result = db.execute("SELECT NOW()")
        result = result.one()
        log.info(
            f"/health reported OK including database connection: {result}"
        )  # noqa: E501
    except sqlalchemy.exc.OperationalError as e:
        error = True
        msg = f"sqlalchemy.exc.OperationalError: {e}"
        log.error(msg)
        return_error(msg)
    except Exception as e:
        error = True
        msg = f"Error performing healthcheck: {e}"
        log.error(msg)
        return_error(msg)

    if error:
        return return_error(msg)

    return jsonify(health)


def return_error(msg, error_code=500):
    return jsonify(msg), error_code