from models import db
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    orders = relationship("Order", back_populates="user")

    def __repr__(self):
        return f'<User {self.email}>'