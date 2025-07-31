# mock.py
from app import app
#from models.user import db, User
#from models.book import Book
import uuid

with app.app_context():
    db.drop_all()
    db.create_all()

    users = [
        User(id=str(uuid.uuid4()), name="Alice", email="alice@example.com", password_hash="1234", role="user"),
        User(id=str(uuid.uuid4()), name="Bob", email="bob@example.com", password_hash="1234", role="stock_keeper"),
        User(id=str(uuid.uuid4()), name="Admin", email="admin@example.com", password_hash="1234", role="admin")
    ]

    books = [
        Book(title="Python 101", author="Guido", price=299.0, stock_quantity=5, image_path="python101.jpg"),
        Book(title="Flask Mastery", author="Miguel", price=450.0, stock_quantity=10, image_path="flask_mastery.jpg")
    ]

    db.session.add_all(users + books)
    db.session.commit()
    print("✅ Mock data loaded!")
