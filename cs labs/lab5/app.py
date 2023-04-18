import requests
from flask import Flask, render_template, request, flash, redirect
import psycopg2

app = Flask(__name__)

app.secret_key = b''

conn = psycopg2.connect(database="",
                        user="",
                        password="",
                        host="",
                        port="")

cursor = conn.cursor()

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')   
            password = request.form.get('password')

            if username == '' or password == '':
                flash(u'Empty username or password', 'error')
                return render_template('login.html')

            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())

            if len(records) == 0:
                flash(u'!!!!!!!YOU ARE AN IMPOSTER!!!!!!!')
                return render_template('login.html')

            return render_template('account.html', full_name=records[0][1], username=username, password=password )
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')

        if password == '' or login == '' or name == '':
            flash(u'Fill in all fields please')
            return render_template('registration.html')

        cursor.execute("SELECT * FROM service.users WHERE login=%s", (str(login),))
        records = list(cursor.fetchall())
        if len(records) != 0:
            flash(u'Someone already has this username, please choose another one')
            return render_template('registration.html')

        cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                       (str(name), str(login), str(password)))
        conn.commit()

        cursor.execute("SELECT * FROM service.users WHERE login=%s", (str(login),))
        records = list(cursor.fetchall())

        if len(records) == 0:
            flash(u"Couldn't create account, please try again")
            return render_template('registration.html')

        return redirect('/login/')

    return render_template('registration.html')


