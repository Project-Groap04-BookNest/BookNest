# routes/ui_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort, current_app
from functools import wraps
import os

# ==== Models / DB ====
from models import db
from models.user import User
from models.book import Book
from models.order import Order
from models.order_item import OrderItem

ui_bp = Blueprint("ui", __name__)

# ========================
# Auth / Role decorators
# ========================
def stock_keeper_or_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return abort(403)
        if session.get("user_role") not in ["admin", "stock_keeper"]:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return abort(403)
        if session.get("user_role") != "admin" or session.get("user_email") != "admin@example.com":
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function

# ========================
# Helpers
# ========================
def _cart_items_and_total():
    cart = session.get("cart", {})
    items, total = [], 0
    for book_id, qty in cart.items():
        book = Book.query.get(int(book_id))
        if not book:
            continue
        subtotal = book.price * qty
        items.append({
            "id": book.id,
            "title": book.title,
            "price": book.price,
            "quantity": qty,
            "subtotal": subtotal
        })
        total += subtotal
    return items, total

def _safe_image_path(image_path: str | None) -> str:
    """คืน path รูปใน static ถ้าไฟล์หายให้ fallback เป็น assets/if_book_error.png"""
    fallback = "assets/if_book_error.png"
    path = image_path or fallback
    if not os.path.exists(os.path.join(current_app.static_folder, path)):
        return fallback
    return path

# ========================
# Public pages
# ========================
@ui_bp.route("/")
def index():
    import re
    from models.book_categories import BookCategory

    def series_base(title: str) -> str:
        # ตัดคำระบุเล่ม/ภาค/ตอน ออก เพื่อจับชื่อซีรีส์ฐาน
        base = re.sub(r"\s*(?:เล่ม|Vol(?:ume)?|ตอนที่|ภาค)\s*\d+.*$", "", title, flags=re.IGNORECASE)
        return base.strip()

    def volume_no(title: str) -> int:
        # ดึงเลขเล่ม ถ้าไม่เจอให้เป็นค่าใหญ่ ๆ เพื่อไปอยู่ท้ายซีรีส์นั้น
        m = re.search(r"(?:เล่ม|Vol(?:ume)?|ตอนที่|ภาค)\s*(\d+)", title, flags=re.IGNORECASE)
        return int(m.group(1)) if m else 10**9

    categories = BookCategory.query.order_by(BookCategory.name.asc()).all()
    grouped = []

    for c in categories:
        # ถ้ามี relationship c.books ใช้ list(...) ให้แน่ใจว่าเรา sort ใน Python ได้
        books_q = getattr(c, "books", None)
        if hasattr(books_q, "all"):   # lazy='dynamic'
            books_list = books_q.all()
        elif books_q is not None:
            books_list = list(books_q)
        else:
            books_list = Book.query.filter_by(category_id=c.id).all()

        # ทำรูปให้ปลอดภัย + จัดเรียง: ซีรีส์ -> เลขเล่ม -> title -> id
        safe = []
        for b in books_list:
            img = getattr(b, "image_path", None) or "assets/if_book_error.png"
            full = os.path.join(current_app.static_folder, img)
            b.image_path = img if os.path.exists(full) else "assets/if_book_error.png"
            safe.append(b)

        safe_sorted = sorted(
            safe,
            key=lambda x: (series_base(x.title), volume_no(x.title), x.title, x.id)
        )

        if safe_sorted:
            grouped.append({"name": c.name, "books": safe_sorted})

    # เผื่อหนังสือที่ไม่มีหมวด
    uncategorized = Book.query.filter(Book.category_id.is_(None)).all()
    if uncategorized:
        for b in uncategorized:
            img = getattr(b, "image_path", None) or "assets/if_book_error.png"
            full = os.path.join(current_app.static_folder, img)
            b.image_path = img if os.path.exists(full) else "assets/if_book_error.png"
        uncategorized_sorted = sorted(
            uncategorized,
            key=lambda x: (series_base(x.title), volume_no(x.title), x.title, x.id)
        )
        grouped.append({"name": "อื่น ๆ", "books": uncategorized_sorted})

    return render_template("index.html", grouped_categories=grouped)


@ui_bp.route("/orders")     # endpoint: ui.orders
def orders():
    items, total = _cart_items_and_total()
    return render_template("orders.html", items=items, total=total)

# ========================
# Cart actions (no JS)
# ========================
@ui_bp.route("/add-to-cart/<int:book_id>")
def add_to_cart(book_id):
    cart = session.get("cart", {})
    cart[str(book_id)] = cart.get(str(book_id), 0) + 1
    session["cart"] = cart
    session.modified = True
    return redirect(url_for("ui.orders"))

@ui_bp.route("/update-qty/<int:book_id>/<int:qty>")
def update_qty(book_id, qty):
    cart = session.get("cart", {})
    key = str(book_id)
    if key in cart:
        if qty > 0:
            cart[key] = qty
        else:
            del cart[key]
    session["cart"] = cart
    session.modified = True
    return redirect(url_for("ui.orders"))

@ui_bp.route("/remove-item/<int:book_id>")
def remove_item(book_id):
    cart = session.get("cart", {})
    key = str(book_id)
    if key in cart:
        del cart[key]
    session["cart"] = cart
    session.modified = True
    return redirect(url_for("ui.orders"))

@ui_bp.route("/checkout")
def checkout():
    cart = session.get("cart", {})
    if not cart:
        return redirect(url_for("ui.orders"))

    order = Order(total_amount=0)
    db.session.add(order)
    total = 0

    for book_id, qty in cart.items():
        book = Book.query.get(int(book_id))
        if book and book.stock_quantity >= qty:
            subtotal = book.price * qty
            # ชื่อฟิลด์ราคาใช้ 'price' ให้ตรงกับ API checkout เดิมของโปรเจค
            db.session.add(OrderItem(
                order=order,
                book_id=book.id,
                quantity=qty,
                price=book.price
            ))
            book.stock_quantity -= qty
            total += subtotal

    order.total_amount = total
    db.session.commit()

    session["cart"] = {}
    session.modified = True
    return redirect(url_for("ui.orders"))

# ========================
# Auth pages
# ========================
@ui_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        # ใช้ plain text ตามที่ไฟล์เดิมเขียนไว้
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
    session.clear()
    return redirect(url_for("ui.index"))

@ui_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template("register.html", error="อีเมลนี้ถูกใช้งานแล้ว")

        new_user = User(name=name, email=email, password_hash=password, role="user")
        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id
        session["user_name"] = new_user.name
        session["user_role"] = new_user.role
        session["user_email"] = new_user.email

        return redirect(url_for("ui.index"))

    return render_template("register.html")

# ========================
# Management pages
# ========================
@ui_bp.route("/manage_books", methods=["GET", "POST"])
@stock_keeper_or_admin_required
def manage_books():
    from models.book_categories import BookCategory
    if request.method == "POST":
        action = request.form.get("action")
        book_id = request.form.get("book_id")

        if action == "add":
            title = request.form.get("title")
            author = request.form.get("author")
            price = request.form.get("price")
            stock_quantity = request.form.get("stock_quantity")
            image_path = request.form.get("image_path") or "assets/if_book_error.png"
            category_id = request.form.get("category_id")
            new_category_name = request.form.get("new_category")

            if new_category_name:
                category = BookCategory.query.filter_by(name=new_category_name).first()
                if not category:
                    category = BookCategory(name=new_category_name)
                    db.session.add(category)
                    db.session.commit()
                category_id = category.id

            if title and author and price and stock_quantity and category_id:
                new_book = Book(
                    title=title, author=author, price=price,
                    stock_quantity=stock_quantity, image_path=image_path, category_id=category_id
                )
                db.session.add(new_book)
                db.session.commit()
                flash("เพิ่มหนังสือสำเร็จ", "success")

        elif action == "delete" and book_id:
            book = Book.query.get(book_id)
            if book:
                db.session.delete(book)
                db.session.commit()
                flash("ลบหนังสือสำเร็จ", "success")

        elif action == "edit" and book_id:
            book = Book.query.get(book_id)
            if book:
                book.title = request.form.get("title", book.title)
                book.author = request.form.get("author", book.author)
                book.price = request.form.get("price", book.price)
                book.stock_quantity = request.form.get("stock_quantity", book.stock_quantity)
                book.image_path = request.form.get("image_path", book.image_path)
                category_id = request.form.get("category_id")
                new_category_name = request.form.get("new_category")

                if new_category_name:
                    category = BookCategory.query.filter_by(name=new_category_name).first()
                    if not category:
                        category = BookCategory(name=new_category_name)
                        db.session.add(category)
                        db.session.commit()
                    category_id = category.id
                if category_id:
                    book.category_id = category_id

                db.session.commit()
                flash("แก้ไขข้อมูลหนังสือสำเร็จ", "success")

        elif action == "increase_stock" and book_id:
            book = Book.query.get(book_id)
            if book:
                book.stock_quantity += 1
                db.session.commit()

        elif action == "decrease_stock" and book_id:
            book = Book.query.get(book_id)
            if book and book.stock_quantity > 0:
                book.stock_quantity -= 1
                db.session.commit()

        return redirect(url_for("ui.manage_books"))

    books = Book.query.order_by(Book.id.asc()).all()
    # safe image path
    for book in books:
        book.image_path = _safe_image_path(getattr(book, "image_path", None))

    from models.book_categories import BookCategory
    categories = BookCategory.query.order_by(BookCategory.name).all()
    return render_template("manage_books.html", books=books, categories=categories)

@ui_bp.route("/manage_users", methods=["GET", "POST"])
@admin_required
def manage_users():
    users = User.query.all()

    if request.method == "POST":
        user_id = request.form.get("user_id")
        new_role = request.form.get("role")

        user = User.query.get(user_id)
        if user:
            if new_role in ["user", "stock_keeper", "admin"]:
                user.role = new_role
                db.session.commit()
                flash(f"Role ของ {user.email} ถูกเปลี่ยนเป็น {new_role}", "success")
            else:
                flash("Role ไม่ถูกต้อง", "error")
        else:
            flash("User ไม่พบ", "error")

        return redirect(url_for("ui.manage_users"))

    return render_template("manage_users.html", users=users)

# Error handler
@ui_bp.app_errorhandler(403)
def forbidden(e):
    return render_template("404.html"), 403
