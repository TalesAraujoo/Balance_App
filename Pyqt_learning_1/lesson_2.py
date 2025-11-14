from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit
import sys


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.count = 0

        self.setWindowTitle("Lesson 2 - UI Basics")


        #Create widgets
        self.label = QLabel("Hello! Click the button")
        self.label_count = QLabel(f'Cliked {self.count} time(s)')
        self.button = QPushButton("Click me")
        self.reset_button = QPushButton("Reset")
        self.label_input = QLineEdit()
        self.set_text_button = QPushButton("Set Text")

        #Connect button signal to function
        self.button.clicked.connect(self.button_clicked)
        self.reset_button.clicked.connect(self.reset_button_clicked)
        self.set_text_button.clicked.connect(self.set_text_button_clicked)

        #create layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.label_count)
        layout.addWidget(self.button)
        layout.addWidget(self.reset_button)
        layout.addWidget(self.label_input)
        layout.addWidget(self.set_text_button)

        self.setLayout(layout)


    def set_text_button_clicked(self):
        self.label.setText(f'{self.label_input.text()}')
        self.label_input.clear()
    
    def button_clicked(self):
        self.count += 1
        self.label.setText("Button clicked!")
        self.label_count.setText(f'Clicked {self.count} time(s)')
    
    def reset_button_clicked(self):
        self.count = 0
        self.label.setText("Hello! Click the button")
        self.label_count.setText(f"Clicked {self.count} time(s)")


app = QApplication(sys.argv)
window = MyApp()
window.show()
app.exec()