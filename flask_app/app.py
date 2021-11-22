import functools
import psycopg2
from decimal import Decimal
from flask import Flask, jsonify, redirect, render_template, request
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

CONN_INFO = {
    'database': 'db',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'db',
    'port': '5432'
}
FIELD_TYPES = {'lastname': 'str',
               'firstname': 'str',
               'patronym': 'str',
               'birthyear': 'int',
               'id': 'int',
               'salary': 'Decimal',
               'jobname': 'str',
               'company': 'str',
               'department': 'str'}

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
    # @functools.wraps(func)
    def decorated(func, args):
        try:
            for field_name in FIELD_TYPES.keys():
                value = args.get(field_name)
                if field_types[field_name] == 'int':
                    int(value)
                elif field_types[field_name] == 'Decimal':
                    Decimal(value)
            output = func(*args, **kwargs)
            return jsonify({'result': output})
        except Exception as e:
            return jsonify({'error': str(e)})
    return decorated

# @validate_types(FIELD_TYPES)
def form_add_request(args):
    params = []
    query = """INSERT INTO employees (lastname, firstname, patronym, birthyear, 
                                      id, salary, jobname, company, department)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
               RETURNING id;"""
    for field_name in FIELD_TYPES.keys():
        if args.get(field_name):
            params.append(args.get(field_name))
        else:
            raise Exception('One or more required parameters missing')
    return query, params

@app.route("/")
def show_employee_list():
    employees = db_request('SELECT * FROM employees')
    return render_template('list.html', employees=employees)


@app.route("/api/v1/employees/all")
@error_handler
def api_all_employees():
    employees = db_request('SELECT * FROM employees')
    return jsonify(employees)


@app.route("/api/v1/employees", methods=['GET'])
@error_handler
def api_filter_employees():
    filter_args = request.args()
    params = []
    query = "SELECT * FROM employees WHERE "
    filter_fields = ['id', 'firstname', 'lastname', 'patronym']
    for field_name in filter_fields:
        if filter_args.get(field_name):
            query = query + field_name + '=(%s) AND '
            params.append(filter_args.get(field_name))
    query = query[:-4] + ';'
    employees = db_request(query, params)
    return employees


@app.route('/add_profile')
def add_employee_profile():
    return render_template('add_profile.html')


@app.route('/add_profile/submit', methods=['POST'])
def submit_employee_new():
    if request.method == 'POST':
        data = request.form
    query = """INSERT INTO employees (lastname, firstname, patronym, birthyear, 
                                      id, salary, jobname, company, department)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
               RETURNING id;"""
    params = [i for i in data.values()]
    db_request(query, params)
    return redirect("/")


@app.route("/api/v1/employees/add", methods=['GET'])
@error_handler
def api_add_employee():
    db_request(*form_add_request(request.args))
    return "Employee successfully added"


@app.route("/profile/<employee_id>")
def show_employee_profile(employee_id):
    employee_data = db_request('SELECT * FROM employees WHERE id = (%s)', (employee_id, ))
    if len(employee_data):
        return render_template('profile.html', data=employee_data[0])
    return render_template('404.html')


@app.route("/profile/<employee_id>/edit")
def edit_employee_profile(employee_id):
    employee_data = db_request('SELECT * FROM employees WHERE id = (%s)', (employee_id, ))
    if len(employee_data):
        return render_template('edit_profile.html', data=employee_data[0])
    return render_template('404.html')


@app.route("/profile/<employee_id>/submit", methods=['POST'])
def submit_employee_edit(employee_id):
    if request.method == 'POST':
        data = request.form
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
    params = [i for i in data.values()] + [employee_id]
    db_request(query, params)
    return redirect("/profile/" + str(employee_id))


@app.route("/profile/<employee_id>/delete")
def delete_employee_profile(employee_id):
    query = "DELETE FROM employees WHERE id = (%s) RETURNING id"
    db_request(query, (employee_id, ))
    return redirect('/')

@app.route("/api/v1/employees/delete", methods=['GET'])
def api_delete_employee():
    params = request.args
    return "Employee successfully deleted"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)