from importlib.metadata import requires
from flask import Blueprint , jsonify, request
from models.book import Book
from models.user import User
from app import db   # ต้อง import db จาก app ที่คุณ init ไว้

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/get_books", methods=["GET"])
def get_books():
    books = Book.query.all()
    return jsonify([
        {
            "id": b.id,
            "title": b.title,
            "author": b.author,
            "price": str(b.price),   # แปลง Decimal → string
            "stock_quantity": b.stock_quantity
        } for b in books
    ])

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
