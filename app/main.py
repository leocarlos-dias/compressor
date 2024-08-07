from flask import Flask
from app.routes import api
from app.utils.error_handler import handle_exception, APIError, handle_api_error


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api)
    app.register_error_handler(Exception, handle_exception)
    app.register_error_handler(APIError, handle_api_error)
    return app


app = create_app()
