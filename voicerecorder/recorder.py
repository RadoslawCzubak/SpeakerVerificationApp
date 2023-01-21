import threading
from time import time_ns

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write

from voice_verification.utils.preprocessing import remove_silence, preprocess_audio

FS = 44100  # Sample rate
SECONDS = 60  # Duration of recording


def callback(indata, outdata, frames, time):
    print(indata)


class Recorder:

    def __init__(self, output_path: str):
        self.volume_listener = None
        self.stop_listener = None
        self.recording_stream = None
        self.recording = None
        self.output_path = output_path
        self.duration_time = None
        self.start_timestamp = None
        self.stop_timestamp = None
        self.max_limit_task = None

    def recording_callback(self, indata, outdata, frames, time):
        if self.recording is None:
            self.recording = indata
        else:
            self.recording = np.concatenate((self.recording, indata), axis=0)
        if self.volume_listener is not None:
            volume = np.linalg.norm(indata) * 10
            self.volume_listener(volume)

    def record_audio(self, seconds=5):
        def timeout_task():
            self.stop_recording()
            print("task ended")

        self.duration_time = seconds
        self.max_limit_task = threading.Timer(float(seconds), timeout_task)
        self.max_limit_task.start()
        print("task started")
        self.start_timestamp = time_ns()
        self.recording_stream = sd.InputStream(samplerate=FS, channels=1, callback=self.recording_callback)
        self.recording_stream.start()

    def stop_recording(self):
        if self.recording_stream is not None:
            self.recording_stream.stop()
            self.recording_stream.close()
            self.recording_stream = None
            self._save_recording()
            if self.max_limit_task is not None:
                self.max_limit_task.cancel()
            self.max_limit_task = None
            if self.stop_listener:
                self.stop_listener()

    def _save_recording(self):
        self.stop_timestamp = time_ns()
        if self.recording is not None:
            #recoding_duration_time_ms = self._get_recording_duration_time()
            #recording_sliced = self.recording[:][:int((FS / 1000) * recoding_duration_time_ms)]
            write(self.output_path, FS, np.array(self.recording))
            preprocess_audio(self.output_path)

    def _get_recording_duration_time(self):
        if self.stop_timestamp is not None:
            delta_time_ns = self.stop_timestamp - self.start_timestamp
            delta_time_ms = delta_time_ns / (10 ** 6)
            return delta_time_ms
        else:
            return self.duration_time

    def set_on_stop_listener(self, listener):
        self.stop_listener = listener

    def set_volume_listener(self, volume_listener):
        self.volume_listener = volume_listener
