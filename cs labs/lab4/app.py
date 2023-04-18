import requests
from flask import Flask, render_template, request, flash
import psycopg2

app = Flask(__name__)

app.secret_key = b''

conn = psycopg2.connect(database="",
                        user="",
                        password="",
                        host="",
                        port="")

cursor = conn.cursor()

@app.route('/login/', methods=['POST'])
def login():
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
    return render_template('account.html', full_name=records[0][1], username=username, password=password)


@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')
