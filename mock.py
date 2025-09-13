# mock.py
from app import app
from models.user import db, User
from models.book import Book
from models.book_categories import BookCategory
from models.order import Order, StatusEnum
from models.order_item import OrderItem
from decimal import Decimal

print("→ Using DB URI:", app.config.get("SQLALCHEMY_DATABASE_URI"))

with app.app_context():
    try:
        db.drop_all()
        db.create_all()

        # Categories
        categories = [
            BookCategory(name="Programming"),
            BookCategory(name="Web Development"),
        ]

        # Users
        users = [
            User(name="Alice", email="alice@example.com", password_hash="1234", role="user"),
            User(name="Bob", email="bob@example.com", password_hash="1234", role="stock_keeper"),
            User(name="Admin", email="admin@example.com", password_hash="1234", role="admin"),
        ]

        # Books
        books = [
            Book(
                title="Python 101",
                author="Guido",
                price=Decimal("299.00"),
                stock_quantity=5,
                image_path="python101.jpg",
                category=categories[0],
            ),
            Book(
                title="Flask Mastery",
                author="Miguel",
                price=Decimal("450.00"),
                stock_quantity=10,
                image_path="flask_mastery.jpg",
                category=categories[1],
            ),
        ]

        db.session.add_all(categories + users + books)
        db.session.commit()

        # Orders
        order1 = Order(
            user=users[0],   # Alice สั่งซื้อ
            status=StatusEnum.pending,
            total_amount=Decimal("749.00"),
        )

        # Order Items
        order1_item1 = OrderItem(
            order=order1,
            book=books[0],
            quantity=1,
            unit_price=Decimal("299.00"),
        )
        order1_item2 = OrderItem(
            order=order1,
            book=books[1],
            quantity=1,
            unit_price=Decimal("450.00"),
        )

        db.session.add_all([order1, order1_item1, order1_item2])
        db.session.commit()

        print("✅ Mock data inserted successfully!")

    except Exception as e:
        print("❌ Error while seeding mock data:", e)
