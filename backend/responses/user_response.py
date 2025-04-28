from enum import Enum


class UserErrorResponse(Enum):
    NOT_FOUND = {
        "message": "User not found.",
        "status_code": 404
    }
    MISSING_FIELDS = {
        "message": "Missing required fields: name, email, and/or password.",
        "status_code": 400
    }
    UNEXPECTED_ERROR = {
        "message": "An unexpected error occurred.",
        "status_code": 500
    }


class UserSuccessResponse(Enum):
    CREATED = {
        "message": "User created successfully.",
        "status_code": 201
    }
    RETRIEVED = {
        "message": "User retrieved successfully.",
        "status_code": 200
    }
    LIST_RETRIEVED = {
        "message": "Users retrieved successfully.",
        "status_code": 200
    }
    UPDATED = {
        "message": "User updated successfully.",
        "status_code": 200
    }
    DELETED = {
        "message": "User deleted successfully.",
        "status_code": 200
    }
