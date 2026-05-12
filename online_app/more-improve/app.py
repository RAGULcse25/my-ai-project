```python
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskhorizon.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    avatar = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    projects = db.relationship('Project', backref='creator', lazy=True)
    tasks = db.relationship('Task', backref='assignee', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tasks = db.relationship('Task', backref='project', lazy=True, cascade='all, delete-orphan')

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    priority = db.Column(db.String(20), default='medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    projects = Project.query.filter_by(user_id=current_user.id).order_by(Project.created_at.desc()).limit(5).all()
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.deadline.asc()).limit(5).all()
    return render_template('dashboard.html', projects=projects, tasks=tasks)

@app.route('/projects')
@login_required
def projects():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'all')
    
    query = Project.query.filter_by(user_id=current_user.id)
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    projects = query.order_by(Project.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('projects.html', projects=projects, status_filter=status_filter)

# API Endpoints
@app.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': task.id,
        'title': task.title,
        'status': task.status,
        'priority': task.priority,
        'deadline': task.deadline.isoformat() if task.deadline else None,
        'project': task.project.title
    } for task in tasks])

# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Seed Data
def seed_data():
    with app.app_context():
        db.create_all()
        
        # Create admin user
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@taskhorizon.com')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            
            # Create sample projects
            projects = [
                Project(title='Website Redesign', description='Complete redesign of company website', user_id=admin.id),
                Project(title='Mobile App Development', description='Build cross-platform mobile app', user_id=admin.id)
            ]
            
            for project in projects:
                db.session.add(project)
            
            db.session.commit()
            
            # Create sample tasks
            tasks = [
                Task(title='Create wireframes', project_id=1, user_id=admin.id, status='in_progress', priority='high'),
                Task(title='Design UI components', project_id=1, user_id=admin.id, priority='medium'),
                Task(title='Setup development environment', project_id=2, user_id=admin.id, status='completed')
            ]
            
            for task in tasks:
                db.session.add(task)
            
            db.session.commit()

if __name__ == '__main__':
    seed_data()
    app.run(debug=True)
```