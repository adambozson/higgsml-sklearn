import utilities, argparse, dill, numpy, time
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.cross_validation import cross_val_score, StratifiedKFold
from sklearn.metrics import f1_score
from joblib import Parallel, delayed

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_estimators', type=int, default=100)
    parser.add_argument('--max_depth', type=int, default=3)
    parser.add_argument('--min_weight_fraction_leaf', type=float, default=.05)
    parser.add_argument('--max_features', type=int, default=None)
    return vars(parser.parse_args())

def make_GBC(n_estimators=100, max_depth=3,
             min_weight_fraction_leaf=.05, max_features=None):
    return GradientBoostingClassifier(loss='exponential',
                                      n_estimators=n_estimators,
                                      min_weight_fraction_leaf=min_weight_fraction_leaf,
                                      max_depth=max_depth,
                                      max_features=max_features,
                                      verbose=2)

def fold_score(clf, X, y, w, train_idx, test_idx):
    clf = clf.fit(X.values[train_idx], y.values[train_idx],
                  sample_weight=w.values[train_idx])
    return f1_score(y.values[test_idx], clf.predict(X.values[test_idx]),
                     sample_weight=w.values[test_idx])

def train_cv(clf, X, y, w):
    score = lambda clf, X, y: f1_score(y, clf.predict(X), sample_weight=w_norm)
    skf = StratifiedKFold(y, n_folds=5)
    scores = Parallel(n_jobs=-1, verbose=11)(delayed(fold_score)(clf, X, y, w, train_idx, test_idx) for train_idx, test_idx in skf)
    log.info('Cross-validation scores: {}'.format(scores))
    return numpy.mean(scores)

if __name__ == '__main__':
    TRAIN_DATA = 'atlas-higgs-challenge-2014-v2_train.csv'
    OUTPUT = 'GBC.pkl'

    args = parse_args()

    log.info('Reading data from {}'.format(TRAIN_DATA))
    X, y, w = utilities.get_data_labels_weights(TRAIN_DATA)

    log.info('Renormalising weights')
    w_norm = utilities.normalise_weights(w, y)

    gbc = make_GBC(**args)
    log.info('Created classifier\n{}'.format(gbc))

    log.info('Calculating cross-validation score...')
    start_time = time.time()
    mean_score = train_cv(gbc, X, y, w_norm)
    end_time = time.time()
    log.info('Completed in {}'.format(utilities.delta_time(start_time, end_time)))
    print 'Mean cross-validation score: {}'.format(mean_score)
