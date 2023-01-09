import os
import shutil

from PySide6.QtCore import Qt, Slot, Signal
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QCheckBox, QPushButton, QProgressBar

from constants import ROOT_DIR
from voice_verification.training import train
from voicerecorder.recorder import Recorder


class RegisterDialog(QDialog):
    volumeSignal = Signal(float)

    def __init__(self, username):
        super().__init__()
        self.closeEvent()
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
        self.recording_info_layout = None
        self.recording_progress_bar = None
        self.recording_label = None
        self.recording_layout = None

        self.setWindowTitle("Nagraj próbki")
        self.init_UI()

        # Signals
        self.volumeSignal.connect(self.set_volume_widget)

    def closeEvent(self, event=None):
        if event is not None:
            self.on_negative_clicked()
            event.accept()

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
        self.negative_btn.clicked.connect(self.on_negative_clicked)
        self.positive_btn.clicked.connect(self.on_record_clicked)
        self.positive_btn.setDefault(True)
        # self.negative_btn.setStyleSheet("background-color: red; color: white;")

        self.layout = QVBoxLayout()
        message = QLabel("Nagraj próbki swojego głosu:\n"
                         "Powtórz 5 razy wybrane hasło!")

        checkbox_layout = QHBoxLayout()
        for checkbox in self.checkboxes:
            checkbox_layout.addWidget(checkbox)

        self.recording_info_layout = QHBoxLayout()
        self.recording_progress_bar = QProgressBar()
        self.recording_progress_bar.setRange(0, 100)
        self.recording_info_layout.addWidget(self.recording_progress_bar)

        self.layout.addLayout(self.recording_info_layout)
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
            self.recording_progress_bar.show()
            # pb.setStyleSheet("background-color: red; color: white;")
            pb.setStyleSheet("QPushButton { background-color: #ff2929; color: white; border: none; border-radius: 5px; "
                             " padding-top: 2px; padding-bottom: 4px;}"
                             "QPushButton:hover { background-color: #d62424 } "
                             "QPushButton:pressed { background-color: #a31c1c }")
            pb.setText("Stop")
        else:
            self.recording_progress_bar.hide()
            # pb.setStyleSheet("background-color: blue; color: white;")
            pb.setStyleSheet("QPushButton { background-color: #5DADE2; color: white; border: none; border-radius: 5px; "
                             " padding-top: 2px; padding-bottom: 4px;}"
                             "QPushButton:hover { background-color: #3498DB } "
                             "QPushButton:pressed { background-color: #2E86C1 }")
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

        def on_volume_changed_callback(volume):
            self.volumeSignal.emit(volume)

        self.recorder.set_volume_listener(on_volume_changed_callback)

    def _stop_record(self):
        self.set_recorder_state(False)
        self.recorder.stop_recording()
        self.recorder = None

    def is_all_recorded(self):
        return self.recording_num >= 5

    def set_volume_widget(self, volume):
        self.recording_progress_bar.setValue(volume)

    def remove_cached_files(self):
        if os.path.exists(f"{ROOT_DIR}/user/{self.username}"):
            shutil.rmtree(f"{ROOT_DIR}/user/{self.username}")

    @Slot()
    def on_negative_clicked(self):
        self.remove_cached_files()
        self.reject()
