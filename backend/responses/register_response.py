from enum import Enum


class RegisterErrorResponse(Enum):
    MISSING_CREDENTIALS = {
        "message": "Please provide both email and password.",
        "status_code": 400
    }
    EMAIL_ALREADY_EXISTS = {
        "message": "An account with this email address already exists.",
        "status_code": 409
    }
    UNEXPECTED_ERROR = {
        "message": "An unexpected error occurred during registration.",
        "status_code": 500
    }


class RegisterSuccessResponse(Enum):
    REGISTRATION_SUCCESS = {
        "message": "Registration successful.",
        "status_code": 201
    }
