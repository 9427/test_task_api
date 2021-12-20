import psycopg2
from psycopg2.extras import RealDictCursor

CONN_INFO = {
    'database': 'db',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'db',
    'port': '5432'
}


def db_request(query, params=None):
    pg_conn = psycopg2.connect(**CONN_INFO)
    pg_cur = pg_conn.cursor(cursor_factory=RealDictCursor)
    pg_cur.execute(query, params)
    data = pg_cur.fetchall()
    pg_conn.commit()
    pg_conn.close()
    return data
