from flask import jsonify
from werkzeug.exceptions import HTTPException


def handle_exception(e):
    if isinstance(e, HTTPException):
        response = {
            "error": {
                "code": e.code,
                "name": e.name,
                "description": e.description,
            }
        }
        return jsonify(response), e.code

    response = {
        "error": {
            "code": 500,
            "name": "Internal Server Error",
            "description": str(e),
        }
    }
    return jsonify(response), 500


class APIError(Exception):
    def __init__(self, status_code, error_code, message):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message


def handle_api_error(e):
    response = {"error": {"code": e.error_code, "message": e.message}}
    return jsonify(response), e.status_code
