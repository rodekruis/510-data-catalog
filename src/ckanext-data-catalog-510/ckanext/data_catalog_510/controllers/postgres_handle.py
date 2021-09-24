from typing import final
import psycopg2.extras
from pgconnection import get_connection

class PostgresHandle:
    def __init__(self):
        # self.connection_string = "postgresql://azure_postgres_sql_db@ckan-test:l7#lJ9IWlSF1v00LCEXLe​@ckan-test.postgres.database.azure.com/azure_postgres_sql_db?sslmode=require"
        self.db = ""
        self.schema = ""

    def fetch_db(self):
        '''
        To fetch the db details
        '''
        try:
            db_conn = get_connection()
            return db_conn.info.dbname

        except Exception as e:
            print('psycopg2 Error')
        
        finally:
            db_conn.close()
    
    def fetch_schema(self,db=None):
        '''
        To fetch the schema of the db
        '''
        try:
            print('check2')
            db_conn = get_connection()
            cursor = db_conn.cursor()
            cursor.execute("SELECT current_schema();")

            return cursor.fetchone()[0]

        except Exception as e:
            print('psycopg2 Error')
        
        finally:
            cursor.close()
            db_conn.close()

    def fetch_metadata(self,schema=None):
        try:
            db_conn = get_connection()
            cursor = db_conn.cursor()
            cursor.execute("""select table_name from information_schema.tables \
                    WHERE table_schema='public'""")
            data = cursor.fetchall()
            data_list = []
            for row in data:
                data_list.append(row[0])
            return data_list
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            db_conn.close()
    
    def fetch_tables(self, db=None, schema=None):
        """
        Create and return a list of dictionaries with the
        schemas and names of tables in the database
        connected to by the connection argument.
        """
        try:
            db_conn = get_connection()
            cursor = db_conn.cursor()
            cursor.execute("""SELECT table_name FROM information_schema.tables
                WHERE table_schema = 'public'""")

            tables = cursor.fetchall()
            tables_list = []
            for table in tables:
                tables_list.append(table[0])
            # cursor.close()
            return tables_list

        except Exception as e:
            print('Error')
        
        finally:
            cursor.close()
            db_conn.close()

    def __to_dict__(self):
        pass

if __name__ == "__main__":
    PostgresHandle()