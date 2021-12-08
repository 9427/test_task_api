import csv
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
    query = """SELECT * 
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_TYPE = 'BASE TABLE'
        AND TABLE_NAME = 'employees'"""
    pg_cur.execute(query)
    db_exists = pg_cur.fetchall()
    if not db_exists:
        query = """CREATE TABLE employees (
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

        with open('init_data.csv', 'r') as f:
            query = """INSERT INTO employees (lastname, firstname, patronym, birthyear, 
                                         id, salary, jobname, company, department)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            reader = csv.reader(f)

            for data in reader:
                pg_cur.execute(query, data)
            pg_conn.commit()

    pg_cur.close()
    pg_conn.close()

