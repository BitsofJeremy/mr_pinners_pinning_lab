# pinning_lab/utils/__init__.py

# Some nice utilities for the web app

import requests

import logging
logger = logging.getLogger(__name__)


def ada_usd():
    """ GET ADA/USD Price """
    url = 'https://api.coingecko.com/api/v3/simple/price' \
          '?ids=cardano&vs_currencies=usd&include_market_cap=true' \
          '&include_24hr_vol=true&include_24hr_change=true'
    headers = {'accept': 'application/json'}
    response = requests.get(url, headers=headers)
    quote = response.json()
    logger.info(f"ADA/USD Price Quote: {quote}")
    return quote


