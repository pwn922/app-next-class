from flask import jsonify, make_response


def create_response(
        success: bool,
        message: str,
        status_code: int,
        **extra_fields
        ):
    response = {
        "success": success,
        "message": message
    }
    response.update(extra_fields)
    return make_response(jsonify(response), status_code)


def success_response(
        message_key: str,
        status_code,
        data: dict = None,
        ):
    response = create_response(
        success=True,
        message=message_key or "",
        status_code=status_code
    )
    response_data = response.get_json()
    response_data.update({"data": data or {}})
    return make_response(jsonify(response_data), status_code)


def error_response(
        error_code: str,
        status_code,
        message: str = None,
        ):
    response = create_response(
        success=False,
        message=message or "Unknown error",
        status_code=status_code
    )
    response_data = response.get_json()
    response_data.update({"error_code": error_code})
    return make_response(jsonify(response_data), status_code)
