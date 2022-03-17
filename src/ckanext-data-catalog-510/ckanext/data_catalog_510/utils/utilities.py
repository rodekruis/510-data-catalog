import os
import json

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
