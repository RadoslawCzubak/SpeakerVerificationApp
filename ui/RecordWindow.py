from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtWidgets import QMainWindow
from voicerecorder import recorder

class RecordWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        window = QWidget()
        self.record_button = QPushButton("Record")
        self.record_button.clicked.connect(self.record_audio)
        layout.addWidget(self.record_button)
        window.setLayout(layout)
        self.setCentralWidget(window)

    @Slot()
    def record_audio(self):
        recorder.record_audio("test.wav", seconds=5)