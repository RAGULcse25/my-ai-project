from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chess.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class ChessGame(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1 = db.Column(db.String(100), nullable=False)
    player2 = db.Column(db.String(100), nullable=False)
    result = db.Column(db.String(100), nullable=False)

    def __init__(self, player1, player2, result):
        self.player1 = player1
        self.player2 = player2
        self.result = result

class ChessGameSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ChessGame

class ChessForm(FlaskForm):
    player1 = StringField('Player 1', validators=[DataRequired()])
    player2 = StringField('Player 2', validators=[DataRequired()])
    result = StringField('Result', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/games', methods=['GET'])
def get_games():
    games = ChessGame.query.all()
    schema = ChessGameSchema(many=True)
    return jsonify(schema.dump(games))

@app.route('/games', methods=['POST'])
def create_game():
    form = ChessForm()
    if form.validate_on_submit():
        game = ChessGame(form.player1.data, form.player2.data, form.result.data)
        db.session.add(game)
        db.session.commit()
        return jsonify({'message': 'Game created successfully'}), 201
    return jsonify({'message': 'Invalid form data'}), 400

@app.route('/games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    game = ChessGame.query.get(game_id)
    if game:
        schema = ChessGameSchema()
        return jsonify(schema.dump(game))
    return jsonify({'message': 'Game not found'}), 404

@app.route('/games/<int:game_id>', methods=['PUT'])
def update_game(game_id):
    game = ChessGame.query.get(game_id)
    if game:
        form = ChessForm()
        if form.validate_on_submit():
            game.player1 = form.player1.data
            game.player2 = form.player2.data
            game.result = form.result.data
            db.session.commit()
            return jsonify({'message': 'Game updated successfully'}), 200
        return jsonify({'message': 'Invalid form data'}), 400
    return jsonify({'message': 'Game not found'}), 404

@app.route('/games/<int:game_id>', methods=['DELETE'])
def delete_game(game_id):
    game = ChessGame.query.get(game_id)
    if game:
        db.session.delete(game)
        db.session.commit()
        return jsonify({'message': 'Game deleted successfully'}), 200
    return jsonify({'message': 'Game not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)