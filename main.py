from flask import Flask, url_for, redirect, request, render_template, session
from db import *

app = Flask(__name__)


@app.route('/')
def home_page():
    return render_template("index.jinja2")


@app.route("/account-chose")
def account():
    return render_template("account.jinja2")


@app.route("/account-login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form["name"]
        password = request.form["pass"]
        print(user, password)
    return render_template('login.jinja2')


@app.route('/account-register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user_reg = request.form["name_reg"]
        password_reg = request.form["pass_reg"]
        email = request.form["email_reg"]
        sqlq = "SELECT COUNT(1) FROM users WHERE username = %s"
        val = (user_reg, )
        cursor.execute(sqlq, val)
        if cursor.fetchone()[0]:
            return render_template('login.jinja2')
        else:
            execute = "INSERT INTO users (username, password, email, account) VALUES(%s, %s, %s, %s)"
            value = (user_reg, password_reg, email, "normal")
            cursor.execute(execute, value)
            db.commit()
    return render_template('register.jinja2')


if __name__ == '__main__':
    app.run(debug=True)
