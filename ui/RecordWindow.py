from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

from voicerecorder.recorder import Recorder


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
        self.recorder = None
        self.is_recording = False
        self.set_recorder_state(False)

    @Slot()
    def record_audio(self):
        if self.recorder is None:
            self._start_record()
        else:
            self._stop_record()

    def _start_record(self):
        def on_recorder_stop():
            self.set_recorder_state(False)
            self.recorder = None

        self.set_recorder_state(True)
        self.recorder = Recorder(output_path="test.wav")
        self.recorder.record_audio()
        self.recorder.set_on_stop_listener(on_recorder_stop)

    def _stop_record(self):
        self.set_recorder_state(False)
        self.recorder.stop()
        self.recorder = None

    def set_recorder_state(self, is_enabled: bool):
        if is_enabled:
            self.record_button.setText("Stop")
        else:
            self.record_button.setText("Record")
