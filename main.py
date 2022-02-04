from flask import Flask, url_for, redirect, request, render_template, session
from db import *
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "root"
app.permanent_session_lifetime = timedelta(minutes=10)


@app.route('/')
def home_page():
    if "admin" in session:
        root = session["admin"]
        return render_template("admin_home.jinja2", user=root)
    elif "normal" in session:
        user = session["normal"]
        return render_template("index.jinja2", user=user)
    return render_template("index.jinja2")


@app.route("/account-chose")
def account():
    return render_template("account.jinja2")


@app.route("/account-login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True
        user = request.form["name"]
        password = request.form["pass"]
        sqlq = "SELECT COUNT(1) FROM users WHERE username = %s AND password = %s"
        check_root = "SELECT account FROM users WHERE username = %s AND password = %s"
        val = (user, password)
        cursor.execute(sqlq, val)
        if cursor.fetchone():
            print("Yes you are exist")
            session["normal"] = user
            val_root = (user, password)
            cursor.execute(check_root, val_root)
            results = cursor.fetchone()
            if 'root' in results:
                session["admin"] = user
                print("admin")
            return redirect(url_for('home_page'))
        else:
            return render_template('login.jinja2')
    else:
        if "normal" in session or "admin" in session:
            return render_template("login.jinja2")
    return render_template('login.jinja2')


@app.route('/account-register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user_reg = request.form["name_reg"]
        password_reg = request.form["pass_reg"]
        email = request.form["email_reg"]
        sqlq = "SELECT COUNT(1) FROM users WHERE username = %s"
        val = (user_reg,)
        cursor.execute(sqlq, val)
        if cursor.fetchone()[0]:
            return render_template('login.jinja2')
        else:
            execute = "INSERT INTO users (username, password, email, account) VALUES(%s, %s, %s, %s)"
            value = (user_reg, password_reg, email, "normal")
            cursor.execute(execute, value)
            db.commit()
    return render_template('register.jinja2')


@app.route('/Logout')
def logout():
    session.pop("normal", None)
    session.pop("admin", None)
    return render_template('account.jinja2')


if __name__ == '__main__':
    app.run(debug=True)
