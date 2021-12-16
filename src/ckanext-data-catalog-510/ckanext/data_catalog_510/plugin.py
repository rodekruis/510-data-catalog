import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.data_catalog_510.\
     utils.validators import (validate_date_yyyy_mm_dd)
from ckanext.data_catalog_510.\
     utils.helpers import (get_countries, get_db_host, generate_sample_db_string, get_request_data_mailTo, check_security_classification, get_bbox_from_coords)
from collections import OrderedDict

from ckanext.data_catalog_510.logic import (get_db_connections,
                                            get_schemas,
                                            get_tables,
                                            get_tables_metadata,
                                            get_all_dbs,
                                            get_containers,
                                            get_directories_and_files,
                                            get_no_of_files,
                                            get_geo_metadata,
                                            country_autocomplete)


class DataCatalog510Plugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IFacets)
    plugins.implements(plugins.IDatasetForm, inherit=False)
    # plugins.implements(plugins.IPackageController, inherit=False)
    plugins.implements(plugins.IFacets)
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
            'get_no_of_files': get_no_of_files,
            'get_geo_metadata': get_geo_metadata,
            'country_autocomplete': country_autocomplete,
            
        }

    # ITemplateHelpers
    def get_helpers(self):
        return {
            'get_countries_list': get_countries,
            'get_db_string': get_db_host,
            'generate_sample_db_string': generate_sample_db_string,
            'get_request_data_mailTo': get_request_data_mailTo,
            'check_security_classification': check_security_classification,
            'get_bbox_from_coords': get_bbox_from_coords
        }

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return False

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []
    
    def _modify_package_schema(self, schema):
        # Add our spatial metadata field to the schema, this one will use
        # convert_to_extras instead of convert_to_tags.
        schema.update({
                'spatial': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')]
        })
        print(schema)
        return schema
    
    def show_package_schema(self):
        schema = super(DataCatalog510Plugin, self).show_package_schema()

        # Add our spatial field to the dataset schema.
        schema.update({
            'spatial': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_from_extras')]
            })

        return schema

    def create_package_schema(self):
        schema = super(DataCatalog510Plugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(DataCatalog510Plugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def dataset_facets(self, facets_dict, package_type):
        return OrderedDict([('dataset_owner', 'Dataset Owner'),
                            ('country', 'Country'),
                            ('initially_used', 'Project'),
                            ('data_quality', 'Dataset Quality')])

    def group_facets(self, facets_dict, group_type, package_type):
        return facets_dict

    def organization_facets(self, facets_dict, organization_type,
                            package_type):
        return facets_dict
    
    # IPackageController
    # def before_search(self, search_params):
    #     print("Before search", search_params)
    #     query = search_params.get('q')
    #     if query and 'location' in query:
    #         location = query.replace(" ", "").split(':')[-1]
    #         coords = get_bbox_from_coords(location)
    #         if coords:
    #             search_params['extras']['ext_bbox'] = coords
    #     return search_params
    
    # def after_search(self, search_results, search_params):
    #     print(search_results)
    #     return search_results
    
    # def before_view(self, pkg_dict):
    #     return pkg_dict
    
    # def before_index(self, pkg_dict):
    #     return pkg_dict
