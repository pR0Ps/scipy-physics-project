Project for PHYS 104
====================

Installation - Windows
----------------------

1. Install [pyzo](http://www.pyzo.org/). It comes with the full SciPy stack.

Installation - UNIX
-------------------

1. Install [Python 3](http://www.python.org/download/releases/3.3.4/).
2. Install [pip](http://www.pip-installer.org/) and [virtualenv](http://www.virtualenv.org/).
3. Make a new virtual environment and activate it.
4. Install dependencies for Scipy (`sudo apt-get build-dep python-numpy python-scipy`).
5. Install the required packages (`pip install -r requirements.txt`).

Instructions
------------

- Run `python main.py` to run the script
- To run an IPython shell run `ipython3`
- To run the IPython web notebook insterface run `ipython3 notebook`
- To convert an IPython notebook to HTML run `ipython3 nbconvert --to html book.ipynb`
