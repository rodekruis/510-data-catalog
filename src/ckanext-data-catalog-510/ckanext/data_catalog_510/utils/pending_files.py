from io import StringIO
import json
import os
import csv
import logging
from datetime import datetime, timezone, timedelta

import ckan.logic as logic

from ckanext.data_catalog_510.controllers.database_handler import SQLHandler
from ckanext.data_catalog_510.controllers.datalake_handler import DataLakeHandler
from ckanext.data_catalog_510.utils.utilities import startsWith

log = logging.getLogger(__name__)
HERE = os.path.dirname(__file__)


def is_database_table_ignored(ignore_path, path):
    if ignore_path['db_type'] == path['db_type']:
        if ignore_path['db_name'] == path['db_name']:
            if ignore_path['schema_name'] == path['schema_name']:
                if "*" in ignore_path['tables'] or path['table_name'] in ignore_path['tables']:
                    return True
    return False


def is_datalake_path_ignored(ignore_paths, path):
    if ignore_paths['container'] == path['container']:
        if "*" in ignore_paths['paths'] or startsWith(path['path'], ignore_paths['paths']):
            return True
    return False


def filter_datalake_paths(datalake_paths):
    try:
        with open(os.path.join(HERE, 'ignore_pending_files.json'), 'r') as fp:
            ignore_dict = json.load(fp)
            filtered_datalake_paths = datalake_paths
            for ignore_paths in ignore_dict['datalake']:
                filtered_datalake_paths = [data for data in filtered_datalake_paths if not is_datalake_path_ignored(ignore_paths, data)]
        # log.info("Filtered Datalake: " + str(filtered_datalake_paths))
        return filtered_datalake_paths
    except Exception as e:
        log.error(e, exc_info=True)


def filter_database_data(database_data):
    try:
        with open(os.path.join(HERE, 'ignore_pending_files.json'), 'r') as fp:
            ignore_dict = json.load(fp)
            filtered_database_data = database_data
            for ignore_table in ignore_dict['database']:
                filtered_database_data = [data for data in filtered_database_data if not is_database_table_ignored(ignore_table, data)]
        # log.info("Filtered Database: " + str(filtered_database_data))
        return filtered_database_data
    except Exception as e:
        log.error(e, exc_info=True)


def generate_pending_file_list(context):
    stop_api = False
    result = False
    rows = 10
    start = 0
    try:
        resource_list = []
        while not stop_api:
            package_slice = logic.action.get.package_search(
                context, {'rows': rows, 'start': start, 'include_private': True})
            # log.info("Package_slice: " + str(package_slice['results']))
            if len(package_slice['results']) > 0:
                for package in package_slice['results']:
                    resource = package['resources']
                    resource_list.extend(resource)
                start += rows
            else:
                stop_api = True
        # log.info("Resource List: " + str(resource_list))
        if len(resource_list) > 0:
            datalake_handler = DataLakeHandler()
            datalake_handler.initialize_storage_account()
            datalake_paths = datalake_handler.get_all_paths()
            # log.info("Datalake_handler: " + str(datalake_paths))

            database_handler = SQLHandler()
            database_data = database_handler.get_all_tables()
            # log.info("Database_handler: " + str(database_data))

            if len(datalake_paths) > 0:
                for resource in resource_list:
                    if resource['resource_type'] == 'datalake':
                        for container_path in datalake_paths:
                            if resource['datalake_data']['container'] == container_path['container']:
                                if container_path['path'].startswith(resource['datalake_data']['file_path']):
                                    datalake_paths.remove(container_path)
            if len(database_data) > 0:
                for resource in resource_list:
                    if resource['resource_type'] == 'database':
                        for database_path in database_data:
                            if resource['database_connection'] == database_path['db_name']:
                                if resource['schema_name'] == database_path['schema_name']:
                                    if resource['table_name'] == database_path['table_name']:
                                        database_data.remove(database_path)
            datalake_paths = filter_datalake_paths(datalake_paths)
            # print(datalake_paths)
            database_data = filter_database_data(database_data)
            # print(database_data)

            timestamp = datetime.now(timezone(timedelta(hours=1.0))).isoformat(
                sep="_", timespec='minutes')
            # print(timestamp)
            if len(datalake_paths) > 0:
                with StringIO(newline='') as csvFile:
                    filename = f"510DataCatalog_Pending_Datalake_{timestamp}.csv"
                    writer = csv.DictWriter(csvFile, fieldnames=[
                                            'container', 'path'])
                    writer.writeheader()
                    writer.writerows(datalake_paths)
                    csvFile.seek(0)
                    # print(csvFile.getvalue())

                    datalake_handler.upload_file('data-catalog', f'dataset-verification/{filename}', csvFile.getvalue())

            if len(database_data) > 0:
                with StringIO(newline='') as csvFile:
                    filename = f"510DataCatalog_Pending_Database_{timestamp}.csv"
                    writer = csv.DictWriter(csvFile, fieldnames=['db_type', 'db_name', 'schema_name', 'table_name'])
                    writer.writeheader()
                    writer.writerows(database_data)
                    csvFile.seek(0)

                    datalake_handler.upload_file('data-catalog', f'dataset-verification/{filename}', csvFile.read())
            result = True
        else:
            raise Exception(
                "Could not retrieve any resources from Data Catalog.")
    except Exception as e:
        log.error(e, exc_info=True)
        result = False
    finally:
        return result
