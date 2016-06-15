# Main file for the spearmint experiment
# Configuration in config.json

from train import make_GBC
from sv import train_cv
from utilities import get_data_labels_weights, normalise_weights, delta_time
import time

def main(job_id, params):
    print 'Parameters: {}'.format(params)

    TRAIN_DATA = 'atlas-higgs-challenge-2014-v2_train.csv'

    print 'Reading data from {}'.format(TRAIN_DATA)
    X, y, w = get_data_labels_weights(TRAIN_DATA)
    w_norm = normalise_weights(w, y)

    gbc = make_GBC(n_estimators=params['n_estimators'][0],
                  max_features=params['max_features'][0],
                  min_weight_fraction_leaf=params['min_weight_fraction_leaf'][0],
                  max_depth=params['max_depth'][0])
    print 'Created classifier\n{}'.format(gbc)

    print 'Calculating cross-validation score...'
    start_time = time.time()
    mean_score = train_cv(gbc, X, y, w_norm)
    end_time = time.time()
    print 'Completed in {}'.format(delta_time(start_time, end_time))
