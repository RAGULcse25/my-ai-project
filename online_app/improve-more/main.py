```python
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users
    (id INTEGER PRIMARY KEY, username TEXT, password TEXT)
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS expenses
    (id INTEGER PRIMARY KEY, user_id INTEGER, category TEXT, amount REAL, date TEXT)
''')

class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.username_input = TextInput(multiline=False)
        self.password_input = TextInput(password=True, multiline=False)
        self.add_widget(Label(text='Username:'))
        self.add_widget(self.username_input)
        self.add_widget(Label(text='Password:'))
        self.add_widget(self.password_input)
        self.add_widget(Button(text='Login', on_press=self.login))
        self.add_widget(Button(text='Register', on_press=self.register))

    def login(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        if user:
            self.clear_widgets()
            self.add_widget(ExpenseTrackerScreen())
        else:
            popup = Popup(title='Error', content=Label(text='Invalid username or password'), size_hint=(None, None), size=(200, 100))
            popup.open()

    def register(self, instance):
        self.clear_widgets()
        self.add_widget(RegisterScreen())

class RegisterScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.username_input = TextInput(multiline=False)
        self.password_input = TextInput(password=True, multiline=False)
        self.add_widget(Label(text='Username:'))
        self.add_widget(self.username_input)
        self.add_widget(Label(text='Password:'))
        self.add_widget(self.password_input)
        self.add_widget(Button(text='Register', on_press=self.register))
        self.add_widget(Button(text='Back', on_press=self.back))

    def register(self, instance):
        username = self.username_input.text
        password = self.password_input.text
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        self.clear_widgets()
        self.add_widget(LoginScreen())

    def back(self, instance):
        self.clear_widgets()
        self.add_widget(LoginScreen())

class ExpenseTrackerScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(ExpenseTrackerScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.category_spinner = Spinner(text='Food', values=['Food', 'Transportation', 'Entertainment'])
        self.amount_input = TextInput(multiline=False)
        self.add_widget(Label(text='Category:'))
        self.add_widget(self.category_spinner)
        self.add_widget(Label(text='Amount:'))
        self.add_widget(self.amount_input)
        self.add_widget(Button(text='Add Expense', on_press=self.add_expense))
        self.add_widget(Button(text='View Expenses', on_press=self.view_expenses))

    def add_expense(self, instance):
        category = self.category_spinner.text
        amount = float(self.amount_input.text)
        cursor.execute('INSERT INTO expenses (user_id, category, amount, date) VALUES (1, ?, ?, ?)', (category, amount, '2024-09-16'))
        conn.commit()
        popup = Popup(title='Success', content=Label(text='Expense added successfully'), size_hint=(None, None), size=(200, 100))
        popup.open()

    def view_expenses(self, instance):
        cursor.execute('SELECT * FROM expenses')
        expenses = cursor.fetchall()
        popup = Popup(title='Expenses', content=Label(text=str(expenses)), size_hint=(None, None), size=(400, 400))
        popup.open()

class ExpenseTrackerApp(App):
    def build(self):
        return LoginScreen()

if __name__ == '__main__':
    ExpenseTrackerApp().run()
```

####