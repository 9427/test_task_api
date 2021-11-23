from flask import Flask, jsonify, redirect, render_template, request
from simplejson import JSONEncoder
from api_helpers import *

app = Flask(__name__)
app.json_encoder = JSONEncoder


@app.route("/")
def show_employee_list():
    employees = db_request('SELECT * FROM employees')
    return render_template('list.html', employees=employees)


@app.route("/api/v1/employees/all")
@error_handler
def api_all_employees():
    employees = db_request('SELECT * FROM employees')
    return employees


@app.route("/api/v1/employees", methods=['GET'])
@error_handler
def api_filter_employees():
    filter_args = request.args
    params = []
    query = "SELECT * FROM employees WHERE "
    filter_fields = ['id', 'firstname', 'lastname', 'patronym']
    for field_name in filter_fields:
        if filter_args.get(field_name):
            query = query + field_name + '=(%s) AND '
            params.append(filter_args.get(field_name))
    if not params:
        raise Exception('No valid filters in request')
    query = query[:-4] + ';'
    employees = db_request(query, params)
    if not employees:
        raise Exception('No employees found')
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
    args = request.args
    db_request(*assemble_add_request(args))
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


@app.route("/api/v1/employees/update", methods=['GET'])
@error_handler
def api_update_employee():
    args = request.args
    query, params = assemble_update_request(args)
    upd_id = db_request(query, params)
    return "Employee data successfully updated: " + str(upd_id)


@app.route("/profile/<employee_id>/delete")
def delete_employee_profile(employee_id):
    query = "DELETE FROM employees WHERE id = (%s) RETURNING id"
    db_request(query, (employee_id, ))
    return redirect('/')

@app.route("/api/v1/employees/delete", methods=['GET'])
@error_handler
def api_delete_employee():
    args = request.args
    query, params, amount = assemble_delete_request(args)
    if amount == 1:
        del_data = db_request(query, params)
        return "Employee data successfully deleted: " + str(del_data)
    elif amount:
        raise Exception('Can only delete employees one at a time; request matched more than one employee')
    else:
        raise Exception('No employees found')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
