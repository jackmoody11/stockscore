.. _screens:

stockscore Screens
==================

The `stockscore` module relies on many different screens. Screens relate to certain 
"scores." Each stock is given scores based on relevant statistics. The available score 
categories are:
 * Value
 * Growth
 * Momentum

Value
~~~~~
* :ref:`Trading Volume<scores.trading_volume_screen>`
* :ref:`Net Income<scores.net_income_screen>`
* :ref:`Current Ratio<scores.current_ratio_screen>`
* :ref:`Price/Book Ratio<scores.p_to_b_screen>`
* :ref:`Price/Earnings Ratio<scores.p_to_e_screen>`
* :ref:`Profit Margin<scores.profit_margin_screen>`
* :ref:`Dividend<scores.dividend_screen>`

Growth
~~~~~~
* :ref:`Splits<scores.splits_screen>`

Momentum
~~~~~~~~
* :ref:`Moving Avg<scores.moving_avg_screen>`
* :ref:`Trading Volume<scores.trading_volume_screen>`
* :ref:`Splits<scores.splits_screen>`

Value
~~~~~

.. _scores.trading_volume_screen:

Trading Volume
--------------
.. automethod:: stockscore.scores.Scores.trading_volume_screen

.. _scores.net_income_screen:

Net Income
----------
.. automethod:: stockscore.scores.Scores.net_income_screen

.. _scores.current_ratio_screen:

Current Ratio
-------------
.. automethod:: stockscore.scores.Scores.current_ratio_screen

.. _scores.p_to_b_screen:

Price/Book
----------
.. automethod:: stockscore.scores.Scores.p_to_b_screen

.. _scores.p_to_e_screen:

Price/Earnings
--------------
.. automethod:: stockscore.scores.Scores.p_to_e_screen

.. _scores.profit_margin_screen:

Profit Margin
-------------
.. automethod:: stockscore.scores.Scores.profit_margin_screen

.. _scores.dividend_screen:

Dividend
--------
.. automethod:: stockscore.scores.Scores.dividend_screen


Growth
~~~~~~

.. _scores.splits_screen:

Splits
------
.. automethod:: stockscore.scores.Scores.splits_screen

Momentum
~~~~~~~~

.. _scores.moving_avg_screen:

Moving Avg
----------
.. automethod:: stockscore.scores.Scores.moving_avg_screen

.. _scores.trading_volume_screen:

Trading Volume
--------------
.. automethod:: stockscore.scores.Scores.trading_volume_screen

.. _scores.splits_screen

Splits
------
.. automethod:: stockscore.scores.Scores.splits_screen
