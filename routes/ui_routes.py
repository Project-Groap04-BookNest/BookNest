from flask import Blueprint, render_template, request, redirect, url_for
from models.user import User
from models import db # เอาไว้บันทึกลง DB 
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from functools import wraps
from flask import abort # เอาไว้แสดง error 403
from flask import session 
#ตัว hash password ของ flak สำหรับ reg

ui_bp = Blueprint("ui", __name__)  # ชื่อ blueprint  มันจะไป map กับตัว html 

@ui_bp.route("/")
def index():
    return render_template("index.html")

@ui_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        # ❌ อย่าใช้ check_password_hash
        # ✅ เทียบ plain text ตรง ๆ
        if user and user.password_hash == password:
            session["user_id"] = user.id
            session["user_name"] = user.name
            session["user_role"] = user.role
            session["user_email"] = user.email
            return redirect(url_for("ui.index"))
        else:
            return render_template("login.html", error="Email หรือ Password ไม่ถูกต้อง")

    return render_template("login.html")


@ui_bp.route("/logout")
def logout():
    session.clear()  # ลบ session ทั้งหมด
    return redirect(url_for("ui.index"))


@ui_bp.route("/orders")
def orders():
    return render_template("orders.html")

@ui_bp.route("/manage_books")
def manage_books():
    from models.book import Book
    books = Book.query.all()
    return render_template("manage_books.html", books=books)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # ต้อง login ก่อน
        if "user_id" not in session:
            return abort(403)

        # ต้องเป็น admin
        if session.get("user_role") != "admin" or session.get("user_email") != "admin@example.com":
            return abort(403)

        return f(*args, **kwargs)
    return decorated_function


@ui_bp.route("/manage_users")
@admin_required
def manage_users():
    from models.user import User
    users = User.query.all()
    return render_template("manage_users.html", users=users)

@ui_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        # เช็คว่า email ซ้ำหรือเปล่า
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template("register.html", error="อีเมลนี้ถูกใช้งานแล้ว")

        # ❌ ไม่ต้อง hash แล้ว
        # hashed_pw = generate_password_hash(password)

        # ✅ เก็บ plain text ไปเลย
        new_user = User(name=name, email=email, password_hash=password, role="user")
        db.session.add(new_user)
        db.session.commit()

        # สมัครเสร็จ -> auto login
        session["user_id"] = new_user.id
        session["user_name"] = new_user.name
        session["user_role"] = new_user.role

        return redirect(url_for("ui.index"))

    return render_template("register.html")
