from models import db
from sqlalchemy.orm import relationship

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    
    # FK ไปที่ Order
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    order = relationship("Order", back_populates="items")

    # FK ไปที่ Book
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    book = relationship("Book", back_populates="order_items")

    # จำนวนที่ซื้อ
    quantity = db.Column(db.Integer, nullable=False)

    # ราคาต่อหน่วยตอนซื้อ
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)