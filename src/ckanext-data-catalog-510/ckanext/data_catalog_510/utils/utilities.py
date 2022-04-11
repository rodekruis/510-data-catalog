import os
import json
import requests

import logging

from sqlalchemy import true
log = logging.getLogger(__name__)
HERE = os.path.dirname(__file__)

def endsWith(string: str, suffix_list: list):
    for suffix in suffix_list:
        if string.endswith(suffix):
            return True
    return False


def startsWith(string: str, prefix_list: list):
    for prefix in prefix_list:
        if string.startswith(prefix):
            return True
    return False


def get_file_format(file_path: str):
    '''
    Utility used to detect format of a file located at the path provided.
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


def get_db_access_token(endpoint, request_data):
    try:
        log.info([type(endpoint), type(request_data)])
        resp = requests.post(endpoint, request_data)
        resp_data = resp.json()
        if resp_data:
            access_token = resp_data['access_token']
            log.info(access_token)
            if access_token:
                return access_token
    except Exception as e:
        log.error(e, exc_info=true)
