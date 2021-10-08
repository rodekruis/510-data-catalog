# /bin/bash
# Initialize the CKAN DB
ckan db init

# Install the Extensions
/bin/sh scripts/install_extensions.sh

# Update the Plugins from the ENV
ckan config-tool $CKAN_CONFIG/production.ini "ckan.plugins = ${CKAN__PLUGINS}"
/bin/sh scripts/ckan_ini.sh

# Start the CKAN
/usr/lib/ckan/venv/bin/uwsgi -i /etc/ckan/uwsgi.ini
