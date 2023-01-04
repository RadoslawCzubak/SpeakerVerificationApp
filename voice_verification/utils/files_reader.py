'''
working criteria is as:
Three modules to be build:
    one for loading the training dataset
    another for loading testing dataset
    another for loading dataset for  accuracy testing
'''

import os

import pandas as pd

from constants import ROOT_DIR

'''
Actually the dataset to be tested is placed inside the test_dataset folder 
and dataset to be trained is placed inside the train_dataset

And dataset to be predicted is placed inside the predict_dataset folder

So for interfacing to the above criteria the flag variable must be passed.
No need to implement for predicting.

'''


class GetFiles:

    def __init__(self, dataset_directory_path=f"{ROOT_DIR}/user"):
        """
        @:param

        dataset: dataset is the root path for dataset(test,train,predict)
                all the data-sets  are stored as sub-folder inside this folder

        """
        self.dataset_directory_path = dataset_directory_path

    def get_train_files(self, train_speaker_folder, flag="training"):

        '''
        @:param
        flag: flag is used to indicate which sub folder in the dataset is to be
              extracted. For example train or test or predict.
        Possible values:
            flag = train / test / predict

        train_speaker_folder : dataset for particular speaker folder
                Description: Actually, the list of audio files must be placed inside
                             the folder with speaker name in testing and training.
        '''

        data_frame_row = []
        #  each row consists of audio_path and the target(who is the speaker)

        sub_files = os.listdir(self.dataset_directory_path + "/" + train_speaker_folder + "/" + flag)
        for files in sub_files:
            path_to_audio = self.dataset_directory_path + "/" + train_speaker_folder + "/" + flag + "/" + files
            # "dataset/train/surya"
            # creating a row for appending in the frame
            # row consists of the path for that files inside the parent_folder
            data_frame_row.append([path_to_audio, train_speaker_folder])
        data_frame = pd.DataFrame(data_frame_row, columns=['audio_path', 'target_speaker'])

        return data_frame

    def get_test_files(self):

        data_frame_row = []

        data_frame = pd.DataFrame()

        flag = "test"

        # root test dierctory files listing
        speaker_audio_folder = os.listdir(self.dataset_directory_path + "/" + flag)

        for folders in speaker_audio_folder:

            audio_files = os.listdir(self.dataset_directory_path + "/" + flag + "/" + folders)
            # listing of sub directory

            for files in audio_files:
                path_to_audio = self.dataset_directory_path + "/" + flag + "/" + folders + "/" + files
                data_frame_row.append([path_to_audio, folders])

            data_frame = pd.DataFrame(data_frame_row, columns=['audio_path', 'actual'])

        return data_frame
