from collections import OrderedDict

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.data_catalog_510.\
     utils.validators import (validate_date_yyyy_mm_dd)
from ckanext.data_catalog_510.\
     utils.helpers import (get_countries)
from collections import OrderedDict

from ckanext.data_catalog_510.logic import (get_db_connections,
                                            get_schemas,
                                            get_tables,
                                            get_tables_metadata,
                                            get_all_dbs,
                                            get_containers,
                                            get_directories_and_files,
                                            get_no_of_files)


class DataCatalog510Plugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IFacets)
    plugins.implements(plugins.IDatasetForm, inherit=False)
    plugins.implements(plugins.IFacets)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
                             'data_catalog_510')
        toolkit.add_resource('assets', 'ckanext-data_catalog_510')

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
            'get_no_of_files': get_no_of_files
        }

    # Helpers
    def get_helpers(self):
        return {
            'get_countries_list': get_countries
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
                            ('initially_used', 'Project')])

    def group_facets(self, facets_dict, group_type, package_type):
        return facets_dict

    def organization_facets(self, facets_dict, organization_type,
                            package_type):
        return facets_dict

