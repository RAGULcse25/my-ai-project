from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import math

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calculator.db'
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Calculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    calculation = db.Column(db.String(200), nullable=False)
    result = db.Column(db.String(200), nullable=False)

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

class CalculatorForm(FlaskForm):
    calculation = StringField('Calculation', validators=[InputRequired()])
    submit = SubmitField('Calculate')

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
            return redirect(url_for('calculator'))
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

@app.route('/calculator', methods=['GET', 'POST'])
@login_required
def calculator():
    form = CalculatorForm()
    if form.validate_on_submit():
        calculation = form.calculation.data
        try:
            result = eval(calculation)
            new_calculation = Calculation(user_id=current_user.id, calculation=calculation, result=str(result))
            db.session.add(new_calculation)
            db.session.commit()
        except Exception as e:
            flash(str(e), 'error')
        return redirect(url_for('history'))
    return render_template('calculator.html', form=form)

@app.route('/history')
@login_required
def history():
    calculations = Calculation.query.filter_by(user_id=current_user.id).all()
    return render_template('history.html', calculations=calculations)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/advanced_calculator')
@login_required
def advanced_calculator():
    return render_template('advanced_calculator.html')

@app.route('/advanced_calculator/calculate', methods=['POST'])
@login_required
def advanced_calculate():
    calculation = request.form['calculation']
    try:
        result = eval(calculation)
        new_calculation = Calculation(user_id=current_user.id, calculation=calculation, result=str(result))
        db.session.add(new_calculation)
        db.session.commit()
    except Exception as e:
        flash(str(e), 'error')
    return redirect(url_for('history'))

@app.route('/trigonometry')
@login_required
def trigonometry():
    return render_template('trigonometry.html')

@app.route('/trigonometry/calculate', methods=['POST'])
@login_required
def trigonometry_calculate():
    angle = float(request.form['angle'])
    operation = request.form['operation']
    if operation == 'sin':
        result = math.sin(math.radians(angle))
    elif operation == 'cos':
        result = math.cos(math.radians(angle))
    elif operation == 'tan':
        result = math.tan(math.radians(angle))
    new_calculation = Calculation(user_id=current_user.id, calculation=f'{operation}({angle})', result=str(result))
    db.session.add(new_calculation)
    db.session.commit()
    return redirect(url_for('history'))

@app.route('/exponentiation')
@login_required
def exponentiation():
    return render_template('exponentiation.html')

@app.route('/exponentiation/calculate', methods=['POST'])
@login_required
def exponentiation_calculate():
    base = float(request.form['base'])
    exponent = float(request.form['exponent'])
    result = base ** exponent
    new_calculation = Calculation(user_id=current_user.id, calculation=f'{base}^{exponent}', result=str(result))
    db.session.add(new_calculation)
    db.session.commit()
    return redirect(url_for('history'))

@app.route('/logarithm')
@login_required
def logarithm():
    return render_template('logarithm.html')

@app.route('/logarithm/calculate', methods=['POST'])
@login_required
def logarithm_calculate():
    number = float(request.form['number'])
    base = float(request.form['base'])
    result = math.log(number, base)
    new_calculation = Calculation(user_id=current_user.id, calculation=f'log_{base}({number})', result=str(result))
    db.session.add(new_calculation)
    db.session.commit()
    return redirect(url_for('history'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)