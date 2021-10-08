# /bin/bash
# Initialize the CKAN DB
ckan db init

# Install the Extensions
/bin/sh scripts/install_extensions.sh

# Update the Plugins from the ENV
ckan config-tool $CKAN_CONFIG/production.ini "ckan.plugins = ${CKAN__PLUGINS}"

# Start the CKAN
ckan run --host 0.0.0.0 --port 5000
