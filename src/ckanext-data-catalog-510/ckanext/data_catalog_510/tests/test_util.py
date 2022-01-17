# encoding: utf-8

import pytest

import ckanext.data_catalog_510.utils.utilities as util
class TestUtil(object):
    
    def test_ends_with_check_success(self):
        expected_result = True
        path = "tiff/hrsl_egy_pop_resized_100.tif"
        
        assert(util.endsWith(path,['.tiff','.tif']) == expected_result)
        
    def test_ends_with_check_fail(self):
        expected_result = False
        path = "tiff/hrsl_egy_pop_resized_100.tif"
        
        assert(util.endsWith(path,['.geojson']) == expected_result)

        