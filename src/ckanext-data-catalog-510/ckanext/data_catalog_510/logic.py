import json
import ckan.logic as logic
from ckan.common import g, config, _
import ckan.model as model
import ckan.plugins.toolkit as toolkit 
import base64

from ast import literal_eval as make_list
from ckanext.data_catalog_510.utils.helpers import set_data_access, generate_pending_files_list_helper, update_ignored_pending_list_helper

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


def check_db_credentials(context, data_dict):
    logic.check_access(u'package_create', context)
    # log.info(data_dict)
    # log.info(context)
    try:
        db_name = data_dict.get('db_name', '')
        db_type = data_dict.get('db_type', '')
        token = data_dict.get('token', '')
        username, password = base64.b64decode(token).decode('utf-8').split(':') if token else (None, None)
        db_obj = validate_db_connections_and_init(db_type)
        is_login = db_obj.check_login_credentials(db_type, db_name, username, password)
        return is_login
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
        token = data_dict.get('token', '')
        username, password = base64.b64decode(token).decode('utf-8').split(':') if token else (None, None)
        db_obj = validate_db_connections_and_init(db_type)
        isValid = True
        db_schema = None
        if db_type == 'azuresql':
            isValid = db_obj.validate_azure()
        if isValid:
            db_schema = db_obj.fetch_schema(db_type, db_name, username, password)
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
        token = data_dict.get('token', '')
        username, password = base64.b64decode(token).decode('utf-8').split(':') if token else (None, None)
        db_obj = validate_db_connections_and_init(db_type)
        db_tables = db_obj.fetch_tables(db_type, db_name, schema, username, password)
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
        token = data_dict.get('token', '')
        username, password = base64.b64decode(token).decode('utf-8').split(':') if token else (None, None)
        db_obj = validate_db_connections_and_init(db_type)
        db_table_metadata = db_obj.fetch_metadata(db_type, db_name, schema, table, username, password)
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
        count = data_dict.get('count','1')
        datalake_connection = DataLakeHandler()
        datalake_connection.initialize_storage_account()
        # page_num = data_dict.get('page_num','')

        return datalake_connection.list_file_system(count)
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
        page_num = data_dict.get('page_num', '')
        records_per_page = data_dict.get('records_per_page', '')
        return datalake_connection.list_directory_contents(container, path, page_num, records_per_page)
    except Exception as e:
        log.error(e)
        raise e


def get_datalake_file_search(context, data_dict):
    # Validate whether user has permission to create datasets or not
    logic.check_access(u'package_create', context)
    try:
        datalake_connection = DataLakeHandler()
        datalake_connection.initialize_storage_account()
        container = data_dict.get('container', '')
        query = data_dict.get('query', '')
        page_num = data_dict.get('page_num', '')
        records_per_page = data_dict.get('records_per_page', '')
        return datalake_connection.get_search_results(container, query, page_num, records_per_page)
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

def get_file_contents(context, data_dict):
    '''Return a top x line of file set in env or otherwise 10
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
        if path.endswith('.csv'):
            return datalake_connection.get_csv_data(container, path)
        else:
            return []
    except Exception as e:
        log.error(e)
        raise e

def get_geo_metadata(context, data_dict):
    logic.check_access(u'package_create', context)
    try:
        datalake_connection = DataLakeHandler()
        datalake_connection.initialize_storage_account()
        container = data_dict.get('container', '')
        path = data_dict.get('path', '')
        return datalake_connection.get_geo_metadata(container, path)
    except Exception as e:
        log.error(e)
        raise e


@toolkit.side_effect_free
def package_ext_spatial_patch(context, data_dict):
    logic.check_access(u'package_create', context)
    try:
        # log.info(data_dict)
        spatial_extent = make_list(data_dict.get('spatial_extent'))
        id = data_dict.get('id')
        if spatial_extent:
            package = logic.action.get.package_show(context, {"id": id})
            if 'extras' not in package:
                package['extras'] = []
            if 'spatial' not in package.get('extras'):
                from ckanext.data_catalog_510.utils.helpers import get_bbox_from_coords
                package['extras'].append({'key': 'spatial', 'value': json.dumps(get_bbox_from_coords(spatial_extent))})
                package = logic.action.patch.package_patch(context, package)
        # log.info(package)
        return package
    except Exception as e:
        log.error(e)
        raise e


# @toolkit.side_effect_free
# def extended_package_search(context, data_dict):
#     logic.check_access(u'package_create', context)
#     try:
#         log.info(data_dict)
#         query = data_dict.get('q')
#         if query and query.startswith('location:'):
#             location = query.split('location:')[-1] if len(query.split('location:')) > 0 else ''
#             if location:
#                 from ckanext.data_catalog_510.utils.helpers import get_location_geocode
#                 coords = get_location_geocode(location)
#                 log.info(coords)
#                 if coords:
#                     data_dict['extras']['ext_bbox'] = str(','.join(coords))
#         return logic.action.get.package_search(context, data_dict)
#     except Exception as e:
#         log.error(e)
#         raise e


@toolkit.side_effect_free
def country_autocomplete(context, data_dict):
    from ckanext.data_catalog_510.utils.helpers import get_countries
    search = data_dict.get('search')
    return get_countries(search)

@toolkit.side_effect_free
def forecast_project_autocomplete(context, data_dict):
    from ckanext.data_catalog_510.utils.helpers import get_forecast_projects
    search = data_dict.get('search')
    return get_forecast_projects(search)


@toolkit.side_effect_free
def forecast_product_autocomplete(context, data_dict):
    from ckanext.data_catalog_510.utils.helpers import get_forecast_products
    search = data_dict.get('search')
    return get_forecast_products(search)


@toolkit.side_effect_free
def extended_package_patch(context, data_dict):
    package = set_data_access(data_dict)
    package = logic.action.patch.package_patch(context, data_dict)
    return package


@toolkit.side_effect_free
def extended_package_create(context, data_dict):
    package = set_data_access(data_dict)
    package = logic.action.create.package_create(context, data_dict)
    return package


@toolkit.side_effect_free
def extended_package_update(context, data_dict):
    package = set_data_access(data_dict)
    package = logic.action.update.package_update(context, data_dict)
    return package

@toolkit.side_effect_free
def update_ignore_pending_file_list(context, data_dict):
    ignore_data = json.loads(data_dict.get('ignore_data'))
    return update_ignored_pending_list_helper(ignore_data)


@toolkit.side_effect_free
def generate_pending_file_list_job(context, data_dict):
    return generate_pending_files_list_helper(context)
