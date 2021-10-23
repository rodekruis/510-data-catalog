
import requests

import logging
log = logging.getLogger(__name__)


def get_countries():
    # URL for fetching countries
    try:
        url = 'https://goadmin.ifrc.org/api/v2/country/?limit=400&offset=0'
        response = requests.get(url)
        results = response.json()['results']
        country_list = []
        for country in results:
            country_list.append({'name': country.get('name')})
        return country_list
    except Exception as e:
        return []
