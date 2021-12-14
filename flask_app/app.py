from flask import Flask, jsonify, redirect, render_template, request
from simplejson import JSONEncoder
from api_helpers import *
from exception_handlers import *

app = Flask(__name__)
app.json_encoder = JSONEncoder


@app.route("/")
def show_employee_list():
    employees = db_request('SELECT * FROM employees')
    return render_template('list.html', employees=employees)


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


@app.route("/profile/<employee_id>")
def show_employee_profile(employee_id):
    employee_data = db_request('SELECT * FROM employees WHERE id = (%s)', (employee_id, ))
    if len(employee_data):
        return render_template('profile.html', data=employee_data[0])
    return render_template('404.html'), 404


@app.route("/profile/<employee_id>/edit")
def edit_employee_profile(employee_id):
    employee_data = db_request('SELECT * FROM employees WHERE id = (%s)', (employee_id, ))
    if len(employee_data):
        return render_template('edit_profile.html', data=employee_data[0])
    return render_template('404.html'), 404


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


@app.route("/api/v1/employees", methods=['GET'])
@api_error_handler
def api_read_employees():
    args = request.args
    if not args:
        return db_request('SELECT * FROM employees'), 200
    employees = db_request(*assemble_read_request(args))
    if not employees:
        raise NotFoundException('No employees found')
    return employees, 200


@app.route("/api/v1/employees", methods=['POST'])
@api_error_handler
def api_add_employee():
    args = request.args
    db_request(*assemble_add_request(args))
    return "", 201


@app.route("/api/v1/employees/<employee_id>", methods=['PATCH'])
@api_error_handler
def api_update_employee(employee_id):
    args_dict = request.args
    query, params = assemble_update_request(args_dict, employee_id)
    db_request(query, params)
    return "", 204


@app.route("/api/v1/employees/<employee_id>", methods=['DELETE'])
@api_error_handler
def api_delete_employee(employee_id):
    query = "SELECT * FROM employees WHERE id=(%s)"
    old_data = db_request(query, (employee_id,))
    if not old_data:
        raise NotFoundException('No employee found with id ' + employee_id)
    query = "DELETE FROM employees WHERE id=(%s) RETURNING id"
    db_request(query, (employee_id,))
    return "", 204


app.register_error_handler(405, handle_method_not_allowed)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
