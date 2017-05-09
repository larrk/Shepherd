''' A "wrapper" for the http://eth-x.digger.ws/ JSON API. '''

# Author: Ryan Stenmark <ryan pstenmark@gmail.com>

import requests as req
import json
from time import gmtime, strftime


def getJSON(address, timeout, headers):
    try:
        response = req.get("http://eth-x.digger.ws/api/accounts/" + address, timeout=timeout, headers=headers)
        response.raise_for_status()
