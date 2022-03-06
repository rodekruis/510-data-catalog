from azure.storage.filedatalake import DataLakeServiceClient
from sqlalchemy import create_engine, inspect

from .config import ENV


class DatalakeController:
    def __init__(self) -> None:
        self.service_client = ''
        self.storage_account_name = ENV['CKAN__DATALAKE_ACCOUNT_NAME']
        self.storage_account_key = ENV['CKAN__DATALAKE_ACCOUNT_KEY']

    def create_client(self):
        try:
            service_client = DataLakeServiceClient(
                account_url="{}://{}.dfs.core.windows.net".format(
                            "https", self.storage_account_name),
                credential=self.storage_account_key)
            self.service_client = service_client
        except Exception as e:
            raise e

    def find_file_or_directory(self, container, filepath):
        try:
            file_system_client = self.service_client.get_file_system_client(
                file_system=container)
            paths = list(file_system_client.get_paths(
                path="/", recursive=True))
            path_name_list = [path.name for path in paths]
            if filepath in path_name_list:
                # print(filepath, path_name_list.index(filepath))
                return True
            else:
                return False
        except Exception as e:
            raise e


class DatabaseController:
    def __init__(self):
        self.db_uri = ''
        self.db_type = ''

    def create_client(self, db_type, db_name):
        self.db_type = db_type
        try:
            conn_details = []
            if db_type == "postgres":
                conn_details = ENV['CKAN__POSTGRESQL_DB_CONNECTIONS']
            elif db_type == "mysql":
                conn_details = ENV['CKAN__MYSQL_DB_CONNECTIONS']
            elif db_type == "azuresql":
                conn_details = ENV['CKAN__AZURESQL_DB_CONNECTIONS']
            else:
                raise Exception("Unsupported database type: " + db_type)

            for conn in conn_details:
                conn_db_name = conn['url'].split('/')[-1].split('?')[0]
                if conn_db_name == db_name:
                    self.db_uri = conn['url']
                else:
                    raise Exception("Unsupported database name: " + db_name)
        except Exception as e:
            raise e

    def find_table(self, db_schema, db_table):
        try:
            if self.db_uri:
                engine = create_engine(self.db_uri)
                inspector = inspect(engine)
                schemas = [x for x in inspector.get_schema_names()]
                if db_schema not in schemas:
                    return False
                else:
                    tables = [x for x in inspector.get_table_names(
                        schema=db_schema)]
                    if db_table not in tables:
                        return False
                    else:
                        return True
            else:
                raise Exception("DatabaseController not initialized.")
        except Exception as e:
            raise e
