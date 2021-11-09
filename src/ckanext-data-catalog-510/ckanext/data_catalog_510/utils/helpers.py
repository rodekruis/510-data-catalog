import requests
import datetime
import json
import os
import logging

from ckan.lib.helpers import core_helper
from ckan.common import c, config

log = logging.getLogger(__name__)
HERE = os.path.dirname(__file__)

def get_countries(search):
    log.info(HERE)
    with open(os.path.join(HERE, 'country.json'),'r') as f:
        license_data = json.load(f)
        license_data = list(map(lambda x:x['name'],license_data))
        country_list = list(filter(lambda k: search.lower() in k.lower(), license_data))
    return country_list

@core_helper
def prefill_dataset_owner_details(data, call_type):
    '''Helper used to prefill the dataset owner and data owner email on the
    database basis of call_type
    :param data: if the value is already present e.g. in case of edit
    string.
    :param call_type: to check if need to fetch name or email.
    string().

    :rtype: string
    '''
    if data:
        return data
    else:
        if c.userobj and call_type == 'name':
            return c.userobj.display_name
        if c.userobj and call_type == 'email':
            return c.userobj.email


@core_helper
def get_current_date(data):
    '''Helper used to get the current date in the format 'yyyy-mm-dd'
    :param data: if the value is already present e.g. in case of edit
    string.

    :rtype: string
    '''
    try:
        format = "%Y-%m-%d"
        if data:
            return data
        else:
            return datetime.datetime.today().strftime(format)
    except Exception as e:
        log.error(e)
        raise e


@core_helper
def get_storage_explorer_link(container):
    '''Helper used to return the azure storage explorer URL so that container
    can be opened directly in storage explorer application.
    :param container: The name of container which need to be opened 
    string.

    :rtype: string
    '''
    if container:
        subscription_id = config.get('ckan.azure_subscription_id')
        datalake_account_name = config.get('ckan.datalake_account_name')
        resource_group_name = config.get('ckan.azure_resource_group_name')
        storage_link = f"storageexplorer://v=1&accountid=/subscriptions/{subscription_id}/resourceGroups/{resource_group_name}/providers/Microsoft.Storage/storageAccounts/{datalake_account_name}&subscriptionid={subscription_id}&resourcetype=Azure.BlobContainer&resourcename={container}"
        return storage_link
    return None
