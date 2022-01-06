# encoding: utf-8
'''Tests for the ckanext.data_catalog_510 extension.

'''
import json
import pytest
import ckanext.data_catalog_510.utils.helpers as helpers
import datetime
import ckan.tests.factories as factories
import unittest.mock as mock
# import logging
# log = logging.getLogger(__name__)


class TestHelpers(object):
    
    def test_get_countries_count_validate(self):
        ''' Validate the get countries list by search string
        
        '''
        expected_result = ['British Indian Ocean Territory', 'India']
        data = helpers.get_countries('India')
        assert (expected_result == data)
        
    def test_get_current_date(self):
        '''Test used to get the current date in the format yyyy-mm-dd'''
        
        expected_result = datetime.datetime.today().strftime("%Y-%m-%d")
        res = helpers.get_current_date("")
        # log.info(res)       
        assert (res == expected_result)
        
    def test_get_current_date_with_exception(self):
        ''' Test used to verify the exception '''
        with pytest.raises(Exception) as excinfo:
            helpers.get_current_date()
            
            
    @pytest.mark.parametrize("text_input, expected", [
        ('hrsl_egy_pop_resized_100.geojson', 'application/geo+json'),
        ('hrsl_egy_pop_resized_100.tiff', 'image/tiff'),
        ('test_file.gif', 'GIF'),
        ('test_file', None)])
    def test_get_file_format(self,text_input, expected):
        '''Test to format of a file located at the path provided.'''
        
        assert(helpers.get_file_format((text_input)) == expected)
        
    @pytest.mark.parametrize("text_input,expected", [
                ({"security_classification":"high"},False),
                ({"security_classification":"low"},True)])
    def test_is_preview_access(self, text_input, expected):
        '''Test to check preview access of user based on security classification.'''
        assert(helpers.is_preview_access(text_input, None) == expected)
        
        
    @pytest.mark.parametrize("text_input,expected", [
                ({"security_classification":"normal"},True),
                ])
    def test_is_preview_access_with_user(self, text_input, expected):
        '''Test to check preview access of user based on security classification.'''
        
        assert(helpers.is_preview_access(text_input, factories.User) == expected)
      
    