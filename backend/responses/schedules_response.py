from enum import Enum


class ScheduleErrorResponse(Enum):
    NOT_FOUND = {
        "message": "Schedule not found.",
        "status_code": 404
    }
    UNEXPECTED_ERROR = {
        "message": "An unexpected error occurred.",
        "status_code": 500
    }
    MISSING_FIELDS = {
        "message": "Missing required schedule fields.",
        "status_code": 400
    }
    INVALID_PAVILION = {
        "message": "Invalid pavilion specified.",
        "status_code": 400
    }
    SCHEDULE_ALREADY_EXISTS = {
        "message": "A schedule with the same details already exists.",
        "status_code": 400
    }
    INVALID_DAY = {
        "message": "Invalid day provided.",
        "status_code": 400
    }
    INVALID_BLOCK = {
        "message": "Invalid block specified.",
        "status_code": 400
    }
    INVALID_CLASSROOM = {
        "message": "Invalid classroom number.",
        "status_code": 400
    }
    UNAUTHORIZED_ACCESS = {
        "message": "You are not authorized to access this schedule.",
        "status_code": 403
    }


class ScheduleSuccessResponse(Enum):
    CREATED = {
        "message": "Schedule created successfully.",
        "status_code": 201
    }
    RETRIEVED = {
        "message": "Schedule retrieved successfully.",
        "status_code": 200
    }
    UPDATED = {
        "message": "Schedule updated successfully.",
        "status_code": 200
    }
    DELETED = {
        "message": "Schedule deleted successfully.",
        "status_code": 200
    }
    LIST_RETRIEVED = {
        "message": "Schedules list retrieved successfully.",
        "status_code": 200
    }
    VALIDATION_PASSED = {
        "message": "Schedule validation passed.",
        "status_code": 200
    }

