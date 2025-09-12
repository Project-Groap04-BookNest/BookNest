from models import db
from sqlalchemy.orm import relationship
from sqlalchemy import DateTime , func , Enum , Numeric
import enum

class StatusEnum(enum.Enum):
    pending = 'pending'
    paid = 'paid'
    shipped = 'shipped'
    canceled = 'canceled'

class order(db.Model):
    # ชื่อ table
    __tablename__ = 'order'
    # PK
    id = db.Column(db.Integer, primary_key=True) 

    # เวลาที่สร้างorder
    created_at = db.Column(DateTime(timezone=True), sever_default=func.now())

    # Enum สถานะการสั่งซื้อ
    status = db.Column(Enum(StatusEnum), nullable = False)

    # ราคารวมของ order 
    total_amount = db.Column(Numeric(10, 2), nullable=False)

    #เชื่อม FK จาก table user
    user_id = db.Column(db.Integer , db.ForeignKey('users.id'))
    user = relationship("User", back_populates="orders")