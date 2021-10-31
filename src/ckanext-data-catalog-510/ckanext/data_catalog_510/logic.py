import ckan.logic as logic
from ckan.common import g, config, _
import ckan.model as model

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
    logic.check_access(u'package_create', context)
    return LIST_ALL_DB


def validate_db_connections_and_init(db_type):
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
    logic.check_access(u'package_create', context)
    db_connections = []
    db_type = data_dict.get('db_type', '')
    db_obj = validate_db_connections_and_init(db_type)
    db_connections = db_obj.get_databases(db_type)
    return db_connections


def get_schemas(context, data_dict):
    '''Return a list of the schemas for the available DB
    :param db_name: will be given to find the the schemas given db(required).
    :type db_name: string
    :param db_type: will be given to find the connections string
    available for the specified for the specified database type. (required).
    :type db_type: string

    :rtype: list of strings
    '''
    logic.check_access(u'package_create', context)
    db_name = data_dict.get('db_name', '')
    db_type = data_dict.get('db_type')
    db_obj = validate_db_connections_and_init(db_type)
    db_schema = db_obj.fetch_schema(db_type, db_name)
    return db_schema


def get_tables(context, data_dict):
    logic.check_access(u'package_create', context)
    db_name = data_dict.get('db_name', '')
    db_type = data_dict.get('db_type', '')
    schema = data_dict.get('schema', '')
    db_obj = validate_db_connections_and_init(db_type)
    db_tables = db_obj.fetch_tables(db_type, db_name, schema)
    return db_tables


def get_tables_metadata(context, data_dict):
    logic.check_access(u'package_create', context)
    db_name = data_dict.get('db_name', '')
    db_type = data_dict.get('db_type', '')
    schema = data_dict.get('schema', '')
    table = data_dict.get('table', '')
    db_obj = validate_db_connections_and_init(db_type)
    db_table_metadata = db_obj.fetch_metadata(db_type, db_name, schema, table)
    return db_table_metadata


def get_containers(context, data_dict):
    logic.check_access(u'package_create', context)
    datalake_connection = DataLakeHandler()
    datalake_connection.initialize_storage_account()
    return datalake_connection.list_file_system()


def get_directories_and_files(context, data_dict):
    logic.check_access(u'package_create', context)
    datalake_connection = DataLakeHandler()
    datalake_connection.initialize_storage_account()
    container = data_dict.get('container', '')
    path = data_dict.get('path', '')
    return datalake_connection.list_directory_contents(container, path)


def get_no_of_files(context, data_dict):
    logic.check_access(u'package_create', context)
    datalake_connection = DataLakeHandler()
    datalake_connection.initialize_storage_account()
    container = data_dict.get('container', '')
    path = data_dict.get('path', '')
    return datalake_connection.get_no_of_files(container, path)
