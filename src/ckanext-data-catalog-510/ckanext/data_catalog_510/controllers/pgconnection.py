from psycopg2 import connect

def get_connection():
    # Update connection string information
    host = ""
    dbname = ""
    user = ""
    password = ""
    sslmode = "require"
    # connect_str = "dbname={dbname} host='localhost' user='xxx' password='xxx'".format(dbname)
    conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
    return connect(conn_string)