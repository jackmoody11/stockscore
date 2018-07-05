import pandas as pd
import numpy as np
from intrinio.client import get


def companies(identifier=None, query=None):
    """
    Get companies with optional filtering using parameters.

    Args:
        identifier: Identifier for the legal entity or a security associated
            with the company: TICKER SYMBOL | FIGI | OTHER IDENTIFIER
        query: Search of company name or ticker symbol

    Returns:
        Dataset as a Pandas DataFrame
    """
    return get('companies',
               identifier=_upper_optional(identifier),
               query=query)


def securities(identifier=None, query=None, exch_symbol=None):
    """
    Get securities with optional filtering using parameters.

    Args:
        identifier: Identifier for the legal entity or a security associated
            with the company: TICKER SYMBOL | FIGI | OTHER IDENTIFIER
        query: Search of security name or ticker symbol
        exch_symbol: Exchange symbol

    Returns:
        Dataset as a Pandas DataFrame
    """
    return get('securities',
               identifier=_upper_optional(identifier),
               query=query,
               exch_symbol=_upper_optional(exch_symbol))


def indices(identifier=None, query=None, type=None):
    """
    Get indices with optional filtering using parameters.

    Args:
        identifier: Intrinio symbol associated with the index
        query: Search of index name or symbol
        type: Type of indices: stock_market | economic | sic

    Returns:
        Dataset as a Pandas DataFrame
    """
    return get('indices',
               identifier=_upper_optional(identifier),
               query=query,
               type=_lower_optional(type))


def prices(identifier, start_date=None, end_date=None, frequency='daily',
           sort_order='desc'):
    """
    Get historical stock market prices or indices.

    Args:
        identifier: Stock market symbol or index
        start_date: Start date of prices (default no filter)
        end_date: Last date (default today)
        frequency: Frequency of prices: daily (default) | weekly | monthly |
            quarterly | yearly
        sort_order: Order of prices: asc | desc (default)

    Returns:
        Dataset as a Pandas DataFrame
    """
    df = get('prices',
             identifier=identifier.upper(),
             start_date=start_date,
             end_date=end_date,
             frequency=frequency.lower(),
             sort_order=sort_order.lower())

    df.index = pd.DatetimeIndex(df.date)
    df.drop('date', axis=1, inplace=True)
    return df


def news(identifier):
    """
    Get news for a company.

    Args:
        identifier: stock market ticker symbol associated with the company's
            common stock. If the company is foreign, use the stock exchange
            code, followed by a colon, then the ticker.

    Returns:
        Dataset as a Pandas DataFrame
    """
    return get('news', identifier=identifier.upper())


def fundamentals(identifier, type='FY', statement='calculations'):
    """
    Get available periods with standardized fundamental data for a company.

    Args:
        identifier: stock market ticker symbol associated with the company's
            common stock. If the company is foreign, use the stock exchange
            code, followed by a colon, then the ticker.
        type: Period type: FY (default) | QTR | TTM | YTD
        statement: Type of fundamental data: calculations (default) |
            income_statement | balance_sheet | cash_flow_statement

    Returns:
        Dataset as a Pandas DataFrame
    """
    return get('fundamentals/standardized',
               identifier=identifier.upper(),
               statement=statement.lower(),
               type=type.upper())


def financials(identifier, type='FY', statement='calculations'):
    """
    Get standardized fundamental data for a company.

    Args:
        identifier: stock market ticker symbol associated with the company's
            common stock. If the company is foreign, use the stock exchange
            code, followed by a colon, then the ticker.
        type: Period type: FY (default) | QTR | TTM | YTD
        statement: Type of fundamental data: calculations (default) |
            income_statement | balance_sheet | cash_flow_statement

    Returns:
        Dataset as a Pandas DataFrame
    """
    identifier = identifier.upper()
    type = type.upper()
    statement = statement.lower()

    f = fundamentals(identifier, type, statement)
    years_and_periods = zip(f.fiscal_year, f.fiscal_period)
    r = None

    for fiscal_year, fiscal_period in years_and_periods:
        period = financials_period(identifier, fiscal_year, fiscal_period,
                                   statement)

        if type == 'TTM' and fiscal_period == 'FY':
            period.index = pd.MultiIndex.from_tuples([(fiscal_year, 'Q4TTM')],
                                                     names=['year', 'period'])
        if r is None:
            r = period
        else:
            r = pd.concat([r, period])

    r = r.sort_index()
    return r


def financials_period(identifier, fiscal_year, fiscal_period='FY',
                      statement='calculations'):
    """
    Get standardized fundamental data for a single period for a company.

    Args:
        fiscal_year: Year
        fiscal_period: FY (default) | Q1 | Q2 | Q3 | Q4 | Q1TTM | Q2TTM | Q3TTM
            | Q2YTD | Q3YTD
        identifier: stock market ticker symbol associated with the company's
            common stock. If the company is foreign, use the stock exchange
            code, followed by a colon, then the ticker.
        statement: Type of fundamental data: calculations (default) |
            income_statement | balance_sheet | cash_flow_statement

    Returns:
        Dataset as a Pandas DataFrame
    """
    identifier = identifier.upper()
    fiscal_period = fiscal_period.upper()
    statement = statement.lower()

    if isinstance(fiscal_year, np.generic):
        fiscal_year = np.asscalar(fiscal_year)

    if fiscal_period == 'FY':
        index = [fiscal_year]
    else:
        index = pd.MultiIndex.from_tuples([(fiscal_year, fiscal_period)],
                                          names=['year', 'period'])

    r = get('financials/standardized',
            identifier=identifier,
            statement=statement,
            fiscal_year=fiscal_year,
            fiscal_period=fiscal_period)

    r = pd.DataFrame(dict(zip(r.tag, r.value)), columns=r.tag, index=index)
    r.columns.name = None
    r = r.apply(pd.to_numeric, errors='coerce')

    if fiscal_period == 'FY':
        r.index.name = 'year'

    return r


def screener(conditions, order_column=None, order_direction=None,
             primary_only=None, logic=None):
    """
    Find securities that meet a list of conditions.

    Args:
        conditions: Comma-separated list of conditions. Each condition
            consists of three or four elements separated by tildes (~):
            Data_tag~Operator~Value~Label(Optional)
        order_column: A data tag by which to order the results
        order_direction: Order of the results: asc (default) | desc
        primary_only: Return only primary securities (excluding special
            securities such as preferred shares)
        logic: How the conditions are applied using AND by default

    Returns:
        List of tickers that meet the conditions as a Pandas DataFrame
    """
    return get('securities/search',
               conditions=conditions,
               order_column=order_column,
               order_direction=order_direction,
               primary_only=primary_only,
               logic=logic)


def _lower_optional(x):
    if x is not None:
        return x.lower()
    else:
        return None


def _upper_optional(x):
    if x is not None:
        return x.upper()
    else:
        return None
