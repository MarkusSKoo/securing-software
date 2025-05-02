import secrets
from flask import Flask, render_template, abort, request, session, flash, redirect
import users
import config
import comments

app = Flask(__name__)
app.secret_key = config.secret_key

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.route("/")
def index():
    comments_list = comments.get_comments()
    return render_template("index.html", comments=comments_list)


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():

    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if not username or not password1 or not password2:
        flash("ERROR: fill all fields")
        return redirect("/register")

    if password1 != password2:
        flash("ERROR: passwords do not match")
        return redirect("/register")

    if len(password1) < 8 or len(password1) > 50:
        flash("ERROR: password must beb 8-50 charachters")
        return redirect("/register")

    if not users.create_user(username, password1):
        flash("ERROR: username not available")
        return redirect("/register")

    flash("Registration succesful")
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
            flash("ERROR: wrong username or password")
            return redirect("/login")
        
@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")

@app.route("/new_comment")
def new_comment():
    if "user_id" not in session:
        flash("ERROR: log in first")
        return redirect("/login")
    return render_template("new_comment.html")


@app.route("/create_comment", methods=["POST"])
def create_comment():
#    check_csrf()
    if "user_id" not in session:
        abort(403)

    comment = request.form["comment"]

    if not comment:
        flash("ERROR: comment can not be empty")
        return redirect("/new_comment")

    comments.create_comment(session["user_id"], comment)
    flash("Comment created")
    return redirect("/")