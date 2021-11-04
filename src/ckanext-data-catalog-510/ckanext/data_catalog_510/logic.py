import ckan.logic as logic
from ckan.common import g, config, _
import ckan.model as model
import ckan.plugins.toolkit as toolkit 

from ckanext.data_catalog_510.\
     controllers.database_handler import SQLHandler

from ckanext.data_catalog_510.\
     controllers.datalake_handler import DataLakeHandler

import logging
log = logging.getLogger(__name__)

NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
ValidationError = logic.ValidationError

LIST_ALL_DB = [{
   "name": "mysql",
   "title": "MYSQL"
    },
    {
    "name": "postgres",
    "title": "Postgresql"
    },
    {
    "name": "azuresql",
    "title": "Azure SQL"
    }
]

ALLOWED_DB_TYPE = ['mysql', 'postgres', 'azuresql']


def get_all_dbs(context, data_dict):
    ''' Function to return all databases
    '''
    # Validate whether user has permission to create datasets or not
    logic.check_access(u'package_create', context)
    return LIST_ALL_DB


def validate_db_connections_and_init(db_type):
    ''' Function to validate whether the connection type exists or not
    '''
    if db_type not in ALLOWED_DB_TYPE:
        # Validate that the db_type is in Allowed types
        raise ValidationError(_('Not a Valid Database Type.'))
    try:
        db_obj = SQLHandler()
        return db_obj
    except Exception as e:
        raise e


def get_db_connections(context, data_dict):
    '''Return a list of the connections strings available for the specified
    database without the actual uri of the connection strings.
    :param db_type: will be given to find the connections string
    available for the specified for the specified database type. (required).
    :type db_type: string

    :rtype: list of strings
    '''
    # Validate whether user has permission to create datasets or not
    logic.check_access(u'package_create', context)
    try:
        db_connections = []
        db_type = data_dict.get('db_type', '')
        db_obj = validate_db_connections_and_init(db_type)
        db_connections = db_obj.get_databases(db_type)
        return db_connections
    except Exception as e:
        log.error(e)
        raise e


def get_schemas(context, data_dict):
    '''Return a list of the schemas for the available DB
    :param db_name: will be given to find the the schemas given db(required).
    :type db_name: string
    :param db_type: will be given to find the connections string
    available for the specified for the specified database type. (required).
    :type db_type: string

    :rtype: list of strings
    '''
    # Validate whether user has permission to create datasets or not
    logic.check_access(u'package_create', context)
    try:
        db_name = data_dict.get('db_name', '')
        db_type = data_dict.get('db_type')
        db_obj = validate_db_connections_and_init(db_type)
        db_schema = db_obj.fetch_schema(db_type, db_name)
        return db_schema
    except Exception as e:
        log.error(e)
        raise e


def get_tables(context, data_dict):
    '''Return a list of the tables for the available Schema
    :param db_name: will be given to find the the schemas given db(required).
    :type db_name: string
    :param db_type: will be given to find the connections string
    available for the specified for the specified database type. (required).
    :type db_type: string
    :param schema: will be given to find the tables available in specific
    database (required)
    :type schema: string

    :rtype: list of strings
    '''
    # Validate whether user has permission to create datasets or not
    logic.check_access(u'package_create', context)
    try:
        db_name = data_dict.get('db_name', '')
        db_type = data_dict.get('db_type', '')
        schema = data_dict.get('schema', '')
        db_obj = validate_db_connections_and_init(db_type)
        db_tables = db_obj.fetch_tables(db_type, db_name, schema)
        return db_tables
    except Exception as e:
        log.error(e)
        raise e


def get_tables_metadata(context, data_dict):
    '''Return a dictionary of the metadata for the table specified
    :param db_name: will be given to find the the schemas given db(required).
    :type db_name: string
    :param db_type: will be given to find the connections string
    available for the specified for the specified database type. (required).
    :type db_type: string
    :param schema: will be given to find the tables available in specific
    database (required)
    :type schema: string
    :param table: will be given to find the tables metadata (required)
    :type table: string

    :rtype: dict
    '''
    # Validate whether user has permission to create datasets or not
    logic.check_access(u'package_create', context)
    try:
        db_name = data_dict.get('db_name', '')
        db_type = data_dict.get('db_type', '')
        schema = data_dict.get('schema', '')
        table = data_dict.get('table', '')
        db_obj = validate_db_connections_and_init(db_type)
        db_table_metadata = db_obj.fetch_metadata(db_type, db_name, schema, table)
        return db_table_metadata
    except Exception as e:
        log.error(e)
        raise e


def get_containers(context, data_dict):
    '''Return a list of containers for the datalake
    :rtype: list of strings
    '''
    # Validate whether user has permission to create datasets or not
    logic.check_access(u'package_create', context)
    try:
        datalake_connection = DataLakeHandler()
        datalake_connection.initialize_storage_account()
        return datalake_connection.list_file_system()
    except Exception as e:
        log.error(e)
        raise e


def get_directories_and_files(context, data_dict):
    '''Return a list of directories and files for the container or for the path
    :param container: Name of container for which files need to retrived
    (required).
    :type container: string
    :param path: will be given to fetch the files/directory in the path Instead
    of container
    :type path: string
    :rtype: list of dict
    '''
    # Validate whether user has permission to create datasets or not
    logic.check_access(u'package_create', context)
    try:
        datalake_connection = DataLakeHandler()
        datalake_connection.initialize_storage_account()
        container = data_dict.get('container', '')
        path = data_dict.get('path', '')
        return datalake_connection.list_directory_contents(container, path)
    except Exception as e:
        log.error(e)
        raise e


def get_no_of_files(context, data_dict):
    '''Return a no of files in the path
    :param container: Name of container for which files need to retrived
    (required).
    :type container: string
    :param path: will be given to fetch the files/directory in the path Instead
    of container
    :type path: string
    :rtype: number
    '''
    # Validate whether user has permission to create datasets or not
    logic.check_access(u'package_create', context)
    try:
        datalake_connection = DataLakeHandler()
        datalake_connection.initialize_storage_account()
        container = data_dict.get('container', '')
        path = data_dict.get('path', '')
        return datalake_connection.get_no_of_files(container, path)
    except Exception as e:
        log.error(e)
        raise e

@toolkit.side_effect_free
def country_autocomplete(context, data_dict):
    from ckanext.data_catalog_510.utils.helpers import get_countries
    log.info(data_dict)
    return get_countries