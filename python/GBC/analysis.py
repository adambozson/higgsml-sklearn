import utilities
import argparse
import numpy as np
import pandas as pd

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('clf', type=str, metavar='CLASSIFIER')
    parser.add_argument('--out', '-o', type=str,
                        help='Save significance curve CSV to file OUT')
    return vars(parser.parse_args())

def get_test_sig_bkg():
    TEST_DATA = 'atlas-higgs-challenge-2014-v2_test.csv'
    SIG_WEIGHT = 691.988608
    BKG_WEIGHT = 410999.847322

    log.info('Reading data from {}'.format(TEST_DATA))
    X, y, w = utilities.get_data_labels_weights(TEST_DATA)

    log.info('Splitting into signal/background')
    X_sig, X_bkg, w_sig, w_bkg = utilities.split_sig_bkg(y, X, w)
    log.info('Sum of weights (samples):')
    log.info('Sig: {:.2f} ({:d}), Bkg: {:.2f} ({:d})'.format(w_sig.sum(),
                                                             X_sig.shape[0],
                                                             w_bkg.sum(),
                                                             X_bkg.shape[0]))

    log.info('Renormalising weights (assuming stratified split)')
    w_sig = w_sig * SIG_WEIGHT / w_sig.sum()
    w_bkg = w_bkg * BKG_WEIGHT / w_bkg.sum()
    log.info('Renormalised weights:')
    log.info('Sig: {:.2f}, Bkg: {:.2f}'.format(w_sig.sum(), w_bkg.sum()))

    return X_sig, X_bkg, w_sig, w_bkg

def sum_weights_above(t_cut, t, weights):
    mask = t > t_cut
    return weights[mask].sum()

def ZA(s, b):
    if b > 0:
        return np.sqrt(2 * ((s+b) * np.log(1 + s/b) - s))
    else:
        return np.nan

def Z0(s, b):
    if b > 0:
        return s / np.sqrt(b)
    else:
        return np.nan

def discovery_significance(p_sig, p_bkg, w_sig=None, w_bkg=None,
                           t_range=(-1., 1.), step=.01):
    if w_sig is None:
        w_sig = np.ones(p_sig.shape)
    if w_bkg is None:
        w_bkg = np.ones(p_bkg.shape)
    cuts = np.arange(t_range[0], t_range[1], step)
    rows = []
    for t_cut in cuts:
        s = sum_weights_above(t_cut, p_sig, w_sig)
        b = sum_weights_above(t_cut, p_bkg, w_bkg)
        row = [t_cut, s, b, Z0(s, b), ZA(s, b)]
        log.debug(row)
        rows.append(row)
    return pd.DataFrame(rows, columns=['t_cut', 's', 'b', 'Z0', 'ZA'])

def print_max_significance(discovery_sig_df):
    max_sig_idx = discovery_sig_df['ZA'].idxmax()
    max_sig_data = discovery_sig_df.iloc[max_sig_idx]
    max_sig = max_sig_data['ZA']
    max_sig_cut = max_sig_data['t_cut']
    max_sig_str = 'Max significance {:.2f} for cut value {:.4f}'.format(max_sig, max_sig_cut)
    print max_sig_str
    return {'str': max_sig_str, 'cut': max_sig_cut, 'value': max_sig}

if __name__ == '__main__':
    args = parse_args()
    X_sig, X_bkg, w_sig, w_bkg = get_test_sig_bkg()

    log.info('Loading classifier from {}'.format(args['clf']))
    clf = utilities.load(args['clf'])
    log.info('Loaded classifier\n{}'.format(clf))

    log.info('Calculating predictions...')
    p_sig = clf.decision_function(X_sig)
    log.debug(p_sig)
    log.debug('Mean: {:.5f}'.format(np.mean(p_sig)))
    p_bkg = clf.decision_function(X_bkg)
    log.debug(p_bkg)
    log.debug('Mean: {:.5f}'.format(np.mean(p_bkg)))

    ds = discovery_significance(p_sig, p_bkg, w_sig, w_bkg,
                                t_range=(-2.5, 2.5))
    if args['out']:
        log.info('Saving discovery significance curve to {}'.format(args['out']))
        ds.to_csv(args['out'], index=False)
    print_max_significance(ds)
