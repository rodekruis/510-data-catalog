from azure.storage.filedatalake import DataLakeServiceClient
from ckan.common import config, _
import ckan.logic as logic

import logging
log = logging.getLogger(__name__)

NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
ValidationError = logic.ValidationError

ITEMS_PER_PAGE = 3


class DataLakeHandler:
    def __init__(self):
        '''Initalize the class with the account name and key for the data
        azure storage
        '''
        self.service_client = ''
        self.storage_account_name = config.get('ckan.datalake_account_name')
        self.storage_account_key = config.get('ckan.datalake_account_key')

    def initialize_storage_account(self):
        '''Get the azure storage account service client using account details
        '''
        try:
            service_client = DataLakeServiceClient(
                account_url="{}://{}.dfs.core.windows.net".format(
                            "https", self.storage_account_name),
                credential=self.storage_account_key)
            self.service_client = service_client
        except Exception as e:
            print(e)

    def list_file_system(self, page_num):
        '''Get the File System/Containers List
        '''
        try:
            file_system = self.service_client.\
                                    list_file_systems(include_metadata=True)
            containers = []
            for data in file_system:
                containers.append({'name': data.name})
            return containers
        except Exception as e:
            log.error(e)
            raise e

    def list_directory_contents(self, container, user_path=None, page_num=None, records_per_page=None):
        '''Fetch the content of container or path
        '''
        # List of directories and their path will be stored.
        # log.info({"container": container, "path": user_path, "page_num": page_num, "records": records_per_page})
        directory_structure = []
        total_records = 0
        try:
            file_system_client = self.service_client.\
                get_file_system_client(file_system=container)
            paths = list(file_system_client.get_paths(path=user_path, recursive=False))
            total_records = len(paths)
            # Logic for previous path
            if not user_path or user_path == '':
                prev_path = "container"
            else:
                prev_path_list = user_path.rsplit('/', 1)
                if len(prev_path_list) > 1:
                    prev_path = prev_path_list[0]
                else:
                    prev_path = ""
            
            if page_num and records_per_page:
                page_num -= 1
                start_index = page_num * records_per_page
                end_index = page_num * records_per_page + records_per_page
                end_index = end_index if end_index < total_records else total_records
                paths = paths[start_index: end_index]
            for path in paths:
                path_type = 'file'
                if path.is_directory:
                    # Change path type to 'directory' when it is directory.
                    path_type = 'directory'
                directory_structure.append({'path': path.name,
                                            'type': path_type,
                                            'name': path.name.split('/')[-1]})
            return {
                'container': container,
                'directory_structure': directory_structure,
                'prev_path': prev_path,
                'total_records': total_records
                }
        except Exception as e:
            log.error(e)
            raise e

    def get_no_of_files(self, container, user_path=None):
        '''Calculate no of files in the given path
        '''
        count = 0
        try:
            file_system_client = self.service_client.\
                get_file_system_client(file_system=container)
            paths = file_system_client.get_paths(path=user_path,
                                                 recursive=True)
            for data in paths:
                if not data.is_directory:
                    # No of files only for not directory
                    count += 1
            return count
        except Exception as e:
            log.error(e)
            raise e
