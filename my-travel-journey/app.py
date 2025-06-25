import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask import jsonify

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///travel.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """ Show index page"""
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            flash("please type username", "error")
            return redirect("/")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("please type password", "error")
            return redirect("/")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            flash("invalid username and/or password", "error")
            return redirect("/")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/home")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            flash("please type username", "error")
            return redirect("/")

        if not password:
            flash("please type password", "error")
            return redirect("/")

        if not confirmation:
            flash("please confirm password", "error")
            return redirect("/")

        if password != confirmation:
            flash("password does not match", "error")
            return redirect("/")

        hash = generate_password_hash(password)

        try:
            # INSERT INTO () VALUES ()
            new_user = db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except:
            flash("username exists already", "error")
            return redirect("/")

        session["user_id"] = new_user

        return redirect("/login")


@app.route("/home")
@login_required
def home():
    """Show home page"""
    user_id = session["user_id"]
    # Fetch user-specific data from the database, such as username, places, notes, etc.
    user_data = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    # Fetch places and notes associated with the user using JOIN
    user_places = db.execute("SELECT * FROM user_places WHERE user_id = ?", user_id)
    user_notes = db.execute("SELECT * FROM user_notes WHERE user_id = ?", user_id)
    return render_template("home.html", user_data=user_data, user_places=user_places, user_notes=user_notes)


@app.route("/add_places", methods=["GET", "POST"])
@login_required
def add_places():
    if request.method == "POST":
        # Get form data
        visit_status = request.form.get("visit_status")
        place_name = request.form.get("place_name")
        visit_date = request.form.get("visit_date")
        user_id = session["user_id"]

        # Insert data into the database
        db.execute("INSERT INTO user_places (user_id, place_name, date, status) VALUES (?, ?, ?, ?)",
                   user_id, place_name, visit_date, visit_status)

        flash("Place added successfully!", "success")
        return redirect("/home")
    else:
        return render_template("add_places.html")



@app.route("/my_places", methods=["GET", "POST"])
@login_required
def my_places():
    if request.method == "POST":
        # Get filter type from the form
        filter_type = request.json.get("filter_type")

        # Fetch user's places based on filter type
        user_id = session["user_id"]
        if filter_type == "all":
            places = db.execute("SELECT place_name, date FROM user_places WHERE user_id = ?", user_id)
        else:
            places = db.execute("SELECT place_name, date FROM user_places WHERE user_id = ? AND status = ?", user_id, filter_type)

        return jsonify(places)
    else:
        return render_template("my_places.html")


@app.route("/notes", methods=["GET", "POST"])
@login_required
def notes():
    user_id = session["user_id"]

    if request.method == "POST":
        # Get form data
        title = request.form.get("title")
        content = request.form.get("content")

        # Insert note into the database
        db.execute("INSERT INTO user_notes (user_id, title, content) VALUES (?, ?, ?)", user_id, title, content)

        flash("Note saved successfully!", "success")
        return redirect("/notes")

    else:
        # Fetch user's notes from the database
        notes = db.execute("SELECT title, content FROM user_notes WHERE user_id = ?", user_id)
        return render_template("notes.html", notes=notes)



if __name__ == "__main__":
    app.run(debug=True)
