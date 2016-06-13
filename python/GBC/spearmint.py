# Main file for the spearmint experiment
# Configuration in config.json

from train import make_GBC, train_cv
import utils, time

def gbc_cv(**args):
    TRAIN_DATA = 'atlas-higgs-challenge-2014-v2_train.csv'

    print 'Reading data from {}'.format(TRAIN_DATA)
    X, y, w = utils.get_data_labels_weights(TRAIN_DATA)
    w_norm = utils.normalise_weights(w, y)

    gbc = make_GBC(**args)
    print 'Created classifier\n{}'.format(gbc)

    print 'Calculating cross-validation score...'
    start_time = time.time()
    mean_score = train_cv(gbc, X, y, w_norm)
    end_time = time.time()
    print 'Completed in {}'.format(utils.delta_time(start_time, end_time))

    return mean_score

def main(job_id, params):
    print 'Parameters: {}'.format(params)
    return 1.0
