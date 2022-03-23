from azure.storage.filedatalake import DataLakeServiceClient
import rioxarray as rxr
import geopandas as gpd
import fiona
import pyodbc
from rasterio.io import MemoryFile

from ckan.common import config, _, c
import ckan.logic as logic
from ckanext.data_catalog_510.utils.utilities import endsWith, get_file_format

import logging
log = logging.getLogger(__name__)

NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
ValidationError = logic.ValidationError
GEO_METADATA_AUTOFILL_SIZE_LIMIT = 100000000


class DataLakeHandler:
    def __init__(self):
        '''Initalize the class with the account name and key for the data
        azure storage
        '''
        self.service_client = ''
        self.storage_account_name = config.get('ckan.datalake_account_name')
        self.storage_account_key = config.get('ckan.datalake_account_key')

    def initialize_storage_account(self):
        '''Get the azure storage account service client using account details
        '''
        try:
            service_client = DataLakeServiceClient(
                account_url="{}://{}.dfs.core.windows.net".format(
                            "https", self.storage_account_name),
                credential=self.storage_account_key)
            self.service_client = service_client
        except Exception as e:
            log.error(e)

    def check_container_access(self, container):
        result = False
        try:
            user_email = c.userobj.email.upper()
            log.info(user_email)
            acl_group_mapping =  config.get('ckan.datalake_groups_mapping')
            log.info(acl_group_mapping)
            root_directory_client = self.service_client.get_directory_client(file_system=container, directory="/")
            container_acl_data = root_directory_client.get_access_control()['acl']
            if container_acl_data:
                acl_string_list = container_acl_data.split(",")
                acl_groups_list = [group_string for group_string in acl_string_list if group_string.startswith("group")]
                acl_group_ids = [group_string.split(":")[1] for group_string in acl_groups_list if group_string.split(":")[1] and group_string.split(":")[2].startswith("r")]
                log.info(acl_group_ids)
                acl_group_names = [mapping['name'] for mapping in acl_group_mapping if mapping['objectId'] in acl_group_ids]
                if len(acl_group_names) > 0:
                    connString = config.get("ckan.datalake_groups_db_connection")
                    log.info(connString)
                    try:
                        with pyodbc.connect(connString) as sqlconn:
                            cursor = sqlconn.cursor()
                            for group_name in acl_group_names:
                                cursor.execute(f"select [isMemberOf{group_name}] from [cleaned_ckan].[CkanPermissions] where UPPER(mail) = {user_email}")
                                value = cursor.fetchval()
                                if value:
                                    result = True
                                    break
                    except Exception as e:
                        raise e
        except Exception as e:
            log.error(e, exc_info=True)
        finally:
            return result


    def list_file_system(self, page_num):
        '''Get the File System/Containers List
        '''
        try:
            file_system = self.service_client.\
                                    list_file_systems(include_metadata=True)
            containers = []
            for data in file_system:
                if self.check_container_access(data):
                    containers.append({'name': data.name})
            return containers
        except Exception as e:
            log.error(e)
            raise e

    def list_directory_contents(self, container, user_path=None, page_num=None, records_per_page=None):
        '''Fetch the content of container or path
        '''
        # List of directories and their path will be stored.
        # log.info({"container": container, "path": user_path, "page_num": page_num, "records": records_per_page})
        directory_structure = []
        total_records = 0
        try:
            file_system_client = self.service_client.\
                get_file_system_client(file_system=container)
            paths = list(file_system_client.get_paths(path=user_path, recursive=False))
            total_records = len(paths)
            # Logic for previous path
            if not user_path or user_path == '':
                prev_path = "container"
            else:
                prev_path_list = user_path.rsplit('/', 1)
                if len(prev_path_list) > 1:
                    prev_path = prev_path_list[0]
                else:
                    prev_path = ""
            
            if page_num and records_per_page:
                page_num -= 1
                start_index = page_num * records_per_page
                end_index = page_num * records_per_page + records_per_page
                end_index = end_index if end_index < total_records else total_records
                paths = paths[start_index: end_index]
            for path in paths:
                path_type = 'file'
                path_format = get_file_format(path.name)
                if path.is_directory:
                    # Change path type to 'directory' when it is directory.
                    path_type = 'directory'
                    if path.name:
                        directory_paths = file_system_client.get_paths(path=path.name, recursive=False)
                        for file_path in directory_paths:
                            if not file_path.is_directory:
                                path_format = get_file_format(file_path.name)
                                break
                directory_structure.append({'path': path.name,
                                            'type': path_type,
                                            'name': path.name.split('/')[-1],
                                            'format': path_format})
            return {'container': container,
                    'directory_structure': directory_structure,
                    'prev_path': prev_path,
                    'total_records': total_records
                    }
        except Exception as e:
            log.error(e)
            raise e

    def get_no_of_files(self, container, user_path=None):
        '''Calculate no of files in the given path
        '''
        count = 0
        try:
            file_system_client = self.service_client.\
                get_file_system_client(file_system=container)
            paths = file_system_client.get_paths(path=user_path,
                                                 recursive=True)
            for data in paths:
                if not data.is_directory:
                    # No of files only for not directory
                    count += 1
            return count
        except Exception as e:
            log.error(e)
            raise e
    
    def get_geo_metadata(self, container, user_path=None):
        response = {}
        geo_metadata = {}
        try:
            file_client = self.service_client.get_file_client(file_system=container, file_path=user_path)
            if file_client.exists():
                file_properties = file_client.get_file_properties()
                # log.info(file_properties.size)
                if file_properties.size < GEO_METADATA_AUTOFILL_SIZE_LIMIT:
                    if endsWith(user_path, ['.tiff', '.tif']):
                        geoFile = file_client.download_file()
                        with MemoryFile(geoFile.readall()) as memfile:
                            with memfile.open() as dataset:
                                geoData = rxr.open_rasterio(dataset, masked=True)
                                geo_metadata['spatial_extent'] = str(list(geoData.rio.bounds()))
                                geo_metadata['spatial_resolution'] = str(geoData.rio.resolution()[0])
                                geo_metadata['spatial_reference_system'] = str(geoData.rio.crs.to_epsg())
                    elif endsWith(user_path, ['.geojson']):
                        geoFile = file_client.download_file()
                        with fiona.BytesCollection(bytes(geoFile.readall())) as fileBytes:
                            geoData = gpd.GeoDataFrame.from_features(fileBytes, crs=fileBytes.crs_wkt)
                            geo_metadata['spatial_extent'] = str(list(geoData.total_bounds))
                            geo_metadata['spatial_resolution'] = ""
                            geo_metadata['spatial_reference_system'] = str(geoData.crs.to_epsg())
                    # log.info(geo_metadata)
                    response["data"] = geo_metadata
                    response["error"] = None
                else:
                    response["data"] = None,
                    response["error"] = f"File size is too big for auto-fill. Please ensure that for auto-fill, file size does not exceed {GEO_METADATA_AUTOFILL_SIZE_LIMIT / 1000000} MB."
        except Exception as e:
            log.error(e)
            raise e
        finally:
            return response

    def get_search_results(self, container, query, page_num, records_per_page):
        search_results = []
        total_results = 0
        try:
            file_system_client = self.service_client.\
                get_file_system_client(file_system=container)
            paths = list(file_system_client.get_paths(path="/", recursive=True))
            for path in paths:
                path_name = path.name.split("/")[-1]
                if path_name.lower().startswith(query.lower()):
                    full_path = path.name
                    path_format = get_file_format(path.name)
                    path_type = "file"
                    if path.is_directory:
                        path_type = 'directory'
                        if path.name:
                            directory_paths = list(file_system_client.get_paths(path=path.name, recursive=False))
                            for file_path in directory_paths:
                                if not file_path.is_directory:
                                    path_format = get_file_format(file_path.name)
                                    break
                    search_results.append({
                        "path": full_path,
                        "type": path_type,
                        "name": path_name,
                        "format": path_format
                    })
            total_results = len(search_results)
            page_num -= 1
            start_index = page_num * records_per_page
            end_index = page_num * records_per_page + records_per_page
            end_index = end_index if end_index < total_results else total_results
            search_results = search_results[start_index: end_index]
            return {
                'search_results': search_results,
                'total_results': total_results
            }
        except Exception as e:
            log.error(e)
    
    def get_all_paths(self):
        path_list = []
        try:
            container_list = list(self.service_client.list_file_systems())
            for container in container_list:
                file_system_client = self.service_client.get_file_system_client(container)
                paths = list(file_system_client.get_paths(path="/", recursive=True))
                for path in paths:
                    if path.is_directory:
                        paths.remove(path)
                    else:
                        container_path = {
                            'container': container.name,
                            'path': path.name,
                        }
                        path_list.append(container_path)
        except Exception as e:
            log.error(e, exc_info=True)
        finally:
            return path_list
    
    def upload_file(self, container, file_path, data):
        try:
            file_client = self.service_client.get_file_client(file_system=container, file_path=file_path)
            file_client.create_file()
            file_client.append_data(data, offset=0, length=len(data))
            file_client.flush_data(len(data))
        except Exception as e:
            log.error(e)
            raise e
