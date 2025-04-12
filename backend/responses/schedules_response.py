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
        "status_code": 204
    }
    LIST_RETRIEVED = {
        "message": "Schedules list retrieved successfully.",
        "status_code": 200
    }
