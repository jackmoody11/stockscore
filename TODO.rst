To Do
=====
Instead of constantly updating a TODO list, this project will
utilize the *issues* and *projects* tabs in Github to keep track of
what enhancements are left to do. Below is information that is too long
for Github issues:


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
