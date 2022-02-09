# encoding: utf-8

import json

import pytest
import unittest.mock as mock
import ckan.logic as logic

from ckan.tests import helpers
from ckanext.data_catalog_510.\
    controllers.database_handler import SQLHandler
import ckanext.data_catalog_510.logic as dataCatalogLogic

postgres_env = json.dumps([
    {
        "name": "ckan",
        "title": "Test",
        "url": "postgresql://ckan:ckan@db/ckan"
    }
])
mysql_env = json.dumps([
    {
        "name": "ckan-test",
        "title": "Test",
        "url": "mysql+pymysql://test:test@mysql/ckan-test"
    }
])
azuresql_env = json.dumps([
    {
        "name": "ckan-test",
        "title": "Test",
        "url": ""
    }
])


@pytest.mark.ckan_config("ckan.postgresql_db_connections", postgres_env)
@pytest.mark.ckan_config("ckan.mysql_db_connections", mysql_env)
@pytest.mark.ckan_config("ckan.azuresql_db_connections", azuresql_env)
@pytest.mark.ckan_config("ckan.plugins", "data_catalog_510")
@pytest.mark.usefixtures("with_plugins")
class TestDatabasesConnectionAction:

    def setup(self):
        self.db_handler = SQLHandler()

    def test_get_db_connections_not_found(self):
        '''Test for validating connection type which is not supported'''
        with pytest.raises(logic.ValidationError):
            helpers.call_action(
                "get_db_connections",
                {},
                db_type="test",
            )

    def test_get_db_connections_postgres(self):
        '''Test for validating postgres connection type'''
        expected_res = [{'name': 'ckan', 'title': 'Test'}]
        get_dbs = helpers.call_action(
            "get_db_connections",
            {},
            db_type="postgres",
        )
        # Validating the connection action response
        # log.info(get_dbs)
        assert expected_res == get_dbs

    def test_get_db_connections_mysql(self):
        '''Test for validating mysql connection type'''
        expected_res = [{'name': 'ckan-test', 'title': 'Test'}]
        get_dbs = helpers.call_action(
            "get_db_connections",
            {},
            db_type="mysql",
        )
        # Validating the connection action response
        # log.info(get_dbs)
        assert expected_res == get_dbs

    def test_get_db_connections_azuresql(self):
        '''Test for validating azuresql connection type'''
        expected_res = [{'name': '', 'title': 'Test'}]
        get_dbs = helpers.call_action(
            "get_db_connections",
            {},
            db_type="azuresql",
        )
        # Validating the connection action response
        # log.info(get_dbs)
        assert expected_res == get_dbs

    def test_get_schema_for_mysql(self):
        expected_value = ['test']
        mock_method = ('ckanext.data_catalog_510.controllers'
                       '.database_handler.SQLHandler.fetch_schema')
        with mock.patch(mock_method) as r:
            r.return_value = ['test']
            get_dbs = helpers.call_action(
                "get_schemas",
                {},
                db_type="mysql",
            )
        # Validating the get_schema
        assert get_dbs == expected_value

    def test_get_schema_for_postgres(self):
        expected_value = ['public', 'test']
        mock_method = ('ckanext.data_catalog_510.controllers'
                       '.database_handler.SQLHandler.fetch_schema')
        with mock.patch(mock_method) as r:
            r.return_value = ['public', 'test']
            get_dbs = helpers.call_action(
                "get_schemas",
                {},
                db_type="postgres",
            )
        # Validating the get_schema
        assert get_dbs == expected_value

    def test_get_schema_for_azuresql(self):
        expected_value = ['Forecast', 'test']
        mock_method = ('ckanext.data_catalog_510.controllers'
                       '.database_handler.SQLHandler.fetch_schema')
        with mock.patch(mock_method) as r:
            r.return_value = ['Forecast', 'test']
            get_dbs = helpers.call_action(
                "get_schemas",
                {},
                db_type="azuresql",
            )
        # Validating the get_schema
        assert get_dbs == expected_value

    def test_get_tables_for_postgres(self):
        expected_value = ['rating', 'activity']
        mock_method = ('ckanext.data_catalog_510.controllers'
                       '.database_handler.SQLHandler.fetch_tables')
        with mock.patch(mock_method) as r:
            r.return_value = ['rating', 'activity']
            get_dbs = helpers.call_action(
                "get_tables",
                {},
                db_type="postgres",
            )
        # Validating the get_tables
        assert get_dbs == expected_value

    def test_get_tables_for_mysql(self):
        expected_value = ['rating', 'activity']
        mock_method = ('ckanext.data_catalog_510.controllers'
                       '.database_handler.SQLHandler.fetch_tables')
        with mock.patch(mock_method) as r:
            r.return_value = ['rating', 'activity']
            get_dbs = helpers.call_action(
                "get_tables",
                {},
                db_type="mysql",
            )
        # Validating the get_tables
        assert get_dbs == expected_value

    def test_get_tables_for_azuresql(self):
        expected_value = ['projects']
        mock_method = ('ckanext.data_catalog_510.controllers'
                       '.database_handler.SQLHandler.fetch_tables')
        with mock.patch(mock_method) as r:
            r.return_value = ['projects']
            get_dbs = helpers.call_action(
                "get_tables",
                {},
                db_type="mysql",
            )
        # Validating the get_tables
        assert get_dbs == expected_value

    def test_get_metadata_for_postgres(self):
        # Todo
        pass

    def test_get_metadata_for_mysql(self):
        # Todo
        pass

    def test_get_containers(self):
        ''' Test for get the files from container'''

        expected_value = [{"name": 'test'}]

        mock_method = ('ckanext.data_catalog_510.controllers'
                       '.datalake_handler.DataLakeHandler.list_file_system')
        with mock.patch(mock_method) as r:
            r.return_value = [{'name': 'test'}]
            context = {}
            context.setdefault("user", "")
            context.setdefault("ignore_auth", True)
            get_list = helpers.call_action("get_containers", {})

            # Validating the get_containers
            assert get_list == expected_value

    def test_get_containers_with_exception(self):
        ''' Test to get containers information with exception '''

        mock_method = ('ckanext.data_catalog_510.controllers'
                       '.datalake_handler.DataLakeHandler.list_file_system')
        with mock.patch(mock_method, side_effect=Exception("Mock Containers Exception")) as r:
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

        with mock.patch(mock_method, side_effect=Exception("Mock Directories Exception")) as r:
            with pytest.raises(Exception) as excinfo:
                helpers.call_action("get_directories_and_files", {})

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

        with mock.patch(mock_method, side_effect=Exception("Mock No Of Files Exception")) as r:
            with pytest.raises(Exception) as excinfo:
                helpers.call_action("get_no_of_files", {})

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

        with mock.patch(mock_method, side_effect=Exception("Mock Geo Metadata Exception")) as r:
            with pytest.raises(Exception) as excinfo:
                helpers.call_action("get_geo_metadata", {})

            assert str(excinfo.value) == 'Mock Geo Metadata Exception'

    @pytest.mark.parametrize("text_input", [
        [{"name": "mysql", "title": "MYSQL"},
         {"name": "postgres", "title": "Postgresql"},
         {"name": "azuresql", "title": "Azure SQL"}
         ]
    ])
    def test_get_all_dbs(self, text_input):

        res = helpers.call_action("get_all_dbs", {})
        assert(text_input == res)

    def test_validate_db_connections_and_init_with_db_exception(self):

        with pytest.raises(Exception) as excinfo:
            dataCatalogLogic.validate_db_connections_and_init('oracle')

    def test_validate_db_connections_and_init_with_exception(self):

        with pytest.raises(Exception) as excinfo:
            dataCatalogLogic.validate_db_connections_and_init()
