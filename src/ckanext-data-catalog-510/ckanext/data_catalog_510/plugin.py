import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.data_catalog_510.\
     utils.validators import (validate_date_yyyy_mm_dd)
from ckanext.data_catalog_510.\
     utils.helpers import (get_countries, get_db_host, generate_sample_db_string, get_request_data_mailTo, get_bbox_from_coords, get_site_url)
from collections import OrderedDict

from ckanext.data_catalog_510.logic import (get_db_connections,
                                            get_schemas,
                                            get_tables,
                                            get_tables_metadata,
                                            get_all_dbs,
                                            get_containers,
                                            get_directories_and_files,
                                            get_datalake_file_search,
                                            get_no_of_files,
                                            get_geo_metadata,
                                            package_ext_spatial_patch,
                                            # extended_package_search,
                                            country_autocomplete,
                                            forecast_project_autocomplete,
                                            forecast_product_autocomplete,
                                            check_db_credentials,
                                            extended_package_patch,
                                            extended_package_create,
                                            generate_pending_file_list_job,
                                            update_ignore_pending_file_list,
                                            extended_package_update)


class DataCatalog510Plugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IFacets)
    plugins.implements(plugins.IDatasetForm, inherit=False)
    plugins.implements(plugins.IPackageController, inherit=True)
    # For plugin interfaces
    # Please follow - https://docs.ckan.org/en/2.9/extensions/plugin-interfaces.html#plugin-interfaces-reference

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
                             'data_catalog_510')
        toolkit.add_resource('assets', 'ckanext-data_catalog_510')

    # IValidators
    def get_validators(self):
        return {
            'validate_date_yyyy_mm_dd': validate_date_yyyy_mm_dd
        }

    # IActions
    def get_actions(self):
        return {
            'get_db_connections': get_db_connections,
            'get_schemas': get_schemas,
            'get_tables': get_tables,
            'get_tables_metadata': get_tables_metadata,
            'get_all_dbs': get_all_dbs,
            'get_containers': get_containers,
            'get_directories_and_files': get_directories_and_files,
            "get_datalake_file_search": get_datalake_file_search,
            'get_no_of_files': get_no_of_files,
            'get_geo_metadata': get_geo_metadata,
            'country_autocomplete': country_autocomplete,
            'forecast_project_autocomplete': forecast_project_autocomplete,
            'forecast_product_autocomplete': forecast_product_autocomplete,
            'check_db_credentials': check_db_credentials,
            'package_ext_spatial_patch': package_ext_spatial_patch,
            # 'package_search': extended_package_search
            'package_patch': extended_package_patch,
            'package_update': extended_package_update,
            'package_create': extended_package_create,
            'generate_pending_files_list': generate_pending_file_list_job,
            'update_ignore_pending_file_list': update_ignore_pending_file_list
        }

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'get_countries_list': get_countries,
            'get_db_string': get_db_host,
            'generate_sample_db_string': generate_sample_db_string,
            'get_request_data_mailTo': get_request_data_mailTo,
            'get_bbox_from_coords': get_bbox_from_coords,
            'get_site_url': get_site_url
        }

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return False

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    def dataset_facets(self, facets_dict, package_type):
        return OrderedDict([('dataset_owner', 'Dataset Owner'),
                            ('country', 'Country'),
                            ('accuracy', 'Dataset Quality: Accuracy'),
                            ('consistency', 'Dataset Quality: Consistency'),
                            ('completeness', 'Dataset Quality: Completeness'),
                            ('security_classification', 'Security Classification'),
                            ('forecast_project', 'Used in Projects'),
                            ('forecast_product', 'Used in Products')])

    def group_facets(self, facets_dict, group_type, package_type):
        return facets_dict

    def organization_facets(self, facets_dict, organization_type,
                            package_type):
        return facets_dict

    # IPackageController
    def before_index(self, data_dict):
        if 'country' in data_dict and isinstance(data_dict['country'], str):
            data_dict['country'] = data_dict.get('country', []).split(",")
        if 'forecast_project' in data_dict and isinstance(data_dict['forecast_project'], str):
            data_dict['forecast_project'] = data_dict.get('forecast_project', []).split(",")
        if 'forecast_product' in data_dict and isinstance(data_dict['forecast_product'], str):
            data_dict['forecast_product'] = data_dict.get('forecast_product', []).split(",")
        return data_dict
