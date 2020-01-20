from flask import abort, make_response, jsonify


def abort_func(status_code, message, success_state):
    return abort(make_response(jsonify({
        "error": message,
        "success": success_state,
        "status": str(status_code)
    }), status_code))


def validate_field(field, field_name):
    if not field or field == " ":
        return abort_func(400,
                          f"{field_name} field is missing or empty",
                          False)
