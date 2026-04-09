from rest_framework.views import exception_handler


def library_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return response

    detail = response.data
    if isinstance(detail, dict) and "detail" in detail:
        message = detail["detail"]
    elif isinstance(detail, dict):
        message = "Validation error"
    else:
        message = detail

    response.data = {
        "error": {
            "message": message,
            "details": detail,
            "status_code": response.status_code,
        }
    }
    return response
