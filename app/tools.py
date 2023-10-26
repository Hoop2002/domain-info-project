import werkzeug
import json


def valid_response(data, status=200):
    response_info = {"jsonrpc": "2.0", "id": None, "result": data}

    return werkzeug.wrappers.Response(
        status=status,
        content_type="application/json; charset=utf-8",
        response=json.dumps(response_info),
    )


def invalid_response(message=None, status=400):
    info_err = {"message": message if message else "Wrong arguments"}

    response_info = {"jsonrpc": "2.0", "id": None, "error": info_err}

    return werkzeug.wrappers.Response(
        status=status,
        content_type="application/json; charset=utf-8",
        response=json.dumps(response_info),
    )
