import numpy as np
from sklearn import mixture

from voice_verification.utils.feature_extraction import ExtractFeature
from constants import ROOT_DIR

user_test_audio_path = ROOT_DIR + '/test.wav'
user_gmm_model_path_format = ROOT_DIR + '/user/{}/model/gmm'
minimum_probability = -18


def load_model(user_name: str):
    """
    @:param user_name : name of the model owner

    @:return: Returns loaded model
    """
    gmm_file = user_gmm_model_path_format.format(user_name)
    means = np.load(gmm_file + '_means.npy')
    covar = np.load(gmm_file + '_covariances.npy')
    loaded_gmm = mixture.GaussianMixture(n_components=len(means), covariance_type='diag')
    loaded_gmm.precisions_cholesky_ = np.load(gmm_file + '_precisions_cholesky.npy')
    loaded_gmm.weights_ = np.load(gmm_file + '_weights.npy')
    loaded_gmm.means_ = means
    loaded_gmm.covariances_ = covar
    return loaded_gmm


def test_predict(user_name: str):
    """
    @:param user_name : name of the user to be tested

    @:return: Returns the sum of GMM probabilities per sample
    """

    ef = ExtractFeature

    # existing model
    model = load_model(user_name=user_name)

    test_audio_path = user_test_audio_path

    # features of the file to be predicted
    feature = ef.extract_features(test_audio_path)
    print(feature.shape)

    gmm = model
    scores = np.array(gmm.score(feature))
    score_of_individual_comparision = scores.sum()

    print(score_of_individual_comparision)

    return score_of_individual_comparision


def predict(user_name) -> bool:
    """
    @param user_name : name of the user to be verificated
    @return: Returns bool if user was verificated
    """
    speaker_probability = test_predict(user_name)
    return minimum_probability < speaker_probability
