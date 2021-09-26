import logging
import json
log = logging.getLogger(__name__)
import os
HERE = os.path.dirname(__file__)

def get_countries():
    
    log.info(HERE)
    with open(os.path.join(HERE, 'country.json'),'r') as f:
        license_data = json.load(f)
    return license_data


