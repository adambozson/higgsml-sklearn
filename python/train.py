import os, time
from sklearn.cross_validation import train_test_split
from utils import get_data_labels_weights, delta_time, save
from classifiers import BoostedDecisionTree

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def normalise_weights(weights, labels):
    reweight = lambda w: w/w.sum()
    return weights.groupby(labels).transform(reweight)

def cross_val_error(clf, X_test, y_test, w_test):
    score = clf.score(X_test, y_test, sample_weight=w_test)
    return 1.0 - score

# Run when invoked from the command line
if __name__ == '__main__':
    DATA_F = 'atlas-higgs-challenge-2014-v2.csv'
    TEST_SIZE = 0.5
    OUTPUT = 'BDT.pkl'

    data_path = os.path.join('data', DATA_F)
    log.info('Reading data from {}'.format(data_path))
    data, labels, weights = get_data_labels_weights(data_path)

    log.info('Splitting into train/test samples with test size {:f}'.format(
        TEST_SIZE))
    X_train, X_test, y_train, y_test, w_train, w_test = train_test_split(
        data, labels, weights, test_size=TEST_SIZE)

    log.info('Renormalising training weights')
    log.debug('Sum of training weights before renormalising:')
    log.debug(w_train.groupby(y_train).sum())
    w_train_normed = normalise_weights(w_train, y_train)
    log.debug('Sum of training weights after renormalising:')
    log.debug(w_train_normed.groupby(y_train).sum())

    bdt = BoostedDecisionTree()
    log.info('Created classifier\n{}'.format(bdt))

    log.info('Training classifier...')
    start_time = time.time()
    bdt.fit(X_train, y_train, sample_weight=w_train_normed.values)
    end_time = time.time()
    log.info('Training completed in {}'.format(delta_time(start_time, end_time)))

    log.info('Calculating cross-validation error')
    error = cross_val_error(bdt, X_test, y_test, w_test)
    log.info('Error: {:.3f}'.format(error))

    save(bdt, OUTPUT)
