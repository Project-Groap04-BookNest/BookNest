from models import db
from sqlalchemy.orm import relationship

from sqlalchemy import DateTime, func

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    # FK ไปที่ Order
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    order = relationship("Order", back_populates="items")
    # Snapshot ข้อมูลหนังสือตอนสร้างออเดอร์เพื่อไม่ผูกกับตาราง books โดยตรง
    book_title = db.Column(db.String(200), nullable=False)
    book_author = db.Column(db.String(100), nullable=False)
    book_image_path = db.Column(db.String(200), nullable=True)
    # จำนวนที่ซื้อ
    quantity = db.Column(db.Integer, nullable=False)
    # ราคาต่อหน่วยตอนซื้อ
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    # เวลาที่สร้างรายการ
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())
