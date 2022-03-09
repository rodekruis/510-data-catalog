import os

APIS = {
    'PACKAGE_LIST': '/api/3/action/package_list',
    'PACKAGE_SEARCH': '/api/3/action/package_search',
    'PACKAGE_SHOW': '/api/3/action/package_show',
    'RESOURCE_SHOW': '/api/3/action/resource_show',
}

ENV = {
    'CKAN_SITE_URL': os.environ.get('CKAN_SITE_URL'),
    'SENDGRID_API_KEY': os.environ.get('SENDGRID_API_KEY'),
    'CKAN_API_KEY': os.environ.get('CKAN_API_KEY'),
    'CKAN__AZURESQL_DB_CONNECTIONS': os.environ.get('CKAN__AZURESQL_DB_CONNECTIONS'),
    'CKAN__MYSQL_DB_CONNECTIONS': os.environ.get('CKAN__MYSQL_DB_CONNECTIONS'),
    'CKAN__POSTGRESQL_DB_CONNECTIONS': os.environ.get('CKAN__POSTGRESQL_DB_CONNECTIONS'),
    'CKAN__DATALAKE_ACCOUNT_KEY': os.environ.get('CKAN__DATALAKE_ACCOUNT_KEY'),
    'CKAN__DATALAKE_ACCOUNT_NAME': os.environ.get('CKAN__DATALAKE_ACCOUNT_NAME'),
    'TEAMS_CHANNEL_EMAIL': os.environ.get('TEAMS_CHANNEL_EMAIL'),
}