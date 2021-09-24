from sqlalchemy import create_engine, inspect

class PostgresHandle:
    def __init__(self):
        self.db = ""
        self.schema = ""
        self.db_uri = ""
    
    def fetch_db(self):
        '''
        To fetch the db details
        '''
        try:
            return self.db_uri.split('?')[0].split('/')[-1]

        except Exception as e:
            print('psycopg2 Error')
        
    def fetch_schema(self,db=None):
        '''
        To fetch the schemas of the db
        '''
        try:
            engine = create_engine(self.db_uri)
            inspector = inspect(engine)
            schemas = inspector.get_schema_names()
            return schemas 

        except Exception as e:
            print(e)
        
    def fetch_tables(self, db=None, schema=None):
        """
        To fetch the tables of db and schema
        """
        try:
            engine = create_engine(self.db_uri)
            inspector = inspect(engine)
            tables = inspector.get_table_names(schema='public')
            return tables

        except Exception as e:
            print(e)
        
    def fetch_metadata(self,db=None, schema=None, table_name=None):
        '''
        To fetch metadata of the table
        '''
        try:
            engine = create_engine(self.db_uri)
            inspector = inspect(engine)
            columns = inspector.get_columns(table_name, schema=schema)
            cols_list = list(map(lambda x:x['name'],columns))
            return cols_list

        except Exception as e:
            print(e)
        
    def __to_dict__(self):
        pass

if __name__ == "__main__":
    PostgresHandle()