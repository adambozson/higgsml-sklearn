import utilities, argparse, time
from sklearn.ensemble import GradientBoostingClassifier

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_estimators', type=int, default=100)
    parser.add_argument('--max_depth', type=int, default=3)
    parser.add_argument('--min_weight_fraction_leaf', type=float, default=.05)
    parser.add_argument('--max_features', type=int, default=None)
    parser.add_argument('save', metavar='SAVE_FILE')
    return vars(parser.parse_args())

def make_GBC(n_estimators=100, max_depth=3,
             min_weight_fraction_leaf=.05, max_features=None):
    return GradientBoostingClassifier(loss='exponential',
                                      n_estimators=n_estimators,
                                      min_weight_fraction_leaf=min_weight_fraction_leaf,
                                      max_depth=max_depth,
                                      max_features=max_features,
                                      verbose=2)

if __name__ == '__main__':
    TRAIN_DATA = 'atlas-higgs-challenge-2014-v2_train.csv'

    args = parse_args()
    save_arg = args.pop('save')

    log.info('Reading data from {}'.format(TRAIN_DATA))
    X, y, w = utilities.get_data_labels_weights(TRAIN_DATA)

    log.info('Renormalising weights')
    w_norm = utilities.normalise_weights(w, y)

    gbc = make_GBC(**args)
    log.info('Created classifier\n{}'.format(gbc))

    log.info('Training classifier...')
    start_time = time.time()
    mean_score = gbc.fit(X, y, sample_weight=w_norm)
    end_time = time.time()
    log.info('Completed in {}'.format(utilities.delta_time(start_time, end_time)))

    log.info('Saving classifier as {}'.format(save_arg))
    utilities.save(gbc, save_arg)
