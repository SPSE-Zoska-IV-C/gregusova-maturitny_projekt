import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from models import db, Book  # Import the single `db` instance and Book model
from datetime import datetime

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookapp.db'  # Renamed to bookapp
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize the database with the app
db.init_app(app)

# Routes for Book App
@app.route('/')
def index():
    # Get all books from the database
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        try:
            # Get form data
            title = request.form['title']
            author = request.form['author']
            genre = request.form['genre']
            pages = int(request.form['pages'])
            cover = request.form['cover']
            
            # Determine status based on form input
            status = request.form.get('status', 'Reading Now')
            
            # Get optional fields
            notes = request.form.get('notes', '')
            rating = request.form.get('rating')
            pages_read = request.form.get('pages_read', 0)
            
            # Dates
            start_date_str = request.form.get('start_date')
            finish_date_str = request.form.get('finish_date')
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
            finish_date = datetime.strptime(finish_date_str, '%Y-%m-%d').date() if finish_date_str else None

            # Simple validation
            if status == 'Reading Now' and not start_date:
                flash('Please pick a start date.', 'error')
                return render_template('create.html')
            if status == 'Already Read' and (not start_date or not finish_date):
                flash('Please pick start and finish dates.', 'error')
                return render_template('create.html')

            # Convert rating to int if provided
            if rating:
                rating = int(rating)
            else:
                rating = None
                
            # Convert pages_read to int
            pages_read = int(pages_read) if pages_read else 0
            
            # Create new book instance
            new_book = Book(
                title=title,
                author=author,
                genre=genre,
                pages=pages,
                cover=cover,
                notes=notes,
                rating=rating,
                status=status,
                pages_read=pages_read,
                start_date=start_date,
                finish_date=finish_date
            )
            
            # Save to database
            db.session.add(new_book)
            db.session.commit()
            
            flash('Book added successfully!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f'Error adding book: {str(e)}', 'error')
            return render_template('create.html')
    
    return render_template('create.html')

@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('book_detail.html', book=book)

@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    if request.method == 'POST':
        try:
            # Update book fields
            book.title = request.form['title']
            book.author = request.form['author']
            book.genre = request.form['genre']
            book.pages = int(request.form['pages'])
            book.cover = request.form['cover']
            book.status = request.form.get('status', 'Reading Now')
            book.notes = request.form.get('notes', '')
            
            rating = request.form.get('rating')
            if rating:
                book.rating = int(rating)
            
            pages_read = request.form.get('pages_read', 0)
            book.pages_read = int(pages_read) if pages_read else 0
            
            db.session.commit()
            flash('Book updated successfully!', 'success')
            return redirect(url_for('book_detail', book_id=book.id))
            
        except Exception as e:
            flash(f'Error updating book: {str(e)}', 'error')
    
    return render_template('edit.html', book=book)

@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    try:
        db.session.delete(book)
        db.session.commit()
        flash('Book deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting book: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/reading')
def reading():
    books = Book.query.filter_by(status='Reading Now').all()
    return render_template('reading.html', books=books)

@app.route('/want_to_read')
def want_to_read():
    books = Book.query.filter_by(status='Want to Read').all()
    return render_template('want_to_read.html', books=books)

@app.route('/finished')
def finished():
    books = Book.query.filter_by(status='Finished').all()
    return render_template('finished.html', books=books)

# Helper Function
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Create tables before the first request
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
