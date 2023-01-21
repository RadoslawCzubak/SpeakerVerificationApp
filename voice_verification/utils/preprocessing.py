from pydub import AudioSegment, silence, effects


def remove_silence(file_path: str):
    audio = AudioSegment.from_file(file_path, format="wav")
    non_silence_moments = silence.detect_nonsilent(audio, 150, silence_thresh=-32)
    audio_without_silence = AudioSegment.empty()
    print(non_silence_moments)
    for non_silence_start, non_silence_stop in non_silence_moments:
        audio_without_silence += audio[non_silence_start: non_silence_stop]
    audio_without_silence.export(file_path, format="wav")


def normalize_audio(file_path: str):
    raw_sound = AudioSegment.from_file(file_path, format="wav")
    normalized_sound = effects.normalize(raw_sound)
    normalized_sound.export(file_path, format="wav")


def preprocess_audio(file_path: str):
    normalize_audio(file_path)
    remove_silence(file_path)


if __name__ == '__main__':
    remove_silence("/Users/radoslav/Desktop/train0.wav")
    # normalize_audio("/Users/radoslav/Desktop/test_high.wav")


