import os, requests, gzip
from clint.textui import progress, colored

DATA_DIR = 'data'
URL = 'http://opendata.cern.ch/record/328/files/atlas-higgs-challenge-2014-v2.csv.gz'
DEST_FILE = 'atlas-higgs-challenge-2014-v2.csv'

def create_directory(dir):
    print colored.blue('Creating directory \'{}\'...'.format(dir)),
    try:
        os.makedirs(dir)
        print colored.green('Done')
    except OSError as e:
        if e.errno == os.errno.EEXIST:
            print colored.blue('Already exists')
        else:
            raise

def download_file(url, dest_path):
    print colored.blue('Downloading {}...'.format(url))
    req = requests.get(url, stream=True)
    with open(dest_path, 'wb') as f:
        total_size = int(req.headers.get('content-length'))
        for chunk in progress.bar(req.iter_content(chunk_size=1024),
                                  expected_size=(total_size/1024)+1):
            if chunk:
                f.write(chunk)
                f.flush()
    print colored.green('Done. File at {}'.format(dest_path))

def unzip(from_path, to_path):
    print colored.blue('Decompressing to \'{}\'...'.format(to_path))
    with gzip.open(from_path, 'rb') as f_in:
        lines = f_in.readlines()
        with open(to_path, 'w') as f_out:
            for line in progress.bar(lines):
                f_out.write(line)

if __name__ == '__main__':
    create_directory(DATA_DIR)
    download_file(URL, os.path.join(DATA_DIR, DEST_FILE))
