import secrets
from flask import Flask, render_template, abort, request, session, flash, redirect

app = Flask(__name__)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():

    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if not username or not password1 or not password2:
        flash("VIRHE: kaikki kentät ovat pakollisia")
        return redirect("/register")

    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat")
        return redirect("/register")

    if len(password1) < 8 or len(password1) > 50:
        flash("VIRHE: salasanan tulee olla 8-50 merkkiä pitkä")
        return redirect("/register")

    if len(username) > 20:
        flash("VIRHE: käyttäjänimi on liian pitkä")
        return redirect("/register")

    if not username.isalnum():
        flash("VIRHE: käyttäjänimi saa sisältää vain kirjaimia ja numeroita")
        return redirect("/register")

    if not users.create_user(username, password1):
        flash("VIRHE: tunnus on jo varattu")
        return redirect("/register")

    flash("Tunnus luotu")
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("VIRHE: väärä tunnus tai salasana")
            return redirect("/login")
        
@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")