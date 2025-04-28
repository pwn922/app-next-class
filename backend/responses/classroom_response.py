from enum import Enum


class ClassroomErrorResponse(Enum):
    NOT_FOUND = {
        "message": "Classroom not found.",
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


class ClassroomSuccessResponse(Enum):
    RETRIEVED = {
        "message": "Classroom retrieved successfully.",
        "status_code": 200
    }
    UPDATED = {
        "message": "Classroom updated successfully.",
        "status_code": 200
    }
    DELETED = {
        "message": "Classroom deleted successfully.",
        "status_code": 204
    }
    CREATED = {
        "message": "Classroom created successfully.",
        "status_code": 201
    }
    LIST_RETRIEVED = {
        "message": "Classroom list retrieved successfully.",
        "status_code": 200
    }
