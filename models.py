from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each book
    title = db.Column(db.String(255), nullable=False)  # Title of the book
    author = db.Column(db.String(255), nullable=False)  # Author of the book
    genre = db.Column(db.String(255), nullable=False)  # Genre of the book
    pages = db.Column(db.Integer, nullable=False)  # Number of pages
    cover = db.Column(db.String(255), nullable=False)  # Path to the cover image
    notes = db.Column(db.Text, nullable=True)  # Notes about the book (optional)
    rating = db.Column(db.Integer, nullable=True)  # Rating (1-5 stars, optional)
    status = db.Column(db.String(50), nullable=False)  # Reading status ("Reading Now" or "Already Read")
    pages_read = db.Column(db.Integer, nullable=True, default=0)  # Pages read (for "Reading Now" status)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)  # Date when the book was added

    def __repr__(self):
        return f"<Book {self.title}>"

    def __str__(self):
        return self.title
