import json

from azure.storage.filedatalake import DataLakeServiceClient, FileSystemClient, PathProperties
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
    def test_list_file_system(self, page_num):
        expected_values = [{'name': 'container1'}, {'name': 'container2'}]
        mock_method = ('azure.storage.filedatalake.DataLakeServiceClient.list_file_systems')
        mock_access_method = ('azure.storage.filedatalake.DataLakeServiceClient.check_container_access')
        with mock.patch(mock_method) as r:
            a = Object()
            a.name = 'container1'
            b = Object()
            b.name = 'container2'
            r.return_value = [a, b]
            with mock.patch(mock_access_method) as s:
                s.return_value = True
                handler = DataLakeHandler()
                handler.initialize_storage_account()
                containers = handler.list_file_system(page_num)
                assert containers == expected_values
    
    @pytest.mark.parametrize('container', ['container'])
    def test_list_directory_contents(self, container, user_path=None, page_num=None, records_per_page=None):
        expected_values = {'container': 'container', 'directory_structure': [{'format': 'text/plain', 'name': 'bar.txt', 'path': '/bar.txt', 'type': 'file'}, {'format': 'application/pdf', 'name': 'foo.pdf', 'path': '/foo.pdf', 'type': 'file'}], 'prev_path': 'container', 'total_records': 2}
        mock_method = ('azure.storage.filedatalake.DataLakeServiceClient.get_file_system_client')
        with mock.patch(mock_method) as r:
            file_system_client = Object()
            path_properties_1 = Object()
            path_properties_1.name = "/bar.txt"
            path_properties_1.is_directory = False
            path_properties_2 = Object()
            path_properties_2.name = "/foo.pdf"
            path_properties_2.is_directory = False
            file_system_client.get_paths = lambda path, recursive: [path_properties_1, path_properties_2]
            r.return_value = file_system_client
            handler = DataLakeHandler()
            handler.initialize_storage_account()
            directory_contents = handler.list_directory_contents(container, user_path, page_num, records_per_page)
            assert directory_contents == expected_values

    @pytest.mark.parametrize('container', ['container'])
    def test_get_no_of_files(self, container, user_path=None):
        expected_values = 1
        mock_method = ('azure.storage.filedatalake.DataLakeServiceClient.get_file_system_client')
        with mock.patch(mock_method) as r:
            file_system_client = Object()
            path_properties_1 = Object()
            path_properties_1.name = "/bar.txt"
            path_properties_1.is_directory = False
            path_properties_2 = Object()
            path_properties_2.name = "/foo"
            path_properties_2.is_directory = True
            file_system_client.get_paths = lambda path, recursive: [path_properties_1, path_properties_2]
            r.return_value = file_system_client
            handler = DataLakeHandler()
            handler.initialize_storage_account()
            file_count = handler.get_no_of_files(container, user_path)
            assert file_count == expected_values

    @pytest.mark.parametrize('container', ['container'])
    @pytest.mark.parametrize('query', ['foo'])
    @pytest.mark.parametrize('page_num', [1])
    @pytest.mark.parametrize('records_per_page', [5])
    def test_get_search_results(self, container, query, page_num, records_per_page):
        expected_values = {'search_results': [{'path': '/foo.pdf', 'type': 'file', 'name': 'foo.pdf', 'format': 'application/pdf'}], 'total_results': 1}
        mock_method = ('azure.storage.filedatalake.DataLakeServiceClient.get_file_system_client')
        with mock.patch(mock_method) as r:
            file_system_client = Object()
            path_properties_1 = Object()
            path_properties_1.name = "/bar.txt"
            path_properties_1.is_directory = False
            path_properties_2 = Object()
            path_properties_2.name = "/foo.pdf"
            path_properties_2.is_directory = False
            file_system_client.get_paths = lambda path, recursive: [path_properties_1, path_properties_2]
            r.return_value = file_system_client
            handler = DataLakeHandler()
            handler.initialize_storage_account()
            search_results = handler.get_search_results(container, query, page_num, records_per_page)
            assert search_results == expected_values
        