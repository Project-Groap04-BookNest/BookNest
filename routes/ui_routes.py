from flask import Blueprint, render_template, request, redirect, url_for
from models.user import User

ui_bp = Blueprint("ui", __name__)  # ชื่อ blueprint  มันจะไป map กับตัว html 

@ui_bp.route("/")
def index():
    return render_template("index.html")

@ui_bp.route("/login",endpoint = "login" , methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email, password_hash=password).first()
        if user:
            return redirect(url_for("ui.index"))  # ต้องเรียก "ui.index"
        else:
            return render_template("login.html", error="Password incorrect.")
    return render_template("login.html")

@ui_bp.route("/orders")
def orders():
    return render_template("orders.html")

@ui_bp.route("/manage_books")
def manage_books():
    from models.book import Book
    books = Book.query.all()
    return render_template("manage_books.html", books=books)

@ui_bp.route("/manage_users")
def manage_users():
    return render_template("manage_users.html")
