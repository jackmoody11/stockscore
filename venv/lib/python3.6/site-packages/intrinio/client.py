"""Get datasets from Intrinio API, either complete or one page at a time."""
import os
import logging
import json
import requests.sessions as sessions
import pandas as pd
import hashlib
import time
import codecs

username = os.getenv('INTRINIO_USERNAME')
password = os.getenv('INTRINIO_PASSWORD')
cache_enabled = (os.getenv('INTRINIO_CACHE', 'false') == 'true')
cache_directory = os.path.expanduser('~/.cache/intrinio')
cache_max_age = 3600 * 8

page_sizes = {
    'prices': 50000,
    'historical_data': 50000,
    'tags/standardized': 5000,
    'tags/reported': 5000,
    'tags/banks': 5000,
    'financials/standardized': 5000,
    'financials/reported': 5000,
    'financials/banks': 5000,
}

api_base_url = 'https://api.intrinio.com'
default_page_size = 250
log = logging.getLogger(__name__)


def get(endpoint, **parameters):
    """
    Get complete dataset from an endpoint using optional query parameters.

    Args:
        endpoint: Intrinio endpoint, for example: companies
        parameters: Optional query parameters

    Returns:
        Dataset as a Pandas DataFrame
    """
    page_number = 1
    dataset = pd.DataFrame()

    while True:
        page = get_page(endpoint, page_number, **parameters)
        dataset = pd.concat([dataset, page], ignore_index=True)

        if len(page) == 0 or page_number == page.total_pages:
            return dataset

        page_number += 1


def get_page(endpoint, page_number=1, page_size=None, **parameters):
    """
    Get a dataset page from an endpoint using optional query parameters.

    Args:
        endpoint: Intrinio endpoint, for example: companies
        page_number: Optional page number where 1 is the first page (default 1)
        page_size: Optional page size (default max page size for the endpoint)
        parameters: Optional query parameters

    Returns:
        Dataset page as a Pandas DataFrame with an additional total_pages
        attribute
    """
    response = _query(endpoint, page_number, page_size, **parameters)

    if 'data' in response:
        page = pd.DataFrame(response['data'])
        page.total_pages = response.get('total_pages', 1)
    else:
        page = pd.DataFrame([response])
        page.total_pages = 1

    return page


def _query(endpoint, page_number=1, page_size=None, **parameters):
    """
    Send a query request to Intrinio API for a dataset page including page
    count and other metadata using optional query parameters.

    Args:
        endpoint: Intrinio endpoint, for example: companies
        page_number: Optional page number where 1 is the first page (default 1)
        page_size: Optional page size (default max page size for the endpoint)
        parameters: Optional query parameters

    Returns:
        Intrinio endpoint response as a tree of dictionaries, values and lists
    """
    if page_size is None:
        page_size = get_page_size(endpoint)

    url = '{}/{}'.format(api_base_url, endpoint)
    parameters['page_number'] = page_number
    parameters['page_size'] = page_size

    if cache_enabled:
        response = _web_request_cached(url, parameters)
    else:
        response = _web_request(url, parameters)

    return json.loads(response)


def _web_request(url, parameters):
    """
    Perform HTTP GET request and return response.

    Args:
        url: Absolute URL
        parameters: URL parameters

    Returns:
        Response as a string
    """
    auth = (username, password)

    with sessions.Session() as session:
        response = session.request('GET', url, params=parameters, auth=auth,
                                   verify=True)
    if not response.ok:
        response.raise_for_status()

    return response.content.decode('utf-8')


def _web_request_cached(url, parameters):
    """
    Return cached response if available and not too old, otherwise
    perform HTTP GET request and cache and return response.

    Args:
        url: Absolute URL
        parameters: URL parameters

    Returns:
        Response as a string
    """
    content_id = (url + json.dumps(parameters)).encode('utf-8')
    content_key = hashlib.sha256(content_id).hexdigest()
    cache_file_path = os.path.join(cache_directory, content_key + '.txt')

    if os.path.exists(cache_file_path):
        age = time.time() - os.path.getctime(cache_file_path)

        if age <= cache_max_age:
            with codecs.open(cache_file_path, 'r', 'utf-8') as cached_response:
                return cached_response.read()

    response = _web_request(url, parameters)

    if not os.path.exists(cache_directory):
        os.makedirs(cache_directory)

    with codecs.open(cache_file_path, 'w', 'utf-8') as cached_response:
        cached_response.write(response)

    return response


def get_page_size(endpoint):
    """
    Get page size for a specific endpoint.

    Args:
        endpoint: Intrinio endpoint, for example: companies

    Returns:
        Page size as number of rows
    """
    return page_sizes.get(endpoint.lower(), default_page_size)
