from importlib.metadata import requires
from flask import Blueprint , jsonify
from models.book import Book
from models.user import User

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