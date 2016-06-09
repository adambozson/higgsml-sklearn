# higgsml-sklearn
A demonstration of scikit-learn using the Higgs Boson Machine Learning Challenge dataset.

## Prerequisites
* Python (version 2.7)
* virtualenv -- install with pip, or [manually](https://virtualenv.pypa.io/en/stable/installation/)

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
(Try `python2.7 setup.py` if the last step fails.)

3. Activate the higgsml virtual environment:
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

6. Click on `Tutorial.ipynb` to walk through the tutorial.

## Troubleshooting
Make sure the higgsml virtual environment is activated (run `source activate` from the main higgsml-sklearn directory).

## Tips & tricks
### Working over SSH
You may wish to run on a more powerful, air-conditioned machine over an SSH connection. In this case, use port forwarding to access the Jupyter notebooks. In Step 5 above, start the notebook server with
```bash
jupyter notebook --no-browser
```
There will be a line similar to
```shell
[I 17:22:38.962 NotebookApp] The Jupyter Notebook is running at: http://localhost:XXXX/
```
in the output, where `XXXX` is the port number (default is 8888). Use the SSH magic key combination, normally <kbd>Enter</kbd>+<kbd>~</kbd>+<kbd>C</kbd> to enter the SSH prompt. Then enter
```shell
-L XXXX:localhost:XXXX
```
and point the web browser on your *local* machine at [http://localhost:XXXX/](http://localhost:XXXX/).
