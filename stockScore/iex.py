from iexfinance import Stock
import os
import multiprocessing


def batch_get(batch_list, func, output_format, **kwargs):
    """
    Note: This function is only intended to be used for get_iex_response() function in start module,
    but SHOULD NOT be embedded into get_iex_response to avoid pickling problems.
    :param batch_list: List of tickers
    :param func: Name of iexfinance function to be applied
    :param output_format: choose pandas or json (if pandas not available, will default to json)
    :return: all the data necessary to make multiple iexfinance function calls at once
    """
    f = func
    response = Stock(batch_list, output_format=output_format).f(**kwargs)
    return response


def get_iex_response(batch_list, func, output_format, num_processes=os.cpu_count(), **kwargs):

    """
    :param batch_list: List of symbols -- use get_symbols() and list_split()
    functions to set batch_list
    :param func: name of iexfinance function you want to perform on
    :param output_format: choose pandas or json (if pandas not available, will default to json)
    :param num_processes: Defaults to # of computer cores, but it is possible to have more.
    Increase this as your computer capacity allows for faster multiprocessing.
    :return: Returns all batch GET requests from API for given url_end.
    """
    pool = multiprocessing.Pool(processes=num_processes)
    outputs = []
    outputs.append(pool.starmap(Stock(), [[batch_list, func, output_format, kwargs] for batch in batch_list]))
    pool.close()
    pool.join()
    return outputs


def list_split(symbols, n=100):
    """
    :param symbols: give list of symbols
    :param n: number of symbols per
    :return: returns list of lists (broken into groups of 100 or some remainder by default)
    """
    list_batches = [symbols[i:i+n] for i in range(0, len(symbols), n)]
    return list_batches
