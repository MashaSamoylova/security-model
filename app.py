from flask import Flask, render_template, request, session
from flask_mysqldb import MySQL

import MySQLdb.cursors
import hashlib
import json

app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'mysql'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'shop'

mysql = MySQL(app)

ADMIN_ROLE = 'admin'
DELIVERY_BOY_ROLE = 'delivery_boy'
CLIENT_ROLE = 'client_role'

def hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/admins/', methods=['GET'])
def get_admins():
    if session.get('role', '0') == ADMIN_ROLE:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admins')
        return render_template('table.html', result=cursor.fetchall())
    else:
        return "FORBIDDEN!!"

@app.route('/clients/', methods=['GET'])
def get_clients():
    if session.get('role', '0') == ADMIN_ROLE:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM clients')
        return render_template('table.html', result=cursor.fetchall())
    else:
        return "FORBIDDEN!!"

@app.route('/orders/', methods=['GET'])
def get_orders():
    if session.get('role', '0') in [ADMIN_ROLE, DELIVERY_BOY_ROLE]:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM orders')
        return render_template('table.html', result=cursor.fetchall())
    else:
        return "FORBIDDEN!!"

@app.route('/delivery_boys/', methods=['GET'])
def get_delivery_boys():
    if session.get('role', '0') in [ADMIN_ROLE]:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM delivery_boys')
        return render_template('table.html', result=cursor.fetchall())
    else:
        return "FORBIDDEN!!"


@app.route('/products/', methods=['GET'])
def get_products():
    if session.get('role', '0') in [ADMIN_ROLE, CLIENT_ROLE, DELIVERY_BOY_ROLE]:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM products')
        return render_template('table.html', result=cursor.fetchall())
    else:
        return "FORBIDDEN!!"

@app.route('/rewiews/', methods=['GET'])
def get_rewiews():
    if session.get('role', '0') in [ADMIN_ROLE, DELIVERY_BOY_ROLE, CLIENT_ROLE]:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM rewiews')
        return render_template('table.html', result=cursor.fetchall())
    else:
        return "FORBIDDEN!!"

@app.route('/contain/', methods=['GET'])
def get_contain():
    if session.get('role', '0') in [ADMIN_ROLE, DELIVERY_BOY_ROLE]:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM contain')
        return render_template('table.html', result=cursor.fetchall())
    else:
        return "FORBIDDEN!!"

@app.route('/browse/', methods=['GET'])
def get_browse():
    if session.get('role', '0') in [ADMIN_ROLE, DELIVERY_BOY_ROLE]:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM browse')
        return render_template('table.html', result=cursor.fetchall())
    else:
        return "FORBIDDEN!!"

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('index.html', msg='')

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = hash(request.form['password'])

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admins WHERE login = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['login']
            session['role'] = ADMIN_ROLE
            return f'Hello, {account["login"]}! You are admin!'

        cursor.execute('SELECT * FROM clients WHERE login = %s AND password = %s', (username, password))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['login']
            session['role'] = CLIENT_ROLE
            return f'Hello, {account["login"]}! You are client!'

        cursor.execute('SELECT * FROM delivery_boys WHERE login = %s AND password = %s', (username, password))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['username'] = account['login']
            session['role'] = DELIVERY_BOY_ROLE
            return f'Hello, {account["login"]}! You are delivery boy!'
        
        return "blya"



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')