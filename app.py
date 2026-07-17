import os
import requests
from io import BytesIO
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from gtts import gTTS

app = Flask(__name__)
# Render requires a static secret key or one passed via environment variables
app.secret_key = os.getenv('SECRET_KEY', 'super-secret-ninja-key-198237')

# Database Setup - Points to a persistent directory or local sqlite file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Flask-Mail Setup
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')
mail = Mail(app)

# Fallback API Key safely injected
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "07bbe16acc404cc0b492b7b75f55e708")

# --- Database Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

# --- Custom Decorators ---
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'error')
            return redirect(url_for('login'))
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            flash('You do not have permission to view this page.', 'error')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

def get_news(query):
    """Helper function to fetch news from NewsAPI"""
    url = f"https://newsapi.org/v2/top-headlines?{query}&apiKey={NEWS_API_KEY}"
    try:
        response = requests.get(url, timeout=8).json()
        if response.get("status") == "ok":
            return response.get("articles", [])
    except Exception as e:
        print(f"News fetch error: {e}")
    return []

# --- Routes ---
@app.route('/')
@app.route('/category/<cat>')
def home(cat='headlines'):
    user = User.query.get(session['user_id']) if 'user_id' in session else None
    
    if cat == 'sports':
        articles = get_news("country=ke&category=sports&pageSize=9")
        title = "Kenya Sports News"
    elif cat == 'tech':
        articles = get_news("category=technology&language=en&pageSize=9")
        title = "Technology News"
    elif cat == 'world':
        articles = get_news("language=en&pageSize=9")
        title = "World Headlines"
    elif cat == 'health':
        articles = get_news("country=ke&category=health&pageSize=9")
        title = "Kenya Health News"
    elif cat == 'entertainment':
        articles = get_news("country=ke&category=entertainment&pageSize=9")
        title = "Kenya Entertainment News"
    elif cat == 'science':
        articles = get_news("category=science&language=en&pageSize=9")
        title = "Science News"
    else:
        articles = get_news("country=ke&pageSize=9")
        title = "Top Kenya Headlines"
        
    return render_template('home.html', user=user, articles=articles, title=title)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return redirect(url_for('register'))

        is_first_user = User.query.count() == 0
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_pw, is_admin=is_first_user)
        db.session.add(new_user)
        db.session.commit()

        if not is_first_user:
            try:
                msg = Message("New User Registration - Newsbotninja",
                              recipients=["odangalevi@gmail.com"])
                msg.body = f"A new user has registered on the platform.\nUsername: {username}\nEmail: {email}"
                mail.send(msg)
            except Exception as e:
                print(f"Failed to send email: {e}")

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            flash('Logged in successfully.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

@app.route('/voice-brief')
def voice_brief():
    articles = get_news("country=ke&pageSize=3")
    if not articles:
        return "Audio not available", 404

    script = "Newsbotninja briefing. Here are your top three Kenya stories today. "
    for i, art in enumerate(articles, 1):
        title = art["title"].split(" - ")[0]
        script += f"Story {i}. {title}. "

    audio_buffer = BytesIO()
    tts = gTTS(text=script, lang="en", slow=False)
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)

    return send_file(audio_buffer, mimetype="audio/mpeg")

@app.route('/admin')
@admin_required
def admin_dashboard():
    users = User.query.all()
    user_count = len(users)
    return render_template('admin.html', users=users, user_count=user_count)

@app.route('/admin/delete_user/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    user_to_delete = User.query.get_or_404(user_id)
    if user_to_delete.id == session['user_id']:
        flash('You cannot delete your own admin account!', 'error')
    else:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash(f'User {user_to_delete.username} deleted.', 'success')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
