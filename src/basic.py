from flask import Blueprint, render_template, redirect, url_for, session, flash, request

from db import cursor, db

basic = Blueprint("basic", __name__, static_folder="static", template_folder="templates")


@basic.route('/')
@basic.route('/home')
def home():
    return render_template('index.jinja2')


@basic.route('/account-login', methods=['POST', 'GET'])
@basic.route('/login', methods=['POST', 'GET'])
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


@basic.route('/account-register', methods=['POST', 'GET'])
@basic.route('/register', methods=['POST', 'GET'])
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
