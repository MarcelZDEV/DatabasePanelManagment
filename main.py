from flask import Flask, url_for, redirect, render_template, session, flash, request
from db import *
from datetime import timedelta
from src.basic import basic

app = Flask(__name__)
app.secret_key = "root"
app.permanent_session_lifetime = timedelta(minutes=60)
app.register_blueprint(basic, url_prefix="")


@app.route('/')
def home_page():
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


@app.route("/account-login")
def login():
    return render_template('login.jinja2')


@app.route('/account-register', methods=['POST', 'GET'])
def register():
    return render_template('register.jinja2')


@app.route('/logout')
def logout():
    session.pop("normal", None)
    session.pop("admin", None)
    return render_template('account.jinja2')


@app.route('/database')
def database():
    if "admin" in session:
        user = session["admin"]
        select_all_connects = "SELECT database_name FROM dbpm.db_connects WHERE user_name_table = %s"
        value_select = (user,)
        cursor.execute(select_all_connects, value_select)
        get_db = cursor.fetchall()
        return render_template('database_home.jinja2', db=get_db)
    elif "normal" in session:
        user = session["normal"]
        select_all_connects = "SELECT database_name FROM dbpm.db_connects WHERE user_name_table = %s"
        value_select = (user,)
        cursor.execute(select_all_connects, value_select)
        get_db = cursor.fetchall()
        return render_template('database_home.jinja2', db=get_db)
    else:
        flash('You have to login on page to move on this side', 'info')
        return redirect(url_for('login'))


@app.route('/add-connect', methods=['POST', 'GET'])
def connect():
    return render_template('add_connect.jinja2')


@app.route('/connect-page/<name_id>', methods=['GET', 'POST'])
def connect_page(name_id):
    if "admin" in session:
        user_name = session["admin"]
        return render_template('db_page.jinja2', name_id=name_id, name=user_name)
    elif "normal" in session:
        user_name = session["normal"]
        return render_template('db_page.jinja2', name_id=name_id, name=user_name)
    else:
        return redirect(url_for('login'))


@app.route('/connect-page/mysql-statements/<name_id>', methods=["GET", 'POST'])
def statements(name_id):
    if "admin" in session:
        user_name = session["admin"]
        return render_template('MySQL_Statements.jinja2', name_id=name_id, name=user_name)
    elif "normal" in session:
        user_name = session["normal"]
        return render_template('MySQL_Statements.jinja2', name_id=name_id, name=user_name)
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
