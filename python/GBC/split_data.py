from sklearn.cross_validation import train_test_split
from os import path
import argparse
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(description=
        'Split CSV into train and test samples.')
    parser.add_argument('data', type=str, help='Input data file (CSV)')
    parser.add_argument('--test_size', '-t', type=float, default=0.2)
    parser.add_argument('--stratify', '-s', default=None)
    return vars(parser.parse_args())

if __name__ == '__main__':
    args = parse_args()
    test_size = args['test_size']
    input_path = args['data']
    stratify_column = args['stratify']

    data = pd.read_csv(input_path)

    if stratify_column is None:
        labels = None
    else:
        labels = data[stratify_column].values

    train, test = train_test_split(data, test_size=test_size, stratify=labels)

    input_path_split = path.splitext(path.split(input_path)[1])
    train_path = input_path_split[0] + '_train' + input_path_split[1]
    test_path = input_path_split[0] + '_test' + input_path_split[1]

    train.to_csv(train_path, index=False)
    test.to_csv(test_path, index=False)
