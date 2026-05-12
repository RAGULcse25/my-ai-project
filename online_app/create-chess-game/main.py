```python
import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.properties import StringProperty
from kivy.clock import Clock
import sqlite3
import random

# Initialize the database connection
conn = sqlite3.connect('chess_game.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS game_history
             (id INTEGER PRIMARY KEY AUTOINCREMENT, game_date TEXT, result TEXT)''')
conn.commit()

class ChessGame(GridLayout):
    def __init__(self, **kwargs):
        super(ChessGame, self).__init__(**kwargs)
        self.cols = 1
        self.rows = 2

        # Create the game board
        self.board = GridLayout()
        self.board.cols = 8
        self.board.rows = 8
        self.board.size_hint = (1, 0.8)
        self.add_widget(self.board)

        # Create the pieces
        self.pieces = []
        for i in range(8):
            for j in range(8):
                piece = Button(text='', font_size=20)
                piece.bind(on_press=self.on_piece_press)
                self.board.add_widget(piece)
                self.pieces.append(piece)

        # Create the move history
        self.move_history = ScrollView(size_hint=(1, 0.2))
        self.move_history_layout = StackLayout()
        self.move_history.add_widget(self.move_history_layout)
        self.add_widget(self.move_history)

        # Initialize the game state
        self.current_turn = 'white'
        self.selected_piece = None
        self.possible_moves = []
        self.game_over = False

        # Initialize the pieces
        self.initialize_pieces()

    def initialize_pieces(self):
        # Initialize the pieces
        for i in range(8):
            for j in range(8):
                if i == 1:
                    self.pieces[i*8 + j].text = 'P'
                elif i == 6:
                    self.pieces[i*8 + j].text = 'p'
                elif i == 0:
                    if j in [0, 7]:
                        self.pieces[i*8 + j].text = 'R'
                    elif j in [1, 6]:
                        self.pieces[i*8 + j].text = 'N'
                    elif j in [2, 5]:
                        self.pieces[i*8 + j].text = 'B'
                    elif j == 3:
                        self.pieces[i*8 + j].text = 'Q'
                    elif j == 4:
                        self.pieces[i*8 + j].text = 'K'
                elif i == 7:
                    if j in [0, 7]:
                        self.pieces[i*8 + j].text = 'r'
                    elif j in [1, 6]:
                        self.pieces[i*8 + j].text = 'n'
                    elif j in [2, 5]:
                        self.pieces[i*8 + j].text = 'b'
                    elif j == 3:
                        self.pieces[i*8 + j].text = 'q'
                    elif j == 4:
                        self.pieces[i*8 + j].text = 'k'

    def on_piece_press(self, instance):
        if self.game_over:
            return

        # Get the piece's position
        position = self.pieces.index(instance)

        # Check if the piece is the current player's
        if self.current_turn == 'white' and instance.text.islower():
            return
        elif self.current_turn == 'black' and instance.text.isupper():
            return

        # Check if a piece is already selected
        if self.selected_piece:
            # Move the piece
            self.move_piece(self.selected_piece, position)
            self.selected_piece = None
            self.possible_moves = []
        else:
            # Select the piece
            self.selected_piece = position
            self.possible_moves = self.get_possible_moves(position)

            # Highlight the possible moves
            for move in self.possible_moves:
                self.pieces[move].background_color = (0, 1, 0, 1)

    def get_possible_moves(self, position):
        # Get the piece's type
        piece_type = self.pieces[position].text.lower()

        # Get the piece's position
        x = position % 8
        y = position // 8

        # Get the possible moves
        possible_moves = []
        if piece_type == 'p':
            # Pawn
            if self.current_turn == 'white':
                if y < 7 and self.pieces[(y+1)*8 + x].text == '':
                    possible_moves.append((y+1)*8 + x)
                if y < 6 and self.pieces[(y+1)*8 + x].text == '' and self.pieces[(y+2)*8 + x].text == '':
                    possible_moves.append((y+2)*8 + x)
                if x > 0 and y < 7 and self.pieces[(y+1)*8 + x-1].text != '' and self.pieces[(y+1)*8 + x-1].text.islower():
                    possible_moves.append((y+1)*8 + x-1)
                if x < 7 and y < 7 and self.pieces[(y+1)*8 + x+1].text != '' and self.pieces[(y+1)*8 + x+1].text.islower():
                    possible_moves.append((y+1)*8 + x+1)
            else:
                if y > 0 and self.pieces[(y-1)*8 + x].text == '':
                    possible_moves.append((y-1)*8 + x)
                if y > 1 and self.pieces[(y-1)*8 + x].text == '' and self.pieces[(y-2)*8 + x].text == '':
                    possible_moves.append((y-2)*8 + x)
                if x > 0 and y > 0 and self.pieces[(y-1)*8 + x-1].text != '' and self.pieces[(y-1)*8 + x-1].text.isupper():
                    possible_moves.append((y-1)*8 + x-1)
                if x < 7 and y > 0 and self.pieces[(y-1)*8 + x+1].text != '' and self.pieces[(y-1)*8 + x+1].text.isupper():
                    possible_moves.append((y-1)*8 + x+1)
        elif piece_type == 'n':
            # Knight
            for dx, dy in [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]:
                nx, ny = x + dx, y + dy
                if nx >= 0 and nx < 8 and ny >= 0 and ny < 8:
                    if self.pieces[ny*8 + nx].text == '':
                        possible_moves.append(ny*8 + nx)
                    elif self.pieces[ny*8 + nx].text.islower() != self.pieces[position].text.islower():
                        possible_moves.append(ny*8 + nx)
        elif piece_type == 'b':
            # Bishop
            for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                nx, ny = x + dx, y + dy
                while nx >= 0 and nx < 8 and ny >= 0 and ny < 8:
                    if self.pieces[ny*8 + nx].text == '':
                        possible_moves.append(ny*8 + nx)
                        nx += dx
                        ny += dy
                    elif self.pieces[ny*8 + nx].text.islower() != self.pieces[position].text.islower():
                        possible_moves.append(ny*8 + nx)
                        break
                    else:
                        break
        elif piece_type == 'r':
            # Rook
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                while nx >= 0 and nx < 8 and ny >= 0 and ny < 8:
                    if self.pieces[ny*8 + nx].text == '':
                        possible_moves.append(ny*8 + nx)
                        nx += dx
                        ny += dy
                    elif self.pieces[ny*8 + nx].text.islower() != self.pieces[position].text.islower():
                        possible_moves.append(ny*8 + nx)
                        break
                    else:
                        break
        elif piece_type == 'q':
            # Queen
            for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                while nx >= 0 and nx < 8 and ny >= 0 and ny < 8:
                    if self.pieces[ny*8 + nx].text == '':
                        possible_moves.append(ny*8 + nx)
                        nx += dx
                        ny += dy
                    elif self.pieces[ny*8 + nx].text.islower() != self.pieces[position].text.islower():
                        possible_moves.append(ny*8 + nx)
                        break
                    else:
                        break
        elif piece_type == 'k':
            # King
            for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if nx >= 0 and nx < 8 and ny >= 0 and ny < 8:
                    if self.pieces[ny*8 + nx].text == '':
                        possible_moves.append(ny*8 + nx)
                    elif self.pieces[ny*8 + nx].text.islower() != self.pieces[position].text.islower():
                        possible_moves.append(ny*8 + nx)

        return possible_moves

    def move_piece(self, from_position, to_position):
        # Move the piece
        self.pieces[to_position].text = self.pieces[from_position].text
        self.pieces[from_position].text = ''

        # Update the game state
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'

        # Check for checkmate
        if self.is_checkmate():
            self.game_over = True
            self.show_game_over_popup()

        # Add the move to the move history
        self.move_history_layout.add_widget(Label(text=f'{self.pieces[to_position].text} moved from {from_position} to {to_position}'))

    def is_checkmate(self):
        # Check if the king is in check
        king_position = None
        for i in range(64):
            if self.pieces[i].text.lower() == 'k':
                king_position = i
                break

        if king_position is None:
            return True

        # Check if any pieces can move to the king's position
        for i in range(64):
            if self.pieces[i].text != '' and self.pieces[i].text.islower() != self.pieces[king_position].text.islower():
                possible_moves = self.get_possible_moves(i)
                if king_position in possible_moves:
                    return True

        return False

    def show_game_over_popup(self):
        popup = Popup(title='Game Over', content=Label(text='Checkmate!'), size_hint=(None, None), size=(200, 100))
        popup.open()

class ChessApp(App):
    def build(self):
        return ChessGame()

if __name__ == '__main__':
    ChessApp().run()
```

#### =