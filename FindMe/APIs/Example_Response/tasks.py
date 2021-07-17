task_added_response = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {
                    "status": "OK",
                    "message": "Task Created"
                }
            }
        },
    },
    401: {
        "description": "Not Authorized",
        "content": {
            "application/json": {
                "example": {"details": "Not Authorized"}
            }
        },
    },
}
task_completed_response = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {
                    "status": "OK",
                    "message": "Task Created"
                }
            }
        },
    },
    401: {
        "description": "Not Authorized",
        "content": {
            "application/json": {
                "example": {"details": "Not Authorized"}
            }
        },
    },
}
task_get_response = {
    401: {
        "description": "Not Authorized",
        "content": {
            "application/json": {
                "example": {"details": "Not Authorized"}
            }
        },
    },
}
