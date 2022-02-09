import json

from azure.storage.filedatalake import DataLakeServiceClient
import pytest
import unittest.mock as mock
import ckan.logic as logic
from ckanext.data_catalog_510.\
    controllers.datalake_handler import DataLakeHandler

from ckan.tests import helpers


class Object(object):
    pass


@pytest.mark.ckan_config("ckan.plugins", "data_catalog_510")
@pytest.mark.usefixtures("with_plugins")
class TestDataLakeHandler:
    @pytest.mark.parametrize('page_num', [1])
    def test_get_container_list(self, page_num):
        expected_values = [{'name': 'container1'}, {'name': 'container2'}]
        mock_method = ('azure.storage.filedatalake.DataLakeServiceClient.list_file_systems')
        with mock.patch(mock_method) as r:
            a = Object()
            a.name = 'container1'
            b = Object()
            b.name = 'container2'
            r.return_value = [a, b]
            handler = DataLakeHandler()
            handler.initialize_storage_account()
            containers = handler.list_file_system(page_num)
            assert containers == expected_values
    
    # def test_list_directory_contents(self, container, user_path=None, page_num=None, records_per_page=None):
    #     expected_values = []
    #     mock_method = ('azure.storage.filedatalake.DataLakeServiceClient.get_file_system_client')
    #     with mock.patch(mock_method) as r:
    #         file_object = Object()
    #         file_object.is_directory = False
            
    #         file_system_client = Object()
    #         file_system_client.get_paths = lambda path, recursive=False : return [{}]
