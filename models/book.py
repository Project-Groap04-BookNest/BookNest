from models import db
from sqlalchemy.orm import relationship
from sqlalchemy import Numeric

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(Numeric(10, 2), nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(200), nullable=True)

    # เชื่อมไปยัง OrderItem
    order_items = relationship("OrderItem", back_populates="book")

    # FK ไปยัง Category
    category_id = db.Column(db.Integer, db.ForeignKey("book_categories.id"), nullable=False)
    category = relationship("BookCategory", back_populates="books")

    def __repr__(self):
        return f'<Book {self.title}>'
