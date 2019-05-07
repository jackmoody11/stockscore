.. _screens:


.. currentmodule:: stockscore

stockscore Screens
==================

The `stockscore` module relies on many different screens. Screens relate to certain 
"scores." The `Scores` object takes one or more ticker symbols.

.. autoclass:: stockscore.scores.Scores

Each stock is given scores based on relevant statistics. The available score 
categories are:

* :ref:`Value<screens.value>`
* :ref:`Growth<screens.growth>`
* :ref:`Momentum<screens.momentum>`

.. _screens.value:

Value
~~~~~
- :ref:`Trading Volume <screens.trading_volume_screen>`
- :ref:`Net Income <screens.net_income_screen>`
- :ref:`Current Ratio <screens.current_ratio_screen>`
- :ref:`Price/Book Ratio <screens.pb_ratio_screen>`
- :ref:`Price/Earnings Ratio <screens.pe_ratio_screen>`
- :ref:`Profit Margin <screens.profit_margin_screen>`
- :ref:`Dividend <screens.dividend_screen>`

.. _screens.growth:

Growth
~~~~~~
- :ref:`Splits <screens.splits_screen>`

.. _screens.momentum: 

Momentum
~~~~~~~~
- :ref:`Moving Avg <screens.moving_avg_screen>`
- Trading Volume (See :ref:`screens.value`)
- :ref:`Splits <screens.splits_screen>`

.. _screens.trading_volume_screen:

Trading Volume
--------------
.. automethod:: stockscore.scores.Scores.trading_volume_screen

.. _screens.net_income_screen:

Net Income
----------
.. automethod:: stockscore.scores.Scores.net_income_screen

.. _screens.current_ratio_screen:

Current Ratio
-------------
.. automethod:: stockscore.scores.Scores.current_ratio_screen

.. _screens.pb_ratio_screen:

Price/Book
----------
.. automethod:: stockscore.scores.Scores.pb_ratio_screen

.. _screens.pe_ratio_screen:

Price/Earnings
--------------
.. automethod:: stockscore.scores.Scores.pe_ratio_screen

.. _screens.profit_margin_screen:

Profit Margin
-------------
.. automethod:: stockscore.scores.Scores.profit_margin_screen

.. _screens.dividend_screen:

Dividend
--------
.. automethod:: stockscore.scores.Scores.dividend_screen


.. _screens.splits_screen:

Splits
------
.. automethod:: stockscore.scores.Scores.splits_screen


.. _screens.moving_avg_screen:

Moving Avg
----------
.. automethod:: stockscore.scores.Scores.moving_avg_screen
