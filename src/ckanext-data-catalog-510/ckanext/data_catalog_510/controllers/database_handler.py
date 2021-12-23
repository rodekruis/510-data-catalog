from sqlalchemy.sql.schema import Table
from ckan.common import config, _
import ckan.logic as logic

import json
from geoalchemy2 import Geometry
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError

import logging
log = logging.getLogger(__name__)
EXCLUDE_SCHEMAS = ['information_schema']
DATABASE_FORMAT = "Database Table"

ValidationError = logic.ValidationError
NotFound = logic.NotFound


class SQLHandler:
    def __init__(self):
        self.db_type = ""
        self.db_uri = ""

    def get_databases(self, db_type, return_url=False):
        ''' Method is used to fetch the databases from the configuration
        the config should have the DB in the list.
        e.g [
                {
                    "name":"test",
                    "title":"Test",
                    "url":"postgresql://ckan:ckan@db/ckan"
                }
            ]
        '''
        db_connections = ""
        if db_type == 'postgres':
            db_connections = config.get('ckan.postgresql_db_connections', '')
        if db_type == 'mysql':
            db_connections = config.get('ckan.mysql_db_connections', '')
        if db_type == 'azuresql':
            db_connections = config.get('ckan.azuresql_db_connections', '')
        db_connections = json.loads(db_connections)
        # to get the db_name from connection string
        # if db_type == 'azuresql':
        #     for item in db_connections:
        #         item['name'] = item['url'].split('/')[-1].split('?')[0]
        # else:  
        #     for item in db_connections:
        #         item['name'] = item['url'].split('/')[-1]
        if not return_url:
            [db.pop('url', None) for db in db_connections]
        return db_connections

    def get_db_connection_string(self, db_name):
        '''Method is used to get the url for the db from the connection
        string
        :param db_name: will be given to find the the url of db connection
        string(required).
        :type db_name: string

        :rtype: string
        '''
        db_connections = self.get_databases(self.db_type, return_url=True)
        log.info(db_name)
        filtered = [db['url'] for db in db_connections if db['name'] == db_name]
        if bool(filtered):
            return filtered[0]
        else:
            raise ValidationError(_('Database not available'))
    
    def get_db_host(self, db_type, db_name):
        self.db_type = db_type
        host = self.get_db_connection_string(db_name).split("@")[-1].split("/")[0]
        return host
    
    def get_base_db_connection_string(self, db_type, db_name):
        host = self.get_db_host(db_type, db_name)
        db_string = "Unknown DB String"
        if db_type == 'postgres':
            db_string = f"postgresql://<username>:<password>@{host}/{db_name}"
        elif db_type == 'mysql':
            db_string = f"mysql+pymysql://<username>:<password>@{host}/{db_name}"
        elif db_type == 'azuresql':
            db_string = f"mssql+pyodbc://<username>:<password>@{host}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server"
        else:
            db_string = "Unknown DB String"
        return db_string

    def get_user_db_connection_string(self, db_type, db_name, username, password):
        base_uri = self.get_base_db_connection_string(db_type, db_name)
        base_uri = base_uri.replace('<username>', username).replace('<password>', password)
        log.info(base_uri)
        return base_uri
    
    def check_login_credentials(self, db_type, db_name, username, password):
        try:
            schema = self.fetch_schema(db_type, db_name, username, password)
            return True if schema else False
        except Exception as e:
            log.error(e)
            return False

    def fetch_schema(self, db_type, db_name, username=None, password=None):
        '''Method is used to get the fetch the schemas for given db
        :param db_name: will be given to find the the url of db connection
        string(required).
        :type db_name: string

        :rtype: list of schemas
        '''
        try:
            self.db_type = db_type
            if db_type != 'azuresql':
                if username and password:
                    self.db_uri = self.get_user_db_connection_string(db_type, db_name, username, password)
                else:
                    raise NotFound(_('No User found in Database {}'.format(username)))
            else:
                self.db_uri = self.db_uri = self.get_db_connection_string(db_name)
            engine = create_engine(self.db_uri)
            inspector = inspect(engine)
            schemas = inspector.get_schema_names()
            schemas = [x for x in schemas if x not in EXCLUDE_SCHEMAS]
            if bool(schemas):
                return schemas
            else:
                raise NotFound(_('No Schema found in Database {}'
                                 .format(db_name)))
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            log.error(error)
            raise ValidationError(_(error))
        except Exception as e:
            log.error(e)
            raise e

    def fetch_tables(self, db_type, db_name, schema, username=None, password=None):
        '''Method is used to get the fetch the table for given db and schema
        :param db_name: will be given to find the the url of db connection
        string(required).
        :type db_name: string
        :param schema: will be given to find the the tables the schema
        string(required).
        :type schema: string

        :rtype: list of tables
        '''
        try:
            self.db_type = db_type
            if db_type != 'azuresql':
                if username and password:
                    self.db_uri = self.get_user_db_connection_string(db_type, db_name, username, password)
                else:
                    raise NotFound(_('No User found in Database {}'.format(username)))
            else:
                self.db_uri = self.db_uri = self.get_db_connection_string(db_name)
            engine = create_engine(self.db_uri)
            inspector = inspect(engine)
            tables = inspector.get_table_names(schema=schema)
            if bool(tables):
                return tables
            else:
                raise NotFound(_('No Tables found in {} schema of Database {}'
                                 .format(schema, db_name)))

        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            log.error(error)
            raise ValidationError(_(error))
        except Exception as e:
            log.error(e)
            raise e

    def fetch_metadata(self, db_type, db_name, schema, table_name, username=None, password=None):
        '''Method is used to get the fetch the metadata of tables for given
        db and schema
        :param db_name: will be given to find the the url of db connection
        string(required).
        :type db_name: string
        :param schema: will be given to find the the tables the schema
        string(required).
        :type schema: string
        :param table_name: will be given to find the the metadata of table
        string(required).
        :type table_name: string

        :rtype: list of metadata
        '''
        try:
            self.db_type = db_type
            if db_type != 'azuresql':
                if username and password:
                    self.db_uri = self.get_user_db_connection_string(db_type, db_name, username, password)
                else:
                    raise NotFound(_('No User found in Database {}'.format(username)))
            else:
                self.db_uri = self.db_uri = self.get_db_connection_string(db_name)
            engine = create_engine(self.db_uri)
            if db_type == 'mysql':
                query = f'Select Count(*) from `{schema}`.{table_name};'
            else:
                query = f'Select Count(*) from {schema}.{table_name};'
            
            result = engine.execute(query)
            count = result.first()[0]
            inspector = inspect(engine)
            columns = inspector.get_columns(table_name, schema=schema)
            # log.info(columns)
            col_type_list = list(map(lambda column: column['type'], columns))
            cols_list = list(map(lambda column: column['name'], columns))
            is_geo = False
            geo_metadata = {}
            if db_type == 'postgres':
                for column_type in enumerate(col_type_list):
                    log.info(str(column_type))
                    if 'Geo' in str(column_type) or 'Rast' in str(column_type):
                        is_geo = True
                        geom_col = "geom"
                        spatial_ext = ""
                        spatial_ref_sys = ""
                        spatial_res = ""
                        if 'Rast' in str(column_type):
                            geom_col = "rast"
                            spatial_res = engine.execute(f'SELECT ST_PixelWidth({geom_col}), ST_PixelHeight({geom_col}) from {schema}.{table_name}').first()
                            if spatial_res:
                                spatial_res = spatial_res[0]
                                
                        spatial_ref_sys = engine.execute(f'SELECT ST_SRID({geom_col}) FROM {schema}.{table_name}').first()
                        if spatial_ref_sys:
                            spatial_ref_sys = spatial_ref_sys[0]
                        json_string = engine.execute(f'SELECT ST_AsGeoJSON(ST_Envelope(ST_Union(ST_Envelope({geom_col})))) FROM {schema}.{table_name}').first()
                        if json_string:
                            json_dict = json.loads(json_string[0])
                            X = [pos[0] for pos in json_dict['coordinates'][0]]
                            Y = [pos[1] for pos in json_dict['coordinates'][0]]
                            spatial_ext = (min(X), min(Y), max(X), max(Y))
                        geo_metadata['spatial_extent'] = str(spatial_ext)
                        geo_metadata['spatial_resolution'] = str(spatial_res)
                        geo_metadata['spatial_reference_system'] = str(spatial_ref_sys)
                        
            table_metadata = {
                'no_of_records': count,
                'no_of_attributes': len(cols_list),
                'is_geo': is_geo,
                'geo_metadata': geo_metadata,
                'format': DATABASE_FORMAT
            }
            return table_metadata

        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            log.error(error)
            raise ValidationError(_(error))
        except Exception as e:
            log.error(e)
            raise e
