from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import os  # Add this import

app = Flask(__name__)

# Get the path to the Desktop dynamically
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "tourism.db")

# Configure the database URI to point to the Desktop location
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{desktop_path}"
app.config['SECRET_KEY'] = 'mysecret'
db = SQLAlchemy(app)

# Database Models

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    reviews = db.relationship('Review', backref='author', lazy='dynamic')
    complaints = db.relationship('Complaint', backref='author', lazy='dynamic')

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place_name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    complaint_text = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='Pending')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        new_user = User(username=username, email=email)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Username or email already exists.', 'danger')
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'POST':
        place_name = request.form['place_name']
        rating = int(request.form['rating'])
        review_text = request.form['review_text']
        user_id = 1  # Replace with session-based user authentication
        new_review = Review(place_name=place_name, rating=rating, review_text=review_text, user_id=user_id)
        db.session.add(new_review)
        db.session.commit()
        flash('Review submitted successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('review.html')

@app.route('/complaint', methods=['GET', 'POST'])
def complaint():
    if request.method == 'POST':
        complaint_text = request.form['complaint_text']
        user_id = 1  # Replace with session-based user authentication
        new_complaint = Complaint(complaint_text=complaint_text, user_id=user_id)
        db.session.add(new_complaint)
        db.session.commit()
        flash('Complaint submitted successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('complaint.html')

@app.route('/helplines')
def helplines():
    return render_template('helplines.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
