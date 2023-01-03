import sys

from PySide6 import QtWidgets

# Create a Qt application
app = QtWidgets.QApplication(sys.argv)

# Create the main window
window = QtWidgets.QWidget()

# Set the window title
window.setWindowTitle("Login and Register Form")

# Set the window size
window.setMinimumSize(400, 300)

# Create the login and register forms as stacked widgets
login_form = QtWidgets.QWidget()
register_form = QtWidgets.QWidget()

# Create the form layout for the login form
login_form_layout = QtWidgets.QFormLayout()

# Create the form layout for the register form
register_form_layout = QtWidgets.QFormLayout()

# Add the email, password, and login button to the login form
email_input = QtWidgets.QLineEdit()
password_input = QtWidgets.QLineEdit()
password_input.setEchoMode(QtWidgets.QLineEdit.Password)
login_button = QtWidgets.QPushButton("Login")

# Add stretchable spacers to the login form layout
login_form_layout.addRow(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
login_form_layout.addRow("Email:", email_input)
login_form_layout.addRow("Password:", password_input)
login_form_layout.addRow(login_button)
login_form_layout.addRow(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

# Add the name, email, password, and register button to the register form
name_input = QtWidgets.QLineEdit()
email_input = QtWidgets.QLineEdit()
password_input = QtWidgets.QLineEdit()
password_input.setEchoMode(QtWidgets.QLineEdit.Password)
register_button = QtWidgets.QPushButton("Register")

# Add stretchable spacers to the register form layout
register_form_layout.addRow(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
register_form_layout.addRow("Name:", name_input)
register_form_layout.addRow("Email:", email_input)
register_form_layout.addRow("Password:", password_input)
register_form_layout.addRow(register_button)
register_form_layout.addRow(QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))

# Set the layout for the login form
login_form.setLayout(login_form_layout)

# Set the layout for the register form
register_form.setLayout(register_form_layout)

# Create the tab widget and add the login and register forms as tabs
tabs = QtWidgets.QTabWidget()
tabs.addTab(login_form, "Login")
tabs.addTab(register_form, "Register")

# Create the main layout and add the tab widget
main_layout = QtWidgets.QVBoxLayout()
main_layout.addWidget(tabs)

# Set the main layout for the window
window.setLayout(main_layout)

# Set the style sheet for the application
css = """
    QWidget {
        background-color: #36393f;
        color: white;
    }
    QLineEdit {
        background-color: #2f3136;
        border: 1px solid #4f545c;
        padding: 5px;
        border-radius: 3px;
    }
    QPushButton {
        background-color: #7289da;
        color: white;
        border: none;
        padding: 5px 10px;
        border-radius: 3px;
    }
    QPushButton:hover {
        background-color: #5b6268;
    }
    QTabBar::tab {
        background-color: #2f3136;
        color: #8a8a
        border: 1px solid #4f545c;
        border-bottom: none;
        padding: 5px 10px;
        border-radius: 3px 3px 0 0;
    }
    QTabBar::tab:selected {
        background-color: #36393f;
        color: white;
    }
    QTabBar::tab:hover {
        background-color: #23272a;
    }"""
app.setStyleSheet(css)
# Show the window
window.show()
app.exec()
