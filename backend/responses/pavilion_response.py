from enum import Enum


class PavilionErrorResponse(Enum):
    NOT_FOUND = {
        "message": "Pavilion not found.",
        "status_code": 404
    }
    MISSING_FIELDS = {
        "message": "Missing required fields.",
        "status_code": 400
    }
    UNEXPECTED_ERROR = {
        "message": "Unexpected internal error.",
        "status_code": 500
    }


class PavilionSuccessResponse(Enum):
    CREATED = {
        "message": "Pavilion created successfully.",
        "status_code": 201
    }
    RETRIEVED = {
        "message": "Pavilion retrieved successfully.",
        "status_code": 200
    }
    LIST_RETRIEVED = {
        "message": "Pavilions retrieved successfully.",
        "status_code": 200
    }
    UPDATED = {
        "message": "Pavilion updated successfully.",
        "status_code": 200
    }
    DELETED = {
        "message": "Pavilion deleted successfully.",
        "status_code": 204
    }
