Stock Scores
============

Stock Scores is a python script to score stocks based on specified
criteria. The goal of this project is to eliminate unnecessary filtering
by providing a powerful stock score system.

Similar to how one might rank the best options when they are deciding
where to go to dinner, Stock Scores lets investors choose what criteria
they value and how much they value each criterion. Then, this script
will take care of the rest, showing which stocks performed best under
corresponding tests.

Getting Started
---------------

To clone this, run the following:

``git clone https://github.com/jackmoody11/stockScores``

APIs for future use
-------------------

Though these APIs are not being used yet, the authentication
instructions are included below in order to encourage users to use the
resources below to experiment with other data sources.

Suggestions for free financial data sources are welcome and encouraged!

Visit `here`_ to sign up for Intrinio. After signing up, you will need
to set ``in_user`` and ``in_pass`` as environment variables on your
local machine.

Similarly, visit `here <https://www.alphavantage.co>`__ to sign up for
Alpha Vantage. After signing up and getting your API key, you will need
to set ``av_api_key`` as an environment variable on your local machine.

For Mac users, open up terminal and type ``open .bash_profile``. A text
editor should open and then you will be able to export your variables by
using ``export in_user = *your_username_here*``,
``export in_pass = *password here*``, etc.

.. _here: https://intrinio.com/signup
