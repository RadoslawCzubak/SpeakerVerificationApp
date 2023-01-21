import os

from PySide6 import QtCore
from PySide6.QtCore import Qt, Slot
from PySide6.QtCore import Signal
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QApplication, \
    QHBoxLayout, QProgressBar, QSizePolicy

from ResultDialog import ResultDialog
from constants import ROOT_DIR
from ui.RegisterDialog import RegisterDialog
from voice_verification.prediction import predict
from voicerecorder.recorder import Recorder


class MainWindow(QMainWindow):
    volumeSignal = Signal(float)
    stopRecorderSignal = Signal(bool)

    @Slot()
    def on_register_clicked(self):
        username = self.get_username_from_text()
        if len(username) > 1:
            if self.check_if_user_exists(username):
                dialog = ResultDialog("Niestety, istnieje użytkownik z taką nazwą.")
                dialog.exec()
            else:
                dlg = RegisterDialog(username)
                dlg.setWindowTitle("Registering!")
                dlg.exec()
        # na potrzeby testów
        # dlg = RegisterDialog()
        # dlg.setWindowTitle("Hello!")
        # dlg.exec()

    def __init__(self):
        super().__init__()

        # UI
        self.titleLabel = None
        self.usernameLabel = None
        self.usernameTextbox = None
        self.loginButton = None
        self.registerButton = None
        self.recording_info_layout = None
        self.recording_progress_bar = None
        self.recording_label = None
        self.recording_layout = None
        self.initUI()

        # Recorder
        self.recorder = None
        self.is_recording = False
        self.set_recorder_state(False)

        # Signals
        self.volumeSignal.connect(self.set_volume_widget)
        self.stopRecorderSignal.connect(self.on_recorder_stopped)

    def initUI(self):
        window = QWidget()

        # Set window properties
        window.setLayout(self.create_login_layout())
        self.setCentralWidget(window)
        self.resize(720, 480)
        self.setWindowTitle("Login Window")

    def create_login_layout(self):
        # Create widgets
        self.titleLabel = QLabel("Weryfikacja głosowa")
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleLabel.setStyleSheet("font-size: 24pt; font-weight: bold;")
        self.usernameLabel = QLabel("Nazwa użytkownika:")
        self.usernameLabel.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.usernameTextbox = QLineEdit()

        self.usernameTextbox.setText("")

        self.loginButton = QPushButton("Zaloguj się")
        self.loginButton.clicked.connect(self.on_login_clicked)

        self.registerButton = QPushButton("Utwórz konto")
        self.registerButton.clicked.connect(self.on_register_clicked)

        self.recording_info_layout = QHBoxLayout()
        self.recording_progress_bar = QProgressBar()
        self.recording_progress_bar.setRange(0, 100)
        self.recording_info_layout.addWidget(self.recording_progress_bar)

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addLayout(self.recording_info_layout)
        layout.addWidget(self.titleLabel)
        layout.addWidget(self.usernameLabel)
        layout.addWidget(self.usernameTextbox)
        layout.addWidget(self.loginButton)
        layout.addWidget(self.registerButton)
        self.setLayout(layout)

        # Add CSS styling
        self.setStyleSheet("""
                    QWidget {
                        background-color: #f0f0f0;
                        font-family: Arial;
                    }
                    QLabel {
                        color: #333;
                        font-size: 14px;
                    }
                    QLineEdit {
                        border: 1px solid #ccc;
                        padding: 8px;
                        font-size: 14px;
                    }
                    QPushButton {
                        background-color: #333;
                        color: #fff;
                        border: none;
                        padding: 8px;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background-color: #666;
                    }
                    
                    QPushButton:pressed {
                        background-color: #999;
                    }
                """)
        return layout

    def set_recorder_state(self, is_enabled: bool):
        if is_enabled:
            self.recording_progress_bar.show()
            self.loginButton.setText("Nagrywanie - Stop")
            self.loginButton.setStyleSheet("background-color: red; color: white;")
        else:
            self.recording_progress_bar.hide()
            self.loginButton.setText("Zaloguj się")
            self.loginButton.setStyleSheet("background-color: #333; color: white;")

    def set_volume_widget(self, volume):
        self.recording_progress_bar.setValue(volume)

    def on_volume(self, volume):
        self.volumeSignal.emit(volume)

    @Slot()
    def on_login_clicked(self):
        if self.recorder is None:
            username = self.get_username_from_text()
            if len(username) > 1:
                if self.check_if_user_exists(username):
                    self._start_record()
                else:
                    ResultDialog("Nie znaleziono użytkownika, podaj poprawną nazwę.").exec()

        else:
            self._stop_record()

    def get_username_from_text(self) -> str:
        username = self.usernameTextbox.text()
        username.strip()
        return username

    def _start_record(self):
        def on_recorder_stop_callback():
            self.stopRecorderSignal.emit(True)

        self.set_recorder_state(True)
        self.recorder = Recorder(output_path=f"{ROOT_DIR}/test.wav")
        self.recorder.record_audio()
        self.recorder.set_on_stop_listener(on_recorder_stop_callback)
        self.recorder.set_volume_listener(self.on_volume)

    def _stop_record(self):
        self.set_recorder_state(False)
        self.recorder.stop_recording()
        self.recorder = None

    def on_recorder_stopped(self, is_stopped):
        if is_stopped:
            self.set_recorder_state(False)
            self.recorder = None
            if predict(self.get_username_from_text()):
                dialog = ResultDialog("Tak, to ty!")
            else:
                dialog = ResultDialog("Nie rozpoznano użytkownika")
            dialog.exec()

    @staticmethod
    def check_if_user_exists(username):
        users = os.listdir("../user")
        return len([u for u in users if username == u]) > 0

    @staticmethod
    def clean_test_cache():
        if os.path.exists(f"{ROOT_DIR}/test.wav"):
            os.remove(f"{ROOT_DIR}/test.wav")


app = QApplication()
login_window = MainWindow()
login_window.show()
app.exec()
