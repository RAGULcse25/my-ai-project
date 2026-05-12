from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE = '2048_game.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db_connection()
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                score INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        db.commit()

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        db = get_db_connection()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        
        db = get_db_connection()
        try:
            db.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                      (username, hashed_password))
            db.commit()
            flash('Registration successful! Please login.')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/game', methods=['POST'])
def game():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    direction = request.form['direction']
    # Implement game logic here
    # Update grid, calculate score, etc.
    
    # Example score update
    score = random.randint(100, 1000)
    db = get_db_connection()
    db.execute('INSERT INTO scores (user_id, score) VALUES (?, ?)',
               (session['user_id'], score))
    db.commit()
    
    return redirect(url_for('index'))

@app.route('/highscores')
def highscores():
    db = get_db_connection()
    scores = db.execute('''
        SELECT users.username, MAX(scores.score) as max_score
        FROM scores
        JOIN users ON scores.user_id = users.id
        GROUP BY users.username
        ORDER BY max_score DESC
        LIMIT 10
    ''').fetchall()
    return render_template('highscores.html', scores=scores)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)