from enum import Enum


class LogoutSuccessResponse(Enum):
    LOGOUT_SUCCESS = {
        "message": "Logout successful.",
        "status_code": 200
    }


class LogoutErrorResponse(Enum):
    UNEXPECTED_ERROR = {
        "message": "Unexpected error during logout.",
        "status_code": 500
    }
