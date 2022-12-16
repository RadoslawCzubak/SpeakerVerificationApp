from scipy.io.wavfile import write
import sounddevice as sd
FS = 16000  # Sample rate
SECONDS = 5  # Duration of recording


def record_audio(output_path: str, seconds):
    recording = sd.rec(int(seconds * FS), samplerate=FS, channels=1)
    sd.wait()  # Wait until recording is finished
    write(output_path, FS, recording)  # Save as WAV file
