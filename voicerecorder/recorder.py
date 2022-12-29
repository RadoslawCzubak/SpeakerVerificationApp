import threading
from time import time_ns

import sounddevice as sd
from scipy.io.wavfile import write

FS = 16000  # Sample rate
SECONDS = 60  # Duration of recording


class Recorder:

    def __init__(self, output_path: str):
        self.stop_listener = None
        self.recording = None
        self.output_path = output_path
        self.duration_time = None
        self.start_timestamp = None
        self.stop_timestamp = None
        self.max_limit_task = None

    def record_audio(self, seconds=5):
        def timeout_task():
            self.stop()
            print("task ended")

        self.duration_time = seconds
        self.max_limit_task = threading.Timer(float(seconds), timeout_task)
        self.max_limit_task.start()
        print("task started")
        self.start_timestamp = time_ns()
        self.recording = sd.rec(int(self.duration_time * FS), samplerate=FS, channels=1)

    def stop(self):
        sd.stop()
        self._save_recording()
        self.max_limit_task.cancel()
        self.max_limit_task = None
        if self.stop_listener:
            self.stop_listener()

    def _save_recording(self):
        self.stop_timestamp = time_ns()
        if self.recording is not None:
            recoding_duration_time_ms = self._get_recording_duration_time()
            recording_sliced = self.recording[:][:int((FS / 1000) * recoding_duration_time_ms)]
            write(self.output_path, FS, recording_sliced)

    def _get_recording_duration_time(self):
        if self.stop_timestamp is not None:
            delta_time_ns = self.stop_timestamp - self.start_timestamp
            delta_time_ms = delta_time_ns / (10 ** 6)
            return delta_time_ms
        else:
            return self.duration_time

    def set_on_stop_listener(self, listener):
        self.stop_listener = listener

    # class MaxTimeLimitTask(threading.Timer):
    #
    #     def __init__(self, sleep_duration: int, task):
    #         super().__init__()
    #         self.sleep_duration = sleep_duration
    #         self.task = task
    #
    #     def run(self, *args, **kwargs):
    #         print('Hello')
    #         sleep(self.sleep_duration)
    #         self.task()
    #         print("task done")
