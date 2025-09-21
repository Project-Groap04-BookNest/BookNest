from flask import Blueprint , jsonify
from models.book import Book #import ข้อมูลจาก table book 

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