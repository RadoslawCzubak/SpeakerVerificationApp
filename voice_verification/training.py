import model_maker as mm
from voice_verification.utils.files_reader import GetFiles


def train(speaker_name):
    '''
    :param
    speaker_name : name of the speaker whose model is to be prepared
                   Actually it takes the folder name of the speaker's audio files.
    '''
    print("Training " + speaker_name + "'s model")
    gf = GetFiles()  # getting the training files of speaker
    pandas_frame = gf.get_train_files(train_speaker_folder=speaker_name)  # audios path pipelined in dataframe
    mm.make_model(pandas_frame)
    print("Training finished.")
