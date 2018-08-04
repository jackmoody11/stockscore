Stock Scores
============
.. image:: https://www.codefactor.io/repository/github/jackmoody11/stockscores/badge 
   :target: https://www.codefactor.io/repository/github/jackmoody11/stockscores

.. image:: https://api.codacy.com/project/badge/Grade/d2108117522f4fe498530c6f7185108e
   :target: https://www.codacy.com/project/jacklaytonmoody/stockScores/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=jackmoody11/stockScores&amp;utm_campaign=Badge_Grade_Dashboard

.. image:: https://travis-ci.com/jackmoody11/stockScores.svg?branch=master
    :target: https://travis-ci.com/jackmoody11/stockScores

Stock Scores is a python script to score stocks based on specified
criteria. The goal of this project is to provide a powerful stock scoring
system for various types of stock classifications (growth, momentum, value, etc.).

Similar to how one might rank the best options when they are deciding
where to go to dinner, Stock Scores lets investors choose what screens
they want to run. Then, this script takes care of the rest,
showing which stocks performed best under the given tests.

*Note: This README is a work in progress*

Prerequisites
~~~~~~~~~~~~~

- You can get the latest version of Python 3 here_ (this should come with the latest version of pip)
- All dependencies are contained in `requirements.txt` (more on that directly below)

Installing
~~~~~~~~~~

A step by step series of examples that tell you how to get a development
env running

To clone this, run the following:

::

    git clone https://github.com/jackmoody11/stockScores

These instructions will get you a copy of the project up and running on
your local machine for development and testing purposes. See deployment
for notes on how to deploy the project on a live system.

Make sure you have virtualenv installed

::

   pip install virtualenv

Change working directory to project folder

::

    cd my/path/to/stockScore

Create a virtual environment
For Mac users:
::

    python3 -m virtualenv env 

For Windows users:
::
    
    py -m virtualenv env # for Windows users


Make a virtual environment with :code:`python3 -m venv my-env`.
Then, in order to activate the virtual environment run the following:

For Mac users:

::

    source my-env/bin/activate

For Windows users:

::

    .\my-env\Scripts\activate

Then use :code:`pip3 install -r requirements.txt` to install required modules.

End with an example of getting some data out of the system or using it
for a little demo

Running the tests
-----------------

Once the environment is setup, all tests can be run by simply running
::

    py.test

from the command line.


In order to run a specific test (like test_fundamental_functions.py), run
::

    py.test tests/test_fundamental_functions.py


For more information on how to use py.test (like how to select a few tests),
`look here`_ for the official py.test docs.

Break down into end to end tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Stock Score tests aim to make sure that the program is able to retrieve data
from the IEX API and use that data to properly score the stocks based on
certain numbers relating to the stocks.


And coding style tests
~~~~~~~~~~~~~~~~~~~~~~

Explain what these tests test and why

::

   Give an example

Deployment
----------

Add additional notes about how to deploy this on a live system

Built With
----------

Python 3 and some great third party modules.

Contributing
------------

Please read `CODE_OF_CONDUCT.md`_ for details on our code of conduct, and
the process for submitting pull requests to us.

Versioning
----------

We use `SemVer`_ for versioning. For the versions available, see the
`tags on this repository`_.


License
-------

This project is licensed under the MIT License - see the `LICENSE`_
file for details

Acknowledgments
---------------

-  Hat tip to Benjamin Graham's *Intelligent Investor*. If you haven't already, read this book!

.. _here: https://docs.python.org/3/installing/
.. _look here: https://pytestguide.readthedocs.io/en/latest/
.. _Dropwizard: http://www.dropwizard.io/1.0.2/docs/
.. _Maven: https://maven.apache.org/
.. _ROME: https://rometools.github.io/rome/
.. _CODE_OF_CONDUCT.md: CODE_OF_CONDUCT.md
.. _SemVer: http://semver.org/
.. _tags on this repository: https://github.com/jackmoody11/stockScores/tags
.. _LICENSE: https://github.com/jackmoody11/stockScores/blob/master/LICENSE
