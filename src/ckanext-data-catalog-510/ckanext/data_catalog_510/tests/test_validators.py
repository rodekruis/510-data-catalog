# encoding: utf-8
'''Tests for the ckanext.data_catalog_510 extension.

'''
import pytest

import ckanext.data_catalog_510.utils.validators as validators
from ckan.lib.navl.dictization_functions import (Invalid)


@pytest.mark.ckan_config('ckan.plugins',
                         'data_catalog_510')
class TestValidators(object):
    def test_date_yyyy_mm_dd_correct_date(self):
        '''Validate the Date input for the Validators

        '''
        assert (validators.validate_date_yyyy_mm_dd("2021-12-20", {}) ==
                "2021-12-20")

    def test_date_yyyy_mm_dd_wrong_format(self):
        '''Validate the Date input for the Validators

        '''
        with pytest.raises(Invalid):
            validators.validate_date_yyyy_mm_dd("2021-20-12", {})
            
    def test_date_yyyy_mm_dd_without_value(self):
        '''Validate the date input without value'''
        assert (validators.validate_date_yyyy_mm_dd("",{}) == None)
