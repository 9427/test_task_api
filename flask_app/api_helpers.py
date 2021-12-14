import psycopg2
from psycopg2.extras import RealDictCursor
from exception_handlers import *

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


@validate_types
def assemble_read_request(args):
    params = []
    field_names = []
    query = "SELECT * FROM employees WHERE "
    filter_fields = ['id', 'firstname', 'lastname', 'patronym']
    for field_name in filter_fields:
        if args.get(field_name):
            field_names.append(field_name + '=(%s)')
            params.append(args.get(field_name))
    if not params:
        raise BadRequestException('No valid filters in request')
    query = query + (' AND '.join(field_names))
    return query, params


@validate_types
def assemble_add_request(args):
    params = []
    query = """INSERT INTO employees (lastname, firstname, patronym, birthyear, 
                                      id, salary, jobname, company, department)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
               RETURNING id;"""
    field_names = list(FIELD_TYPES.keys())
    for field_name in field_names:
        if args.get(field_name):
            params.append(args.get(field_name))
        else:
            raise BadRequestException('One or more required parameters missing:' + field_name)
    return query, params


@validate_types
def assemble_update_request(args, search_id):
    params = []
    query = "SELECT * FROM employees WHERE id=(%s)"
    old_data = db_request(query, (search_id, ))
    if not old_data:
        raise NotFoundException('No employee found with id ' + search_id)
    query = """
        UPDATE employees
        SET firstname = (%s),
        lastname = (%s),
        patronym = (%s),
        birthyear = (%s),
        id = (%s),
        salary = (%s),
        jobname = (%s),
        company = (%s),
        department = (%s)
        WHERE id = (%s)
        RETURNING id"""
    for field_name in FIELD_TYPES.keys():
        if args.get(field_name):
            params.append(args.get(field_name))
        else:
            params.append(old_data[0][field_name])
    params.append(search_id)
    return query, params


def assemble_delete_request(search_id):
    query = "SELECT * FROM employees WHERE id=(%s)"
    old_data = db_request(query, (search_id,))
    if not old_data:
        raise NotFoundException('No employee found with id ' + search_id)
    params = (search_id,)
    query = "DELETE * FROM employees WHERE id=(%s) RETURNING id"
    return query, params
