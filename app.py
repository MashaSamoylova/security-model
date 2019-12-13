from flask import Flask, render_template, request, session
from flask_mysqldb import MySQL

from MySQLdb.cursors import DictCursor as mysql_dict_cursor
from hashlib import sha256


app = Flask(__name__)

app.secret_key = "Kubr+phiCrudr@q=@6H#"

app.config["MYSQL_HOST"] = "mysql"
app.config["MYSQL_PORT"] = 3306
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "shop"

mysql = MySQL(app)


class AppDefaultRoles:
    ADMIN_ROLE = "admin"
    DELIVERY_BOY_ROLE = "delivery_boy"
    CLIENT_ROLE = "client_role"


class AppDefaultBinding:
    HOST = "0.0.0.0"
    PORT = 5000


class AppDefaultKeywords:
    FORBIDDEN_WARN = "FORBIDDEN!!"
    WRONG_USER_PASS_WARN = "Sorry, your password or username is incorrect."


def hash_str(password: str) -> str:
    return sha256(password.encode()).hexdigest()


@app.route("/admins/", methods=["GET"])
def get_admins() -> str or any:
    if session.get("role", "0") != AppDefaultRoles.ADMIN_ROLE:
        return render_template("error.html", msg=AppDefaultKeywords.FORBIDDEN_WARN)
    cursor = mysql.connection.cursor(mysql_dict_cursor)
    cursor.execute("SELECT * FROM admins")
    return render_template("admins.html", result=cursor.fetchall())


@app.route("/clients/", methods=["GET"])
def get_clients() -> str or any:
    if session.get("role", "0") != AppDefaultRoles.ADMIN_ROLE:
        return render_template("error.html", msg=AppDefaultKeywords.FORBIDDEN_WARN)
    cursor = mysql.connection.cursor(mysql_dict_cursor)
    cursor.execute("SELECT * FROM clients")
    return render_template("clients.html", result=cursor.fetchall())


@app.route("/orders/", methods=["GET"])
def get_orders() -> str or any:
    if session.get("role", "0") not in [
        AppDefaultRoles.ADMIN_ROLE,
        AppDefaultRoles.DELIVERY_BOY_ROLE,
    ]:
        return render_template("error.html", msg=AppDefaultKeywords.FORBIDDEN_WARN)
    cursor = mysql.connection.cursor(mysql_dict_cursor)
    cursor.execute("SELECT * FROM orders")
    return render_template("orders.html", result=cursor.fetchall())


@app.route("/delivery_boys/", methods=["GET"])
def get_delivery_boys() -> str or any:
    if session.get("role", "0") not in [AppDefaultRoles.ADMIN_ROLE]:
        return render_template("error.html", msg=AppDefaultKeywords.FORBIDDEN_WARN)
    cursor = mysql.connection.cursor(mysql_dict_cursor)
    cursor.execute("SELECT * FROM delivery_boys")
    return render_template("delivery_boys.html", result=cursor.fetchall())


@app.route("/products/", methods=["GET"])
def get_products() -> str or any:
    if session.get("role", "0") not in [
        AppDefaultRoles.ADMIN_ROLE,
        AppDefaultRoles.CLIENT_ROLE,
        AppDefaultRoles.DELIVERY_BOY_ROLE,
    ]:
        return render_template("error.html", msg=AppDefaultKeywords.FORBIDDEN_WARN)
    cursor = mysql.connection.cursor(mysql_dict_cursor)
    cursor.execute("SELECT * FROM products")
    return render_template("products.html", result=cursor.fetchall())


@app.route("/reviews/", methods=["GET"])
def get_reviews() -> str or any:
    if session.get("role", "0") not in [
        AppDefaultRoles.ADMIN_ROLE,
        AppDefaultRoles.DELIVERY_BOY_ROLE,
        AppDefaultRoles.CLIENT_ROLE,
    ]:
        return render_template("error.html", msg=AppDefaultKeywords.FORBIDDEN_WARN)
    cursor = mysql.connection.cursor(mysql_dict_cursor)
    cursor.execute("SELECT * FROM rewiews")
    return render_template("reviews.html", result=cursor.fetchall())


@app.route("/contain/", methods=["GET"])
def get_contain() -> str or any:
    if session.get("role", "0") not in [
        AppDefaultRoles.ADMIN_ROLE,
        AppDefaultRoles.DELIVERY_BOY_ROLE,
    ]:
        return render_template("error.html", msg=AppDefaultKeywords.FORBIDDEN_WARN)
    cursor = mysql.connection.cursor(mysql_dict_cursor)
    cursor.execute("SELECT * FROM contain")
    return render_template("contain.html", result=cursor.fetchall())


@app.route("/browse/", methods=["GET"])
def get_browse() -> str or any:
    if session.get("role", "0") not in [
        AppDefaultRoles.ADMIN_ROLE,
        AppDefaultRoles.DELIVERY_BOY_ROLE,
    ]:
        return render_template("error.html", msg=AppDefaultKeywords.FORBIDDEN_WARN)
    cursor = mysql.connection.cursor(mysql_dict_cursor)
    cursor.execute("SELECT * FROM browse")
    return render_template("browse.html", result=cursor.fetchall())


@app.route("/login/", methods=["GET", "POST"])
def login() -> str or any:
    if request.method == "GET":
        return render_template("index.html", msg="")

    if (
        request.method == "POST"
        and request.form.get("username")
        and request.form.get("password")
    ):
        username = request.form["username"]
        password = hash_str(request.form["password"])

        cursor = mysql.connection.cursor(mysql_dict_cursor)
        cursor.execute(
            "SELECT * FROM admins WHERE login = %s AND password = %s",
            (username, password),
        )
        account = cursor.fetchone()
        if account:
            session["loggedin"] = True
            session["username"] = account["login"]
            session["role"] = AppDefaultRoles.ADMIN_ROLE
            return render_template("error.html", msg=f'Hello, {account["login"]}! You are admin!')

        cursor.execute(
            "SELECT * FROM clients WHERE login = %s AND password = %s",
            (username, password),
        )
        account = cursor.fetchone()
        if account:
            session["loggedin"] = True
            session["username"] = account["login"]
            session["role"] = AppDefaultRoles.CLIENT_ROLE
            return render_template("error.html", msg=f'Hello, {account["login"]}! You are client!')

        cursor.execute(
            "SELECT * FROM delivery_boys WHERE login = %s AND password = %s",
            (username, password),
        )
        account = cursor.fetchone()

        if account:
            session["loggedin"] = True
            session["username"] = account["login"]
            return render_template("error.html", msg=f'Hello, {account["login"]}! You are delivery boy!')

        return render_template("error.html", msg=AppDefaultKeywords.WRONG_USER_PASS_WARN)


if __name__ == "__main__":
    app.run(debug=True, host=AppDefaultBinding.HOST, port=AppDefaultBinding.PORT)
