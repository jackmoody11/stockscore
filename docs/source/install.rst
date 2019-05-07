.. _install:


Install
=======

Dependencies
------------

stockscore relies on:

- grequests
- iexfinance
- matplotlib
- pandas
- requests

Installation
------------

Latest stable release via pip (recommended):

.. code:: bash

    $ pip install stockscore

Latest development version:

.. code:: bash

    $ pip install git+https://github.com/jackmoody11/stockscore.git

or

.. code:: bash

    $ git clone https://github.com/jackmoody11/stockscore.git
    $ cd stockscore
    $ pip install .

**Note:**

The use of virtual environments is recommended as below. 
Using `virtualenv` may cause problems due to a `known conflict<https://matplotlib.org/faq/virtualenv_faq.html>`__ 
with `matplotlib`.

.. code:: bash

    $ python3 -m venv myenv
    $ source myvenv/bin/activate