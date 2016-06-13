import os
import numpy as np
import pandas as pd
from utils import load, get_data_labels_weights

import logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def split_sig_bkg(classes, *dataframes):
    sig = []
    bkg = []
    for df in dataframes:
        sig.append(df[classes == 1])
        bkg.append(df[classes == 0])
    return reduce(lambda a, b: a + b, zip(sig, bkg))

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
                           t_range=(-.5, .5), step=.01):
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
    max_sig_str = 'Max significance {:.2f} for cut value {}'.format(max_sig, max_sig_cut)
    print max_sig_str

if __name__ == '__main__':
    DATA_F = 'atlas-higgs-challenge-2014-v2.csv'
    CLF_F = 'BDT.pkl'

    data_path = os.path.join('data', DATA_F)
    log.info('Reading data from {}'.format(data_path))
    data, labels, weights = get_data_labels_weights(data_path)

    log.info('Splitting into signal and background samples')
    X_sig, X_bkg, w_sig, w_bkg = split_sig_bkg(labels, data, weights)

    clf = load(CLF_F)

    log.info('Calculating classifier predictions')
    p_sig = clf.decision_function(X_sig)
    p_bkg = clf.decision_function(X_bkg)

    log.info('Scanning discovery significance over cut values')
    ds = discovery_significance(p_sig, p_bkg, w_sig, w_bkg)

    print_max_significance(ds)
