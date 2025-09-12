from models import db
from sqlalchemy.orm import relationship

class BookCategory(db.Model):
    __tablename__ = "book_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    # one-to-many: Category → Books
    books = relationship("Book", back_populates="category")
