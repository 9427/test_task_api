from decimal import Decimal, InvalidOperation
from psycopg2.errors import UniqueViolation
from flask import jsonify
import functools

FIELD_TYPES = {'lastname': 'str',
               'firstname': 'str',
               'patronym': 'str',
               'birthyear': 'int',
               'id': 'int',
               'salary': 'Decimal',
               'jobname': 'str',
               'company': 'str',
               'department': 'str'}


class BadRequestException(Exception):
    pass


class NotFoundException(Exception):
    pass


def api_error_handler(func):
    @functools.wraps(func)
    def decorated(*args, **kwargs):
        try:
            output, output_code = func(*args, **kwargs)
            return jsonify({'result': output}), output_code
        except BadRequestException as e:
            return jsonify({'error': str(e)}), 400
        except UniqueViolation as e:
            return jsonify({'error': str(e)}), 400
        except NotFoundException as e:
            return jsonify({'error': str(e)}), 404
    return decorated


def validate_types(func, field_types=FIELD_TYPES):
    @functools.wraps(func)
    def wrapper(validated_args, *args):
        for field_name in field_types.keys():
            value = validated_args.get(field_name)
            if value:
                if field_types[field_name] == 'int':
                    try:
                        int(value)
                    except ValueError:
                        raise BadRequestException(field_name + ' must be int, got ' + type(value).__name__)
                elif field_types[field_name] == 'Decimal':
                    try:
                        Decimal(value)
                    except InvalidOperation:
                        raise BadRequestException(field_name + ' must be Decimal, got ' + type(value).__name__)
        return func(validated_args, *args)
    return wrapper


def handle_method_not_allowed(e):
    return {'error': str(e)}, 405
