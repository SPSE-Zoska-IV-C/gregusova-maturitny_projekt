from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename
from models import db, Article  # Import the single `db` instance and Article model
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bucketlist.db'  # Use a single database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize the database with the app
db.init_app(app)

# Models
class MyList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)


# Routes
@app.route('/')
@app.route('/mylist')
def mylist():
    items = MyList.query.all()  # Fetch all items from MyList
    return render_template('mylist.html', items=items)  # Pass 'items' to the template


@app.route('/inspiration')
def inspiration():
    travel_cards = [
        {"id": 1, "image": "img/cruise.jpg", "title": "Go to cruise", "description": "Cruise the seas."},
        {"id": 2, "image": "img/japan.jpg", "title": "Visit Japan", "description": "Explore Japan."},
        {"id": 7, "image": "img/sweden.jpg", "title": "Visit Sweden", "description": "Week long trip to Sweden."},
        {"id": 8, "image": "img/iceland.jpg", "title": "Visit Iceland", "description": "Road trip throughe ring of the Iceland."},
    ]
    learn_cards = [
        {"id": 3, "image": "img/german.jpg", "title": "Study German language", "description": "Learn German."},
        {"id": 4, "image": "img/guitar.jpg", "title": "Learn to play guitar", "description": "Master guitar."},
        {"id": 9, "image": "img/knit.jpg", "title": "Learn knitting", "description": "knit my own socks."},
        {"id": 10, "image": "img/harp.jpg", "title": "Learnto play harp", "description": "Be able to play at my grandmas funeral"},
    ]
    other_cards = [
        {"id": 5, "image": "img/baloon.jpg", "title": "Fly a hot air balloon", "description": "Soar in a balloon."},
        {"id": 6, "image": "img/camping.jpg", "title": "Go camping", "description": "Experience nature."},
        {"id": 11, "image": "img/diving.jpg", "title": "Diving in Australia", "description": "Go and drown someone you do not like"},
        {"id": 12, "image": "img/roadtrip.jpg", "title": "Go to road trip", "description": "road trip throuh south-east asia with your bestie"},
    ]
    return render_template(
        'inspiration.html',
        travel_cards=travel_cards,
        learn_cards=learn_cards,
        other_cards=other_cards,
    )


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('content')  # You might want to save this as `description`
        file = request.files.get('image')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_url = filepath  # Use uploaded file path
        else:
            image_url = 'static/default.jpg'  # Fallback image

        # Add the new item to MyList
        new_item = MyList(title=title, description=description, image_url=image_url)
        db.session.add(new_item)
        db.session.commit()

        flash('Item added to My List!', 'success')
        return redirect(url_for('mylist'))

    return render_template('create.html')


@app.route('/delete_article/<int:item_id>', methods=['POST'])
def delete_article(item_id):
    item = MyList.query.get_or_404(item_id)  # Fetch the item by ID
    db.session.delete(item)
    db.session.commit()
    flash('Item marked as achieved and removed from My List!', 'success')
    return redirect(url_for('mylist'))  # Redirect to 'mylist' page
  # Redirect back to the My List page


@app.route('/add_to_mylist', methods=['POST'])
def add_to_mylist():
    title = request.form.get('title')
    description = request.form.get('description')
    image_url = request.form.get('image_url')

    # Check if the item already exists in MyList
    existing_item = MyList.query.filter_by(title=title).first()  # You can also check by description or other fields if needed

    if existing_item:
        flash('This item is already in your list!', 'warning')
        return redirect(url_for('inspiration'))  # Redirect to inspiration page if item already exists

    # If no duplicate, create a new item and add it to MyList
    new_item = MyList(title=title, description=description, image_url=image_url)
    db.session.add(new_item)
    db.session.commit()

    flash('Item added to My List!', 'success')
    return redirect(url_for('mylist'))  # Redirect to My List page


# Helper Function
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# Create tables before the first request
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
