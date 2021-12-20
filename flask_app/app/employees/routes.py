from flask import Blueprint, request
from .api_helpers import *
from ..db import *
from ..exception_handlers import *
from . import employees


@employees.route("/api/v1/employees", methods=['GET'])
@api_error_handler
def api_read_employees():
    args = request.args
    if not args:
        return db_request('SELECT * FROM employees'), 200
    employees = db_request(*assemble_read_request(args))
    if not employees:
        raise NotFoundException('No employees found')
    return employees, 200


@employees.route("/api/v1/employees", methods=['POST'])
@api_error_handler
def api_add_employee():
    args = request.args
    db_request(*assemble_add_request(args))
    return "", 201


@employees.route("/api/v1/employees/<employee_id>", methods=['PATCH'])
@api_error_handler
def api_update_employee(employee_id):
    args_dict = request.args
    query, params = assemble_update_request(args_dict, employee_id)
    db_request(query, params)
    return "", 204


@employees.route("/api/v1/employees/<employee_id>", methods=['DELETE'])
@api_error_handler
def api_delete_employee(employee_id):
    query = "SELECT * FROM employees WHERE id=(%s)"
    old_data = db_request(query, (employee_id,))
    if not old_data:
        raise NotFoundException('No employee found with id ' + employee_id)
    query = "DELETE FROM employees WHERE id=(%s) RETURNING id"
    db_request(query, (employee_id,))
    return "", 204
