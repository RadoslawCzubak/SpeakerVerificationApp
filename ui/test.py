import sys
from PySide6.QtWidgets import (QApplication, QWidget, QCheckBox, QHBoxLayout, 
                               QVBoxLayout, QLabel, QLineEdit, QPushButton)


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create the label and textbox for the user name
        username_label = QLabel("Nazwa użytkownika")
        self.username_textbox = QLineEdit()

        # Create the checkboxes
        self.checkbox_1 = QCheckBox("Checkbox 1")
        self.checkbox_2 = QCheckBox("Checkbox 2")
        self.checkbox_3 = QCheckBox("Checkbox 3")
        self.checkbox_4 = QCheckBox("Checkbox 4")
        self.checkbox_5 = QCheckBox("Checkbox 5")

        # Create the button
        self.button = QPushButton("Nagraj")

        # Create the layouts
        username_layout = QHBoxLayout()
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_textbox)

        checkbox_layout = QHBoxLayout()
        checkbox_layout.addWidget(self.checkbox_1)
        checkbox_layout.addWidget(self.checkbox_2)
        checkbox_layout.addWidget(self.checkbox_3)
        checkbox_layout.addWidget(self.checkbox_4)
        checkbox_layout.addWidget(self.checkbox_5)

        main_layout = QVBoxLayout()
        main_layout.addLayout(username_layout)
        main_layout.addLayout(checkbox_layout)
        main_layout.addWidget(self.button)

        self.setLayout(main_layout)

        self.setStyleSheet("""
    QWidget {
        background-color: #222;
        color: #e50914;
        font-family: "Arial", sans-serif;
    }
    QLabel {
        font-size: 18px;
    }
    QTextEdit {
        font-size: 16px;
        border: 1px solid #e50914;
        border-radius: 5px;
        padding: 8px;
        color: #e50914;
    }
    QCheckBox {
        font-size: 16px;
        color: #e50914;
    }
    QPushButton {
        background-color: #e50914;
        color: white;
        font-size: 16px;
        border: none;
        border-radius: 5px;
        padding: 10px;
    }
    QPushButton:hover {
        background-color: #c40812;
    }
    """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec())
