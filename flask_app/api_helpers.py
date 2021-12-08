import functools
import psycopg2
from decimal import Decimal
from flask import jsonify
from psycopg2.extras import RealDictCursor

FIELD_TYPES = {'lastname': 'str',
               'firstname': 'str',
               'patronym': 'str',
               'birthyear': 'int',
               'id': 'int',
               'salary': 'Decimal',
               'jobname': 'str',
               'company': 'str',
               'department': 'str',
               'search_id': 'int'}
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


def error_handler(func):
    @functools.wraps(func)
    def decorated(*args, **kwargs):
        try:
            output = func(*args, **kwargs)
            return jsonify({'result': output})
        except Exception as e:
            return jsonify({'error': str(e)})
    return decorated


def validate_types(func, field_types=FIELD_TYPES):
    @functools.wraps(func)
    def wrapper(args):
        for field_name in field_types.keys():
            value = args.get(field_name)
            if value:
                if field_types[field_name] == 'int':
                    try:
                        int(value)
                    except:
                        raise TypeError(field_name + ' must be int, got ' + type(value).__name__)
                elif field_types[field_name] == 'Decimal':
                    try:
                        Decimal(value)
                    except:
                        raise TypeError(field_name + ' must be Decimal, got ' + type(value).__name__)
        return func(args)
    return wrapper


@validate_types
def assemble_add_request(args):
    params = []
    query = """INSERT INTO employees (lastname, firstname, patronym, birthyear, 
                                      id, salary, jobname, company, department)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
               RETURNING id;"""
    field_names = list(FIELD_TYPES.keys())
    for field_name in field_names[:-1]:
        if args.get(field_name):
            params.append(args.get(field_name))
        else:
            raise Exception('One or more required parameters missing:' + field_name)
    return query, params


@validate_types
def assemble_update_request(args):
    params = []
    search_id = args.get('search_id')
    if not search_id:
        raise Exception('No employee id (search_id) found in request')
    query = "SELECT * FROM employees WHERE id=(%s)"
    old_data = db_request(query, (search_id, ))
    if not old_data:
        raise Exception('No employee found with id ' + search_id)
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
    return query, params



@validate_types
def assemble_delete_request(args):
    params = []
    query = "SELECT * FROM employees WHERE "
    for field_name in FIELD_TYPES.keys():
        if args.get(field_name):
            query = query + field_name + '=(%s) AND '
            params.append(args.get(field_name))
    if not params:
        raise Exception('No parameters specified')
    query = query[:-4]
    employees = db_request(query, params)
    query = "DELETE " + query[8:] + 'RETURNING id'
    return query, params, len(employees)
