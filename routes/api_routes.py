from flask import Blueprint, jsonify, request, session
from models.book import Book
from models.order import Order
from models.order_item import OrderItem
from models.book import Book
from models.user import User
from app import db
from importlib.metadata import requires   


api_bp = Blueprint("api", __name__, url_prefix="/api")

# ตรวจสอบ login
def require_login():
    if "user_id" not in session:
        return False
    return True

#api get_book
@api_bp.route("/get_books", methods=["GET"])
def get_books():
    if not require_login():
        return jsonify({"error": "Please login first"}), 401
    books = Book.query.all()

    return jsonify([{
        "id": b.id,
        "title": b.title,
        "author": b.author,
        "price": str(b.price),
        "stock_quantity": b.stock_quantity,
        "image_path": b.image_path if b.image_path else "assets/if_book_error.png"
    } for b in books])

# เพิ่ม/ลดจำนวนหนังสือ (stock)
@api_bp.route("/books/<int:book_id>/stock", methods=["POST"])
def update_book_stock(book_id):
    if not require_login():
        return jsonify({"error": "Please login first"}), 401
    data = request.get_json()
    action = data.get("action")  # 'increase' or 'decrease'
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    if action == "increase":
        book.stock_quantity += 1
    elif action == "decrease":
        if book.stock_quantity > 0:
            book.stock_quantity -= 1
    else:
        return jsonify({"error": "Invalid action"}), 400
    db.session.commit()
    return jsonify({"message": "Stock updated", "stock_quantity": book.stock_quantity})

# ลบหนังสือ
@api_bp.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    if not require_login():
        return jsonify({"error": "Please login first"}), 401
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"})

# แก้ไขข้อมูลหนังสือ
@api_bp.route("/books/<int:book_id>", methods=["PUT"])
def edit_book(book_id):
    if not require_login():
        return jsonify({"error": "Please login first"}), 401
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    data = request.get_json()
    book.title = data.get("title", book.title)
    book.author = data.get("author", book.author)
    book.price = data.get("price", book.price)
    book.stock_quantity = data.get("stock_quantity", book.stock_quantity)
    book.image_path = data.get("image_path", book.image_path)
    db.session.commit()
    return jsonify({"message": "Book updated"})

# เพิ่มหนังสือใหม่
@api_bp.route("/books", methods=["POST"])
def add_book():
    if not require_login():
        return jsonify({"error": "Please login first"}), 401
    data = request.get_json()
    title = data.get("title")
    author = data.get("author")
    price = data.get("price")
    stock_quantity = data.get("stock_quantity")
    image_path = data.get("image_path", "assets/if_book_error.png")
    if not all([title, author, price, stock_quantity]):
        return jsonify({"error": "Missing required fields"}), 400
    book = Book(title=title, author=author, price=price, stock_quantity=stock_quantity, image_path=image_path)
    db.session.add(book)
    db.session.commit()
    return jsonify({"message": "Book added", "book_id": book.id})



### api get_users
@api_bp.route("/get_users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([
        {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "role": u.role

        } for u in users
    ])

@api_bp.route("/users/<int:user_id>/role", methods=["GET", "PUT"]) # ex /users/1/role
def user_role(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if request.method == "GET":
        # คืนค่า role ของ user
        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        })

    elif request.method == "PUT":
        # อัปเดต role
        data = request.get_json()
        new_role = data.get("role")

        if not new_role:
            return jsonify({"error": "Missing 'role' in request body"}), 400

        allowed_roles = ["user", "stock_keeper", "admin"]
        if new_role not in allowed_roles:
            return jsonify({"error": f"Invalid role. Allowed: {allowed_roles}"}), 400

        user.role = new_role
        db.session.commit()

        return jsonify({
            "message": "Role updated successfully",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
        })


# api get_cart
@api_bp.route("/cart", methods=["GET"])
def get_cart():
    cart = session.get("cart", {})
    items, total = [], 0
    for book_id, qty in cart.items():
        book = Book.query.get(int(book_id))
        if book:
            subtotal = book.price * qty
            items.append({
                "id": book.id,
                "title": book.title,
                "price": str(book.price),
                "quantity": qty,
                "subtotal": str(subtotal)
            })
            total += subtotal
    return jsonify({"items": items, "total": str(total)})

@api_bp.route("/cart", methods=["POST"])
def add_to_cart():
    if not require_login():
        return jsonify({"error": "Please login first"}), 401
    data = request.get_json()
    book_id = int(data.get("book_id"))
    qty = int(data.get("quantity", 1))
    cart = session.get("cart", {})
    key = str(book_id)
    cart[key] = cart.get(key, 0) + qty
    session["cart"] = cart
    session.modified = True
    return jsonify({"message": "Added to cart", "cart": cart})


@api_bp.route("/cart/<book_id>", methods=["PUT"])
def update_cart_item(book_id):
    if not require_login():
        return jsonify({"error": "Please login first"}), 401
    data = request.get_json()
    qty = int(data.get("quantity", 1))
    cart = session.get("cart", {})
    if book_id in cart:
        if qty > 0:
            cart[book_id] = qty
        else:
            del cart[book_id]
    session["cart"] = cart
    session.modified = True
    return jsonify({"message": "Updated cart", "cart": cart})


@api_bp.route("/cart/<book_id>", methods=["DELETE"])
def delete_cart_item(book_id):
    if not require_login():
        return jsonify({"error": "Please login first"}), 401
    cart = session.get("cart", {})
    if book_id in cart:
        del cart[book_id]
    session["cart"] = cart
    session.modified = True
    return jsonify({"message": "Item removed", "cart": cart})



## api checkout 

@api_bp.route("/checkout", methods=["POST"])
def checkout():
    if not require_login():
        return jsonify({"error": "Please login first"}), 401
    cart = session.get("cart", {})
    if not cart:
        return jsonify({"error": "Cart is empty"}), 400

    order = Order(total_amount=0)
    db.session.add(order)
    total = 0
    for book_id, qty in cart.items():
        book = Book.query.get(int(book_id))
        if book and book.stock_quantity >= qty:
            subtotal = book.price * qty
            order_item = OrderItem(
                order=order,
                book_id=book.id,
                quantity=qty,
                price=book.price
            )
            db.session.add(order_item)
            book.stock_quantity -= qty
            total += subtotal
    order.total_amount = total
    db.session.commit()

    session["cart"] = {}
    session.modified = True

    return jsonify({"message": "Checkout successful", "order_id": order.id})