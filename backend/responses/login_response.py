from enum import Enum


class LoginErrorResponse(Enum):
    AUTH_ERROR = {
        "message": "An error occurred during the authentication process.",
        "status_code": 400
    }
    INVALID_STATE = {
        "message": "Invalid state parameter.",
        "status_code": 400
    }
    OAUTH2_ERROR = {
        "message": "OAuth2 authorization failed.",
        "status_code": 400
    }
    EXTERNAL_SERVICE_ERROR = {
        "message": "Unable to fetch information from external service.",
        "status_code": 502
    }
    UNEXPECTED_ERROR = {
        "message": "Unexpected internal error.",
        "status_code": 500
    }
    OAUTH2_FLOW_ERROR = {
        "message": "OAuth2 flow error.",
        "status_code": 400
    }
    INVALID_ID_TOKEN = {
        "message": "Invalid token.",
        "status_code": 400
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
