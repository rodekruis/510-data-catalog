# encoding: utf-8
'''Tests for the ckanext.data_catalog_510 extension.

'''
import json
import pytest
import ckanext.data_catalog_510.utils.helpers as helpers
import datetime
import ckan.tests.factories as factories
import unittest.mock as mock
from ckan.common import c, config
import logging
log = logging.getLogger(__name__)


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
        '''Test used to get the current date in the format yyyy-mm-dd'''
        
        with pytest.raises(Exception) as excinfo:
            res = helpers.get_current_date("")
             
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
      
    def test_get_request_data_mailTo(self):
        ''' Test to check the mail data string'''
        expected_res = "mailto:test@valuelabs@@com?cc=bottow@redcross@@nl&subject=510%\20Data%\20Catalog:%20\Please%20\give%\20me%\20access%\20to%\20test&body=Dear%2\0data%20\owner,%\0A%\0AI%\20found%20'test'%\20part%\20of%20'test'%\20in%\20the%\20510%\20Data%\20Catalog.%\20You%\20can%\20find%\20the%\20entry%20\here:%20\http://localhost:5000/dataset/test/resource/9ca50bcd-7e00-41ec-88ec-29081624f10a%\0A%\0ACould%\20you%\20please%2\0give%2\0me%20\access%20\to%\20the%\20data?%\0A%\0AThanks%\20in%\20advance,%\0A%\0A"
        mock_method = ('ckanext.data_catalog_510.utils'
                       '.helpers.get_request_data_mailTo')
        with mock.patch(mock_method) as r:
            r.return_value = expected_res
            response = helpers.get_request_data_mailTo({},{})
            assert response == expected_res
            
    @pytest.mark.parametrize("text_input",[([24.72, 21.99, 36.89, 31.65])]) 
    def test_get_bbox_from_coords(self,text_input):
        ''' Test to get the coords from bbox'''
        expected_res = {'type': 'Polygon', 'coordinates': [[[31.65, 24.72], [31.65, 21.99], [36.89, 21.99], [36.89, 24.72], [31.65, 24.72]]]}

        assert ( helpers.get_bbox_from_coords(text_input) == expected_res)
        
    def test_get_location_geocode(self):
        ''' Test to check the geocode function'''
        assert ( type(helpers.get_location_geocode("Netherlands")) is list)
        
       
    @pytest.mark.parametrize("text_input,expected",[
                            (
                                {"security_classification" : "high","private" : False},
                                {'security_classification': 'high', 'private': True}
                            ),
                            (
                               {"security_classification" : "high","private" : True}, 
                               {"security_classification" : "high","private" : True}
                            ),
                            (
                               {"security_classification" : "high"}, 
                               {"security_classification" : "high","private" : True}
                            ),
                            (
                               {"security_classification" : "low","private" : True}, 
                               {"security_classification" : "low","private" : False}
                            )
                            ]) 
    def test_set_data_access(self,text_input,expected):
        ''' Test to check the data access '''
        assert( helpers.set_data_access(text_input) == expected)
        