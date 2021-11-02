
import requests
import datetime

from ckan.lib.helpers import core_helper
from ckan.common import c, config

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


@core_helper
def get_storage_explorer_link(container):
    subscription_id = config.get('ckan.azure_subscription_id')
    datalake_account_name = config.get('ckan.datalake_account_name')
    resource_group_name = config.get('ckan.azure_resource_group_name')
    storage_link = f"storageexplorer://v=1&accountid=/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Storage/storageAccounts/{datalake_account_name}&subscriptionid={subscription_id}&resourcetype=Azure.BlobContainer&resourcename={container}"
    return storage_link
