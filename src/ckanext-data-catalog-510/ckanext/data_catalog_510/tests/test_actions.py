# encoding: utf-8

import json

import pytest
import unittest.mock as mock
import ckan.logic as logic

from ckan.tests import helpers
from ckanext.data_catalog_510.\
     controllers.database_handler import SQLHandler

postgres_env = json.dumps([
  {
    "name": "test",
    "title": "Test",
    "url": "postgresql://ckan:ckan@db/ckan"
  }
])
mysql_env = json.dumps([
  {
    "name": "test",
    "title": "Test",
    "url": "mysql+pymysql://test:test@mysql/test"
  }
])


@pytest.mark.ckan_config("ckan.postgresql_db_connections", postgres_env)
@pytest.mark.ckan_config("ckan.mysql_db_connections", mysql_env)
@pytest.mark.ckan_config("ckan.plugins", "data_catalog_510")
@pytest.mark.usefixtures("clean_db", "with_plugins")
class TestDatabasesConnectionAction:

    def setup(self):
        self.SQLHandler = SQLHandler()

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
        expected_res = [{'name': 'test', 'title': 'Test'}]
        get_dbs = helpers.call_action(
            "get_db_connections",
            {},
            db_type="postgres",
        )
        # Validating the connection action response
        assert expected_res == get_dbs

    def test_get_db_connections_mysql(self):
        '''Test for validating mysql connection type'''
        expected_res = [{'name': 'test', 'title': 'Test'}]
        get_dbs = helpers.call_action(
            "get_db_connections",
            {},
            db_type="mysql",
        )
        # Validating the connection action response
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
        # Validating the get_schema
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
        # Validating the get_schema
        assert get_dbs == expected_value

    def test_get_metadata_for_postgres(self):
        # Todo
        pass

    def test_get_metadata_for_mysql(self):
        # Todo
        pass
