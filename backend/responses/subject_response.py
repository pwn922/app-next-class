from enum import Enum


class SubjectErrorResponse(Enum):
    NOT_FOUND = {
        "message": "Subject not found.",
        "status_code": 404
    }
    MISSING_FIELDS = {
        "message": "Missing required fields: name and/or code.",
        "status_code": 400
    }
    UNEXPECTED_ERROR = {
        "message": "An unexpected error occurred.",
        "status_code": 500
    }


class SubjectSuccessResponse(Enum):
    CREATED = {
        "message": "Subject created successfully.",
        "status_code": 201
    }
    RETRIEVED = {
        "message": "Subject retrieved successfully.",
        "status_code": 200
    }
    LIST_RETRIEVED = {
        "message": "Subjects retrieved successfully.",
        "status_code": 200
    }
    UPDATED = {
        "message": "Subject updated successfully.",
        "status_code": 200
    }
    DELETED = {
        "message": "Subject deleted successfully.",
        "status_code": 200
    }
