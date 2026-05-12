from app import db

class ChessGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1 = db.Column(db.String(100), nullable=False)
    player2 = db.Column(db.String(100), nullable=False)
    result = db.Column(db.String(100), nullable=False)

    def __init__(self, player1, player2, result):
        self.player1 = player1
        self.player2 = player2
        self.result = result

    def __repr__(self):
        return f'ChessGame({self.player1}, {self.player2}, {self.result})'

# Create the database tables
with app.app_context():
    db.create_all()

# Seed the database with some data
games = [
    ChessGame('Player 1', 'Player 2', 'Result 1'),
    ChessGame('Player 3', 'Player 4', 'Result 2'),
    ChessGame('Player 5', 'Player 6', 'Result 3'),
    ChessGame('Player 7', 'Player 8', 'Result 4'),
    ChessGame('Player 9', 'Player 10', 'Result 5'),
]

with app.app_context():
    db.session.add_all(games)
    db.session.commit()