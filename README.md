# higgsml-sklearn
A demonstration of scikit-learn using the [Higgs Boson Machine Learning Challenge](https://higgsml.lal.in2p3.fr) dataset.

1. Download the data file:

    ```bash
    python download_data.py
    ```

2. Start up the Jupyter notebook server:

    ```bash
    jupyter notebook
    ```

3. Click on `Tutorial.ipynb` in the browser to walk through the tutorial.

## Scripted analysis
A set of scripts for training and analysis are in the `python` directory. From the project directory, run `python python/BDT200/train.py` to train the TMVA-like model. Then run `python python/BDT200/analysis.py` to calculate the expected discovery significance.

## Tips & tricks
### Working over SSH
You may wish to run on a more powerful, air-conditioned machine over an SSH connection. In this case, use port forwarding to access the Jupyter notebooks. In Step 2 above, start the notebook server with
```bash
jupyter notebook --no-browser
```
There will be a line similar to
```shell
[I 17:22:38.962 NotebookApp] The Jupyter Notebook is running at: http://localhost:XXXX/
```
in the output, where `XXXX` is the port number (default is 8888). Use the SSH magic key combination, normally <kbd>Enter</kbd>+<kbd>~</kbd>+<kbd>C</kbd> to enter the SSH prompt. Then enter `-L XXXX:localhost:XXXX` and point the web browser on your *local* machine to [http://localhost:XXXX/](http://localhost:XXXX/).
