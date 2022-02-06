from flask import Flask, url_for, redirect, request, render_template, session, jsonify
import db
from db import *
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "root"
app.permanent_session_lifetime = timedelta(minutes=60)


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
    if "admin" in session:
        root = session["admin"]
        return render_template("account.jinja2", user=root)
    elif "normal" in session:
        user = session["normal"]
        return render_template("account.jinja2", user=user)
    return render_template("account.jinja2")


@app.route("/account-login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True
        user = request.form["name"]
        password = request.form["pass"]
        sqlq = "SELECT COUNT(1) FROM users_db WHERE username = %s AND password = %s"
        check_root = "SELECT account FROM users_db WHERE username = %s AND password = %s"
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
            else:
                session["normal"] = user
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
        sqlq = "SELECT COUNT(1) FROM users_db WHERE username = %s"
        val = (user_reg,)
        cursor.execute(sqlq, val)
        if cursor.fetchone()[0]:
            return render_template('register.jinja2')
        else:
            execute = "INSERT INTO users_db (username, password, email, account) VALUES(%s, %s, %s, %s)"
            value = (user_reg, password_reg, email, "normal")
            cursor.execute(execute, value)
            db.commit()
            return redirect(url_for('login'))
    return render_template('register.jinja2')


@app.route('/Logout')
def logout():
    session.pop("normal", None)
    session.pop("admin", None)
    return render_template('account.jinja2')


@app.route('/Databases', methods=['POST', 'GET'])
def databases():
    if "admin" in session:
        user = session["admin"]
        select_all_connects = "SELECT database_name FROM connects_db WHERE user_name_table = %s"
        value_select = (user,)
        cursor.execute(select_all_connects, value_select)
        get_db = cursor.fetchall()
        return render_template('database_home.jinja2', db=get_db)
    elif "normal" in session:
        user = session["normal"]
        select_all_connects = "SELECT database_name FROM connects_db WHERE user_name_table = %s"
        value_select = (user,)
        cursor.execute(select_all_connects, value_select)
        get_db = cursor.fetchall()
        return render_template('database_home.jinja2', db=get_db)
    else:
        return redirect(url_for('login'))


@app.route('/Connect', methods=['POST', 'GET'])
def connect():
    if request.method == 'POST':
        host_connect = request.form['host_connect']
        user_connect = request.form['name_connect']
        pass_connect = request.form['pass_connect']
        data_connect = request.form['data_connect']
        query_connect = "INSERT INTO connects_db(host, username, password, database_name, user_name_table) \
    select * from( Select %s, %s, %s, %s, %s) as temp \
    where not exists \
    (Select user_name_table from connects_db where user_name_table) LIMIT 1"
        if "admin" in session:
            user_name_admin = session["admin"]
            value_connect = (host_connect, user_connect, pass_connect, data_connect, user_name_admin)
            cursor.execute(query_connect, value_connect)
            db.commit()
        elif "normal" in session:
            user_name = session["normal"]
            value_connect = (host_connect, user_connect, pass_connect, data_connect, user_name)
            cursor.execute(query_connect, value_connect)
            db.commit()
        else:
            print("test")
    return render_template('connect_db.jinja2')


@app.route('/Connect-Page')
def connect_page():
    if "admin" in session:
        user_name = session["admin"]
        render_template('db_page.jinja2', name=user_name)
    elif "normal" in session:
        user_name_normal = session["normal"]
    return render_template('db_page.jinja2', name=user_name)


if __name__ == '__main__':
    app.run(debug=True)
