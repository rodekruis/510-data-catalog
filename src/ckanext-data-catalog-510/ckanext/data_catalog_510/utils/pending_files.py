import csv
import logging
from datetime import datetime, timezone, timedelta
from tempfile import NamedTemporaryFile

import ckan.logic as logic
from ckan.common import c

from ckanext.data_catalog_510.controllers.database_handler import SQLHandler
from ckanext.data_catalog_510.controllers.datalake_handler import DataLakeHandler

log = logging.getLogger(__name__)


def generate_pending_file_list():
    stop_api = False
    pending_files_list = {}
    rows = 10
    start = 0
    try:
        while not stop_api:
            resource_list = []
            package_slice = logic.action.get.package_search(
                c, {'rows': rows, 'start': start, 'include_private': True})
            if len(package_slice) > 0:
                for package in package_slice:
                    resource = package['resources']
                    resource_list.extend(resource)
                start += rows
            else:
                stop_api = True

        pending_files_list['datalake'] = []
        pending_files_list['database'] = []

        if len(resource_list) > 0:
            datalake_handler = DataLakeHandler()
            datalake_handler.initialize_storage_account()
            datalake_paths = datalake_handler.get_all_paths()

            database_handler = SQLHandler()
            database_data = database_handler.get_all_tables()

            if len(datalake_paths) > 0:
                for resource in resource_list:
                    if resource['resource_type'] == 'datalake':
                        for container_path in datalake_paths:
                            if resource['datalake_data']['container'] == container_path['container']:
                                if container_path['path'].startswith(resource['datalake_data']['file_path']):
                                    datalake_paths.remove(container_path)
                    elif resource['resource_type'] == 'database':
                        for database_path in database_data:
                            if resource['database_connection'] == database_path['db_name']:
                                if resource['schema_name'] == database_path['schema_name']:
                                    if resource['table_name'] == database_path['table_name']:
                                        database_data.remove(database_path)
                    else:
                        pass

                timestamp = datetime.now(timezone(timedelta(hours=1.0))).isoformat(
                    sep="_", timespec='minutes')

                with NamedTemporaryFile(mode='w+t', newline='') as csvFile:
                    csvFile.name = f"510DataCatalog_Pending_Datalake_{timestamp}.csv"
                    writer = csv.DictWriter(csvFile, fieldnames=[
                                            'container', 'path'])
                    writer.writeheader()
                    writer.writerows(datalake_paths)
                    csvFile.seek(0)

                    datalake_handler.upload_file('data-catalog', 'dataset-verification/{csvFile.name}', csvFile)
                
                with NamedTemporaryFile(mode='w+t', newline='') as csvFile:
                    csvFile.name = f"510DataCatalog_Pending_Database_{timestamp}.csv"
                    writer = csv.DictWriter(csvFile, fieldnames=['db_type', 'db_name', 'schema_name', 'table_name'])
                    writer.writeheader()
                    writer.writerows(database_data)
                    csvFile.seek(0)

                    datalake_handler.upload_file('data-catalog', 'dataset-verification/{csvFile.name}', csvFile)
        else:
            raise Exception(
                "Could not find any resources that are not published in 510 Data Catalog.")
    except Exception as e:
        log.error(e)
