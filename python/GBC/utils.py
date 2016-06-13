import pandas as pd
import pickle
import logging
log = logging.getLogger(__name__)

def labels_to_binary(labels):
    return (labels == 's').astype(int)

def remove_cheat_columns(data):
    return data.drop(['EventId', 'Weight', 'Label',
                      'KaggleSet', 'KaggleWeight'],
                      axis = 1)

def get_data_labels_weights(data_path):
    df = pd.read_csv(data_path)
    log.info('Read CSV data with shape {}'.format(df.shape))

    data = remove_cheat_columns(df)
    labels = labels_to_binary(df['Label'])
    weights = df['Weight']

    return data, labels, weights

def delta_time(start, end):
    delta = int(end - start)
    m, s = divmod(delta, 60)
    h, m = divmod(m, 60)
    return '{:d}:{:02d}:{:02d}'.format(h, m, s)

def save(clf, path):
    log.info('Saving to {}'.format(path))
    with open(path, 'w') as f:
        pickle.dump(clf, f)

def load(path):
    log.info('Loading from {}'.format(path))
    try:
        with open(path, 'r') as f:
            clf = pickle.load(f)
            return clf
    except IOError, EOFError:
        print 'Problem loading', path

def normalise_weights(weights, labels):
    reweight = lambda w: w/w.sum()
    return weights.groupby(labels).transform(reweight)

def split_sig_bkg(classes, *dataframes):
    sig = []
    bkg = []
    for df in dataframes:
        sig.append(df[classes == 1])
        bkg.append(df[classes == 0])
    return reduce(lambda a, b: a + b, zip(sig, bkg))
