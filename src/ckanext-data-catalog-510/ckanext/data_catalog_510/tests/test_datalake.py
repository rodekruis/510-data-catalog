# encoding: utf-8
'''Tests for the ckanext.data_catalog_510 extension.

'''
import pytest
import unittest.mock as mock
from ckan.common import config, _
from ckan.tests import helpers
from ckanext.data_catalog_510.\
    controllers.datalake_handler import DataLakeHandler
# import logging
# log = logging.getLogger(__name__)


class TestDataLakeAction(object):

    def setup(self):
        self.DataLakeHandler = DataLakeHandler()

    def test_get_containers(self):
        ''' Test for get the files from container'''

        expected_value = [{"name": 'test'}]

        mock_method = ('ckanext.data_catalog_510.controllers'
                       '.datalake_handler.DataLakeHandler.list_file_system')
        with mock.patch(mock_method) as r:
            r.return_value = [{'name': 'test'}]
            get_list = helpers.call_action(
                "get_containers",
                {}
            )

            # Validating the get_containers
            assert get_list == expected_value
            
    def test_get_containers_with_exception(self):
        ''' Test to get containers information with exception '''
        
        mock_method = ('ckanext.data_catalog_510.controllers'
                       '.datalake_handler.DataLakeHandler.list_file_system')
        with mock.patch(mock_method,side_effect=Exception("Mock Containers Exception")) as r:
            with pytest.raises(Exception) as excinfo:
                get_list = helpers.call_action(
                "get_containers",
                {}
            )
                
            assert str(excinfo.value) == 'Mock Containers Exception'
        

    def test_get_directories_and_files(self):
        ''' Test for get the directories and files '''

        expected_value = {"container": "geodata", "directory_structure": [
            {"path": "geojson", "type": "directory",
                "name": "geojson", "format": "application/geo+json"},
        ],
            "prev_path": "container", "total_records": "3"
        }

        mock_method = ('ckanext.data_catalog_510.controllers'
                       '.datalake_handler.DataLakeHandler.list_directory_contents')

        with mock.patch(mock_method) as r:
            r.return_value = {"container": "geodata", "directory_structure": [
                {"path": "geojson", "type": "directory",
                    "name": "geojson", "format": "application/geo+json"},
            ],
                "prev_path": "container", "total_records": "3"
            }
            get_dir_contents = helpers.call_action(
                "get_directories_and_files", {}
            )

            # log.info(get_dir_contents)

            # Validating the get_directories_and_files
            assert get_dir_contents == expected_value
            
    def test_get_directories_and_files_with_exception(self):
        ''' Test to catch the exception for directories and files '''
        mock_method = ('ckanext.data_catalog_510.controllers'
                       '.datalake_handler.DataLakeHandler.list_directory_contents')
        
        with mock.patch(mock_method,side_effect=Exception("Mock Directories Exception")) as r:
            with pytest.raises(Exception) as excinfo:
                helpers.call_action("get_directories_and_files",{})
                
            assert str(excinfo.value) == 'Mock Directories Exception'

    def test_get_no_of_files(self):
        ''' Test to get the no of files'''
        
        expected_result = 10

        mock_method = ('ckanext.data_catalog_510.controllers'
                       '.datalake_handler.DataLakeHandler.get_no_of_files')

        with mock.patch(mock_method) as r:
            r.return_value = 10
            fetch_no_of_files = helpers.call_action("get_no_of_files", {})

            # Validating the get_no_of_files
            assert fetch_no_of_files == expected_result
            
    def test_get_no_of_files_with_exception(self):
        ''' Test to catch the exception for no of files '''
        
        mock_method = ('ckanext.data_catalog_510.controllers'
                       '.datalake_handler.DataLakeHandler.get_no_of_files')
        
        with mock.patch(mock_method,side_effect=Exception("Mock No Of Files Exception")) as r:
            with pytest.raises(Exception) as excinfo:
                helpers.call_action("get_no_of_files",{})
                
            assert str(excinfo.value) == 'Mock No Of Files Exception'

    def test_get_geo_metadata(self):
        ''' Test to get the geo metadata information'''

        expected_result = {"spatial_extent": [24.72, 21.99, 36.89, 31.65],
                           "spatial_reference_system": "4326",
                           "spatial_resolution": "0.002"}

        mock_method = ('ckanext.data_catalog_510.controllers'
                       '.datalake_handler.DataLakeHandler.get_geo_metadata')

        with mock.patch(mock_method) as r:
            r.return_value = {"spatial_extent": [24.72, 21.99, 36.89, 31.65],
                              "spatial_reference_system": "4326",
                              "spatial_resolution": "0.002"}

            fetch_geo_metadata = helpers.call_action("get_geo_metadata", {})

            # Validating the get_geo_metadata
            assert fetch_geo_metadata == expected_result
            
    
    def test_get_geo_metadata_with_exception(self):
        ''' Test to check the exception for geo metadata'''
        
        mock_method = ('ckanext.data_catalog_510.controllers'
                       '.datalake_handler.DataLakeHandler.get_geo_metadata')
        
        with mock.patch(mock_method,side_effect=Exception("Mock Geo Metadata Exception")) as r:
            with pytest.raises(Exception) as excinfo:
                helpers.call_action("get_geo_metadata",{})
                
            assert str(excinfo.value) == 'Mock Geo Metadata Exception'
        
