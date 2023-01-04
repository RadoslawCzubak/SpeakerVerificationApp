import os

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QCheckBox, QPushButton

from constants import ROOT_DIR
from voice_verification.training import train
from voicerecorder.recorder import Recorder


class RegisterDialog(QDialog):
    def __init__(self, username):
        super().__init__()

        self.username = username

        # Checkboxes
        self.checkbox_1 = None
        self.checkbox_2 = None
        self.checkbox_3 = None
        self.checkbox_4 = None
        self.checkbox_5 = None
        self.checkboxes = []

        # Recorder
        self.recorder = None
        self.is_recording = False
        self.recording_num = 0

        # UI
        self.setWindowTitle("Nagraj próbki")
        self.init_UI()

    def init_UI(self):

        # Create the checkboxes
        self.checkbox_1 = QCheckBox("Próbka 1")
        self.checkbox_2 = QCheckBox("Próbka 2")
        self.checkbox_3 = QCheckBox("Próbka 3")
        self.checkbox_4 = QCheckBox("Próbka 4")
        self.checkbox_5 = QCheckBox("Próbka 5")
        self.checkboxes = [self.checkbox_1, self.checkbox_2, self.checkbox_3, self.checkbox_4, self.checkbox_5]
        for checkbox in self.checkboxes:
            checkbox.setAttribute(Qt.WA_TransparentForMouseEvents)
            # checkbox.setChecked(True)

        self.buttonBox = QHBoxLayout()
        self.positive_btn = QPushButton("Positive - Nagraj")
        self.negative_btn = QPushButton("Negative")
        self.buttonBox.addWidget(self.negative_btn)
        self.buttonBox.addWidget(self.positive_btn)
        self.negative_btn.clicked.connect(self.reject)
        self.positive_btn.clicked.connect(self.on_record_clicked)
        self.positive_btn.setDefault(True)
        # self.negative_btn.setStyleSheet("background-color: red; color: white;")

        self.layout = QVBoxLayout()
        message = QLabel("Nagraj próbki swojego głosu:\n"
                         "Powtórz 5 razy wybrane hasło!")

        checkbox_layout = QHBoxLayout()
        for checkbox in self.checkboxes:
            checkbox_layout.addWidget(checkbox)

        self.layout.addWidget(message)
        self.layout.addLayout(checkbox_layout)
        self.layout.addLayout(self.buttonBox)
        self.setLayout(self.layout)
        self.set_recorder_state(False)

    @Slot()
    def on_record_clicked(self):
        if self.recorder is None and not self.is_all_recorded():
            self._start_record()
        elif self.recorder is None:
            train(speaker_name=self.username)
            self.accept()
        else:
            self.recording_num += 1
            self._stop_record()

    def set_recorder_state(self, is_recording):
        self.update_ui()
        pb = self.positive_btn
        if is_recording:
            pb.setStyleSheet("background-color: red; color: white;")
            pb.setText("Stop")
        else:
            pb.setStyleSheet("background-color: blue; color: white;")
            pb.setText("Nagraj")
            if self.is_all_recorded():
                pb.setText("Dodaj użytkownika")

    def update_ui(self):
        for idx, checkbox in enumerate(self.checkboxes):
            if idx < self.recording_num:
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)

    def _start_record(self):
        def on_recorder_stop():
            self.set_recorder_state(False)
            self.recorder = None

        self.set_recorder_state(True)
        if not os.path.exists(f"{ROOT_DIR}/user/{self.username}/training"):
            os.makedirs(f"{ROOT_DIR}/user/{self.username}/training/")
        self.recorder = Recorder(output_path=f"{ROOT_DIR}/user/{self.username}/training/train{self.recording_num}.wav")
        self.recorder.record_audio()
        self.recorder.set_on_stop_listener(on_recorder_stop)
        # self.recorder.set_volume_listener(self.on_volume)

    def _stop_record(self):
        self.set_recorder_state(False)
        self.recorder.stop_recording()
        self.recorder = None

    def is_all_recorded(self):
        return self.recording_num >= 5
