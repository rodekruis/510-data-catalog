
import requests
import datetime

from ckan.lib.helpers import core_helper
from ckan.common import c

import logging
log = logging.getLogger(__name__)


def get_countries():
    try:
        # URL for fetching countries
        url = 'https://goadmin.ifrc.org/api/v2/country/?limit=400&offset=0'
        response = requests.get(url)
        results = response.json()['results']
        country_list = []
        for country in results:
            country_list.append({'name': country.get('name')})
        return country_list
    except Exception as e:
        log.error(e)
        return []


@core_helper
def prefill_dataset_owner_details(data, call_type):
    if data:
        return data
    else:
        if c.userobj and call_type == 'name':
            return c.userobj.display_name
        if c.userobj and call_type == 'email':
            return c.userobj.email


@core_helper
def get_current_date(data):
    format = "%Y-%m-%d"
    if data:
        return data
    else:
        return datetime.datetime.today().strftime(format)
