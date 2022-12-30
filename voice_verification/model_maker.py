import numpy as np
from sklearn.mixture import GaussianMixture

from voice_verification.utils.feature_extraction import ExtractFeature

'''
This portion consists of making GMM model.

Different Phase Strategy to be adopted:

1. First Phase:
    a. Just focus on developing the model.
    b. Weather it be full of accuracy or not. Dont't think of accuracy at first
    c. Use GMM with any parameters.

2. Second Phase
    a. Try to optimize the model's hyper-parameter
    b. Focus only on hyper-parameters

3. Third Phase:
    a. Try to build the functionality of data pre-processing
    b. Add extra functionality


Currently practicing on phase1. Timeline 1 day.
'''

'''
Tips: If the model representive of the different audio files are to be made.
      Just stack the feature of the different audio files into one array
      and find out the gaussian distribution for the model. 
'''

# Documentation at: https://scikit-learn.org/stable/modules/generated/sklearn.mixture.GaussianMixture.html
# Description of the functional parameters
# these functional parameters needs to be tuned.

# gmm = GMM(n_components=16, n_iter=200, covariance_type='diag', n_init=3)

model_save_path = "user/{}/model/gmm"  # directory in which model is to saved


def make_model(pipelined_data_frame):
    features = get_stacked_features(pipelined_data_frame)

    model_name = pipelined_data_frame["target_speaker"].iloc[0]  # get name of speaker

    # make model
    gmm = GaussianMixture(n_components=16, covariance_type='diag', max_iter=500, n_init=3, verbose=1)
    gmm.fit(features)

    # save to file
    model_path = model_save_path.format(model_name)
    save_model(gmm, model_path)


def get_stacked_features(pipelined_data_frame):
    ef = ExtractFeature  # object to extract the feature

    first_audio_location_in_frame = pipelined_data_frame["audio_path"].iloc[0]  # first audio path in pandas frame
    stacked_feature = ef.extract_features(first_audio_location_in_frame)  # first training audio's feature

    for index, row in pipelined_data_frame.iterrows():  # iterating through the pandas frame
        if index != 0:  # escaping the first audio's feature
            ef = ExtractFeature
            currently_fetched_feature = ef.extract_features(row['audio_path'])  # one feature extracted
            stacked_feature = np.vstack((stacked_feature, currently_fetched_feature))
    return stacked_feature


def save_model(model, model_path):
    np.save(model_path + '_weights', model.weights_, allow_pickle=False)
    np.save(model_path + '_precisions_cholesky', model.precisions_cholesky_, allow_pickle=False)
    np.save(model_path + '_means', model.means_, allow_pickle=False)
    np.save(model_path + '_covariances', model.covariances_, allow_pickle=False)
