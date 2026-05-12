from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chess.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1 = db.Column(db.String(80), nullable=False)
    player2 = db.Column(db.String(80), nullable=False)
    moves = db.Column(db.String(200), nullable=False)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('Email', validators=[InputRequired(), Email(), Length(min=4, max=50)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class CreateGameForm(FlaskForm):
    player1 = StringField('Player 1', validators=[InputRequired(), Length(min=4, max=15)])
    player2 = StringField('Player 2', validators=[InputRequired(), Length(min=4, max=15)])
    submit = SubmitField('Create Game')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=generate_password_hash(form.password.data))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    games = Game.query.all()
    return render_template('dashboard.html', games=games)

@app.route('/create_game', methods=['GET', 'POST'])
@login_required
def create_game():
    form = CreateGameForm()
    if form.validate_on_submit():
        new_game = Game(player1=form.player1.data, player2=form.player2.data, moves='')
        db.session.add(new_game)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('create_game.html', form=form)

@app.route('/game/<int:game_id>')
@login_required
def game(game_id):
    game = Game.query.get(game_id)
    return render_template('game.html', game=game)

@app.route('/make_move/<int:game_id>', methods=['POST'])
@login_required
def make_move(game_id):
    game = Game.query.get(game_id)
    move = request.form['move']
    game.moves += move + ','
    db.session.commit()
    return redirect(url_for('game', game_id=game_id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # seed data
        user1 = User(username='user1', email='user1@example.com', password=generate_password_hash('password1'))
        user2 = User(username='user2', email='user2@example.com', password=generate_password_hash('password2'))
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
    app.run(debug=True)