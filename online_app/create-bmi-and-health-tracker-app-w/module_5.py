from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    bmi = db.Column(db.Float, nullable=False)
    health_status = db.Column(db.String(100), nullable=False)

    def __init__(self, name, email, bmi, health_status):
        self.name = name
        self.email = email
        self.bmi = bmi
        self.health_status = health_status

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.bmi}', '{self.health_status}')"

# Create the database tables
db.create_all()

# Seed the database with some data
users = [
    User('John Doe', 'john@example.com', 25.0, 'Normal'),
    User('Jane Doe', 'jane@example.com', 30.0, 'Overweight'),
    User('Bob Smith', 'bob@example.com', 20.0, 'Underweight'),
    User('Alice Johnson', 'alice@example.com', 28.0, 'Normal'),
    User('Mike Brown', 'mike@example.com', 32.0, 'Obese'),
]

db.session.add_all(users)
db.session.commit()