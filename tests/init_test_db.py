import psycopg2


conn_info = {
    'database': 'db',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'db',
    'port': '5432'
}

if __name__ == '__main__':
    pg_conn = psycopg2.connect(**conn_info)
    pg_cur = pg_conn.cursor()
    query = """DROP TABLE IF EXISTS employees;
    CREATE TABLE employees (
    firstname VARCHAR(30),
    lastname VARCHAR(30),
    patronym VARCHAR(30),
    birthyear SMALLINT,
    id INTEGER PRIMARY KEY,
    salary DECIMAL,
    jobname VARCHAR(50),
    company VARCHAR(50),
    department VARCHAR(50)
    );
    """
    pg_cur.execute(query)
    pg_conn.commit()
    pg_cur.close()
    pg_conn.close()
