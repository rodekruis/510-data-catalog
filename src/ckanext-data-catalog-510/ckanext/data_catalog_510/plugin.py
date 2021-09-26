import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.data_catalog_510.\
     utils.validators import (validate_date_yyyy_mm_dd)
from ckanext.data_catalog_510.\
     utils.helpers import (get_countries)


class DataCatalog510Plugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IValidators)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
                             'data_catalog_510')

    def get_validators(self):
        return {
            'validate_date_yyyy_mm_dd': validate_date_yyyy_mm_dd
        }

    def get_helpers(self):
        return {
            'get_countries_list': get_countries
        }
