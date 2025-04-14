from enum import Enum


class LoginErrorResponse(Enum):
    INVALID_CREDENTIALS = {
        "message": "Invalid email or password.",
        "status_code": 401
    }
    UNEXPECTED_ERROR = {
        "message": "An unexpected error occurred during login.",
        "status_code": 500
    }


class LoginSuccessResponse(Enum):
    LOGIN_SUCCESS = {
        "message": "Login successful.",
        "status_code": 200
    }
    ALREADY_LOGGED_IN = {
        "message": "You are still logged in.",
        "status_code": 200
    }
