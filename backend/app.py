from datetime import datetime
from flask import Flask, redirect, render_template, request, jsonify, url_for, flash
import os
from werkzeug.utils import secure_filename
from services.document_processing.pdf_extractor import extract_pdf_text
from models.legal_research_model import ask_legal_question
from services.summarization.summarizer_service import summarize_text
from services.simplification.simplifier_service import simplify_summary  # Import the simplifier service
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# MySQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mypassword@127.0.0.1:3306/newdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Generate and set a secret key for your application
app.config['SECRET_KEY'] = 'acc82c31a1412e564cb11b5b45af32c7c7d7b1892d5d1063'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Define User and ChatHistory models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    chats = db.relationship('ChatHistory', backref='owner', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    query = db.Column(db.String(500), nullable=False)
    response = db.Column(db.String(1000), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ChatHistory {self.id}>'

# Create the database tables
with app.app_context():
    db.create_all()

# Allowed file function
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(request.args.get('next') or url_for('home'))
        else:
            flash('Login failed. Check your credentials and try again.', 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()
        flash('Signup successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    if request.method == 'POST':
        user_input = request.form.get('prompt')
        if user_input:
            # Ensure you have imported ask_legal_question correctly
            response = ask_legal_question(user_input)
            
            # Save chat history
            new_chat = ChatHistory(query=user_input, response=response, user_id=current_user.id)
            db.session.add(new_chat)
            db.session.commit()
            
            return jsonify({'response': response})
    
    # For GET request, render the chat.html page
    return render_template('chat.html')

@app.route('/summary')
@login_required
def summary():
    return render_template('summary.html')

@app.route('/upload', methods=['POST'])
@login_required
def upload():
    if 'file' not in request.files:
        flash('No file part.', 'danger')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected.', 'warning')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        extracted_text = extract_pdf_text(filepath)
        
        if not extracted_text or len(extracted_text.strip()) == 0:
            flash('The extracted text is empty.', 'danger')
            return render_template('summary.html', error="The extracted text is empty.")
        
        # Generate the initial summary
        summary_text = summarize_text(extracted_text)
        
        return render_template('summary.html', extracted_text=extracted_text, summary_text=summary_text)
    
    flash('Invalid file type.', 'danger')
    return redirect(request.url)

@app.route('/simplify', methods=['POST'])
@login_required
def simplify():
    extracted_text = request.form.get('extracted_text')
    if not extracted_text:
        flash('No text provided for simplification.', 'warning')
        return redirect(url_for('summary'))
    
    simplified_text = simplify_summary(extracted_text)
    return render_template('summary.html', extracted_text=extracted_text, summary_text=None, simplified_text=simplified_text)

@app.route('/api/chat', methods=['POST'])
@login_required
def chat_api():
    user_input = request.json.get('message')
    if user_input:
        response = ask_legal_question(user_input)

        new_chat = ChatHistory(query=user_input, response=response, user_id=current_user.id)
        db.session.add(new_chat)
        db.session.commit()

        return jsonify({'response': response})

    return jsonify({'response': 'No input provided.'}), 400

# Ensure uploads directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if __name__ == '__main__':
    app.run(debug=True, threaded=True, use_reloader=False, host='0.0.0.0', port=5000)
