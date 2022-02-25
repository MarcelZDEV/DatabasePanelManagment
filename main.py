from flask import Flask, url_for, redirect, render_template, session, flash, request
from db import *
from datetime import timedelta
import mysql.connector

app = Flask(__name__, template_folder='templates')
app.secret_key = "root"
app.permanent_session_lifetime = timedelta(minutes=60)
global db_user_connect


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.jinja2')


@app.route("/account-chose")
def account():
    if "admin" in session:
        root = session["admin"]
        return render_template("account.jinja2", user=root)
    elif "normal" in session:
        user = session["normal"]
        return render_template("account.jinja2", user=user)
    return render_template("account.jinja2")


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
        host_user_user = user_name
        print(host_user_user)
        return render_template('MySQL_Statements.jinja2', name_id=name_id, name=user_name)
    elif "normal" in session:
        user_name = session["normal"]
        if request.method == 'POST':
            get_execute = request.form['mysql']
            user_name = user_name
            database_name = name_id
            query = (user_name, database_name)
            host_connect = 'SELECT host FROM dbpm.db_connects WHERE user_name_table = %s AND database_name = %s'
            username_connect = 'SELECT username FROM dbpm.db_connects WHERE user_name_table = %s AND database_name = %s'
            database_name_connect = 'SELECT database_name FROM dbpm.db_connects WHERE user_name_table = %s AND database_name = %s'
            password_connect = 'SELECT password FROM dbpm.db_connects WHERE user_name_table = %s AND database_name = %s'

            cursor.execute(host_connect, query)
            cursor.execute(username_connect, query)
            cursor.execute(database_name_connect, query)
            cursor.execute(password_connect, query)

            global db_user_connect
            db_user_connect = mysql.connector.connect(
                host=f"{host_connect}",
                user=f"{username_connect}",
                password=f"{password_connect}",
                database=f"{database_name_connect}",
                port="3306"
            )

        return render_template('MySQL_Statements.jinja2', name_id=name_id, name=user_name)
    else:
        return redirect(url_for('login'))


@app.route('/add-connect', methods=['POST', 'GET'])
def add_connect():
    if request.method == 'POST':
        host_connect = request.form['host_connect']
        user_connect = request.form['name_connect']
        pass_connect = request.form['pass_connect']
        data_connect = request.form['data_connect']
        insert_connect = "INSERT INTO dbpm.db_connects(host, username, password, database_name, user_name_table) VALUES (%s, %s, %s, %s, %s)"
        check_db = "SELECT COUNT(1) FROM dbpm.db_connects WHERE database_name = %s"
        value = (data_connect,)
        cursor.execute(check_db, value)
        if cursor.fetchone()[0]:
            flash('You already have db with this name', 'info')
            return render_template('add_connect.jinja2')
        else:
            if "admin" in session:
                user_name_admin = session["admin"]
                value_connect = (host_connect, user_connect, pass_connect, data_connect, user_name_admin)
                cursor.execute(insert_connect, value_connect)
                db.commit()
            elif "normal" in session:
                user_name = session["normal"]
                value_connect = (host_connect, user_connect, pass_connect, data_connect, user_name)
                cursor.execute(insert_connect, value_connect)
                db.commit()
            return redirect(url_for('database'))
    return render_template('add_connect.jinja2')


@app.route('/account-login', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True
        user = request.form["name"]
        password = request.form["pass"]
        check_user_exist = "SELECT COUNT(1) FROM dbpm.user WHERE username = %s AND password = %s"
        check_root = "SELECT account FROM dbpm.user WHERE username = %s AND password = %s"
        val = (user, password)
        cursor.execute(check_user_exist, val)
        if cursor.fetchone():
            session["normal"] = user
            val_root = (user, password)
            cursor.execute(check_root, val_root)
            results = cursor.fetchone()
            if results is not None:
                if 'root' in results:
                    session["admin"] = user
                    return redirect(url_for('database'))
                elif 'normal' in results:
                    session["normal"] = user
                    return redirect(url_for('database'))
                else:
                    flash('Your login information are wrong', 'info')
            else:
                flash('Your login information are wrong', 'info')
        else:
            flash('Your login information are wrong', 'info')
            return render_template('login.jinja2')
    else:
        if "normal" in session or "admin" in session:
            return render_template("login.jinja2")
    return render_template('login.jinja2')


@app.route('/account-register', methods=['POST', 'GET'])
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user_reg = request.form["name_reg"]
        password_reg = request.form["pass_reg"]
        email_reg = request.form["email_reg"]
        sqlq = "SELECT COUNT(*) FROM dbpm.user WHERE username = %s"
        val = (user_reg,)
        cursor.execute(sqlq, val)
        if cursor.fetchone()[0]:
            flash('Username already exist. Try other name', 'info')
            return render_template('register.jinja2')
        else:
            execute = "INSERT INTO dbpm.user (username, password, email, account) VALUES(%s, %s, %s, %s)"
            value = (user_reg, password_reg, email_reg, "normal")
            cursor.execute(execute, value)
            db.commit()
            return redirect(url_for('login'))
    return render_template('register.jinja2')


if __name__ == '__main__':
    app.run(debug=True)
