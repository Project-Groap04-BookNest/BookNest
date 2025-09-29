from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 👇 import models ให้ SQLAlchemy register mapper
from .user import User
from .book import Book
from .book_categories import BookCategory
from .order import Order
from .order_item import OrderItem
