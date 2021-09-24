from postgres_handle import PostgresHandle

def fetch_details(db_type):
    if db_type == 'postgres':
        ps = PostgresHandle()
    #   print(ps.fetch_db())
    # print(ps.fetch_schema)
    # print(ps.fetch_tables())
    print(ps.fetch_metadata())

fetch_details()