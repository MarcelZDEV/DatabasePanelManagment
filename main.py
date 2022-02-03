from flask import Flask, url_for, redirect, request, render_template, session
from db import *

app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template("index.jinja2")


@app.route("/account-chose")
def account():
    return render_template("account.jinja2")


@app.route("/account-login")
def login():
    return render_template('login.jinja2')


if __name__ == '__main__':
    app.run(debug=True)
