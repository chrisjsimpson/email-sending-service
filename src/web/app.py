from flask import render_template
from apiflask import APIFlask, Schema
from apiflask.fields import String
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
app.teardown_appcontext(close_db)


class Email(Schema):
    SUBJECT = String(required=True)
    FROM = String(required=True)
    TO = String(required=True)
    BODY = String(required=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/send-email")
@app.input(Email)
def queue_email(email):
    msg = EmailMessage()
    msg.set_content(email["BODY"])

    msg["Subject"] = email["SUBJECT"]
    msg["From"] = email["FROM"]
    msg["To"] = email["TO"]
    with open(f"{EMAIL_FOLDER}{time()}", "w") as fp:
        fp.write(msg.as_string())
    return "OK"


@app.route("/health")
def health():
    log.info("Checking /health")
    db = get_db()
    health = "BAD"
    try:
        result = db.execute("SELECT NOW()")
        result = result.one()
        health = "OK"
        log.info(
            f"/health reported OK including database connection: {result}"
        )  # noqa: E501
    except sqlalchemy.exc.OperationalError as e:
        msg = f"sqlalchemy.exc.OperationalError: {e}"
        log.error(msg)
    except Exception as e:
        msg = f"Error performing healthcheck: {e}"
        log.error(msg)

    return health
