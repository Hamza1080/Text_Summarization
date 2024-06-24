from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import google.generativeai as genai
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Configure the Google Generative AI
genai.configure(api_key=os.getenv("GEM_KEY"))

generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 50,
    "max_output_tokens": 1024
}

model = genai.GenerativeModel(
    "gemini-1.5-flash",
    generation_config=generation_config
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    texts = db.relationship('TextSummary', backref='author', lazy=True)

class TextSummary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_text = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    user_texts = TextSummary.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', texts=user_texts)

@app.route('/index', methods=['GET'])
@login_required
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
@login_required
def summarize():
    text_to_summarize = request.form['text_to_summarize']
    summary_size = request.form.get('summary_size', type=int, default=100)  # Default summary size if not provided

    try:
        prompt = f"Summarize the following text in approximately {summary_size} words, Do not include any pretext like 'Following is the summary of x', give direct answer: {text_to_summarize}"
        response = model.generate_content([prompt])
        summary = response.text

        # Save the text and summary to the database
        text_summary = TextSummary(original_text=text_to_summarize, summary=summary, user_id=current_user.id)
        db.session.add(text_summary)
        db.session.commit()
    except Exception as e:
        summary = None
        error = str(e)

    if summary:
        return render_template('summarize.html', original_text=text_to_summarize, summary=summary)
    else:
        return render_template('error.html', error=error)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
