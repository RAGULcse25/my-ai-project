from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class CalculatorApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.display = TextInput(font_size=32, readonly=True, halign='right', multiline=False)
        layout.add_widget(self.display)
        
        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['C', '0', '=', '+']
        ]
        
        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                btn = Button(text=label, pos_hint={'center_x': 0.5, 'center_y': 0.5})
                btn.bind(on_press=self.on_button_press)
                h_layout.add_widget(btn)
            layout.add_widget(h_layout)
        return layout

    def on_button_press(self, instance):
        if instance.text == 'C':
            self.display.text = ''
        elif instance.text == '=':
            try:
                self.display.text = str(eval(self.display.text))
            except:
                self.display.text = 'Error'
        else:
            self.display.text += instance.text

if __name__ == '__main__':
    CalculatorApp().run()
