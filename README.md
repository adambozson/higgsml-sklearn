# higgsml-sklearn
A demonstration of scikit-learn using the Higgs Boson Machine Learning Challenge dataset.

## Prerequisites
* Python (version 2.7)
* virtualenv -- install with `pip`, or [manually](https://virtualenv.pypa.io/en/stable/installation/)

(Tested on Linux and Mac.)

## Getting started
1. Clone (or download) this repo:
```bash
git clone https://github.com/adambozson/higgsml-sklearn.git
```

2. Run the setup script:
```bash
cd higgsml-sklearn
python setup.py
```

3. Activate the `higgsml` virtual environment:
```bash
source activate
```

4. Download the data file:
```bash
python download_data.py
```

5. Start up the Jupyter notebook server:
```bash
jupyter notebook
```

6. Click on *Tutorial.ipynb* to walk through the tutorial.
