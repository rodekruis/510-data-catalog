# /bin/bash

# Install the Dev Requirements needed for tests
pip install -r /usr/lib/ckan/venv/src/ckan/dev-requirements.txt

# Run the tests for the Extension
pytest --ckan-ini=/usr/lib/ckan/venv/src/ckan/test-core.ini /usr/lib/ckan/venv/src/extensions/ckanext-data-catalog-510/ckanext/data_catalog_510/tests/
