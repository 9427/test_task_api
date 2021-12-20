from flask import Flask
from simplejson import JSONEncoder
from app.exception_handlers import handle_method_not_allowed


def create_app():
    app = Flask(__name__)
    app.json_encoder = JSONEncoder

    from app.employees import employees
    app.register_blueprint(employees)

    app.register_error_handler(405, handle_method_not_allowed)

    return app
