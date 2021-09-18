import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.data_catalog_510.\
     utils.validators import (validate_date_yyyy_mm_dd)


class DataCatalog510Plugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IValidators)

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
