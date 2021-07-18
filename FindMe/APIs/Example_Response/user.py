user_register_example_response = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "example": {
                    "status": "OK",
                    "message": "User Created"
                }
            }
        },
    },
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "example": {"details": "User already exist"}
            }
        },
    },
}

user_login_example_response = {
    400: {
        "description": "Bad Request",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Invalid ID/Password"
                }
            }
        },
    },
}

user_get_user_example_response = {
    401: {
        "description": "Not Authorized",
        "content": {
            "application/json": {
                "example": {"details": "Not Authorized"}
            }
        },
    },
}
