import requests
import datetime
import json
import os
import logging

from ckan.lib.helpers import core_helper
from ckan.common import c, config
from ckanext.data_catalog_510.controllers.database_handler import SQLHandler
# from ckanext.data_catalog_510.logic import check_user_access
log = logging.getLogger(__name__)
HERE = os.path.dirname(__file__)

def get_countries(search):
    # log.info(HERE)
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


@core_helper
def get_db_host(res):
    '''
    Helper used to extract Database hostname from the internal connection string.
    :param res: The resource metadata that is injected into the template HTML.

    :rtype string
    '''
    try:
        host = "Unknown Host"
        db_handler = SQLHandler()
        if(res['database_connection_type']):
            db_handler.db_type = res['database_connection_type']
            host = db_handler.get_db_connection_string(res['database_connection']).split("@")[-1].split("/")[0]
        return host
    except Exception as e:
        log.error(e)
        raise e


@core_helper
def generate_sample_db_string(res):
    '''
    Helper used to generate sample DB connection string for the provided resource, if retrieved from database.
    :param res: The resource metadata that is injected into the template HTML.

    :rtype string
    '''

    host = get_db_host(res)
    db_string = "Unknown DB String"
    if res['database_connection_type'] == 'postgres':
        db_string = f"postgres://<username>:<password>@{host}/{res['database_connection']}"
    elif res['database_connection_type'] == 'mysql':
        db_string = f"mysql+pymysql://<username>:<password>@{host}/{res['database_connection']}"
    elif res['database_connection_type'] == 'azuresql':
        db_string = f"mssql+pyodbc://<username>:<password>@{host}/{res['database_connection']}?driver=ODBC+Driver+17+for+SQL+Server"
    else:
        db_string = "Unknown DB String"
    return db_string


@core_helper
def get_file_format(file_path: str):
    '''
    Helper used to detect format of a file located at the path provided.
    :param file_path: Path of the file.

    :rtype string
    '''
    extension = os.path.splitext(file_path)[1][1:]
    with open(os.path.join(HERE, 'mimetypes.json'), 'r') as format_list_file:
        format_list = json.load(format_list_file)
        if extension:
            if extension in format_list:
                return format_list[extension]
            else:
                return extension.upper()
        else:
            return None


@core_helper
def get_request_data_mailTo(package, res):
    '''
    Helper used to generate mailto string for data request of high security resources.
    :param file_path: Path of the file.

    :rtype string
    '''
    # log.info(package)
    # log.info(res)
    with open(os.path.join(HERE, 'request_data_mail.json'), 'r') as email_template:
        email_template = json.load(email_template)
        # Make sure '.' is replaced with '@@' in all email addresses to prevent spam.
        toEmail = package.get("dataset_owner_email").replace('.', '@@')
        ccEmail = email_template.get('cc').replace('.', '@@')
        resource_url = config.get('ckan_site_url') + '/dataset/' + package.get('name') + '/resource/' + res.get('id')
        subject = email_template.get('subject').format(res.get('name')).replace(" ", "%20")
        body = email_template.get('body').format(res.get('name'), package.get('name'), resource_url).replace(" ", "%20").replace("\n", "%0A")
        return f'mailto:{toEmail}?cc={ccEmail}&subject={subject}&body={body}'


@core_helper
def set_data_access(package):
    '''
    Helper used to set access level of user based on security classification.
    :param file_path: Path of the file.

    :rtype dict
    '''
    sec_class = package.get('security_classification')
    if 'private' not in package:
        package['private'] = True
    if sec_class == 'high' or sec_class == 'normal':
        if package['private'] is not True:
            package['private'] = True
    else:
        if package['private'] is not False:
            package['private'] = False
    return package


@core_helper
def is_preview_access(pkg, userobj=None):
    '''
    Helper used to check preview access of user based on security classification.
    :param file_path: Path of the file.

    :rtype bool
    '''
    sec_class = pkg.get('security_classification')
    if sec_class == 'low':
        return True
    elif userobj:
        # if sec_class == 'normal' or (sec_class == 'high' and userobj.name == pkg.get('dataset_owner')):
        if sec_class == 'normal':
            return True
    return False







