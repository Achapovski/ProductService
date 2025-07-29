from dataclasses import dataclass

from grpc import StatusCode


@dataclass
class ErrorDetails:
    SERVER_ERROR: str = "Server error."
    PERMISSION_DENIED: str = "Permission denied."
    BAD_REQUEST: str = "Bad request."
    NOT_FOUND: str = "Entity not found"


GRPC_TO_HTTP = {
    StatusCode.OK: 200,
    StatusCode.NOT_FOUND: 404,
    StatusCode.ALREADY_EXISTS: 409,
    StatusCode.INVALID_ARGUMENT: 422,
    StatusCode.PERMISSION_DENIED: 403,
    StatusCode.UNAUTHENTICATED: 401,
    StatusCode.UNAVAILABLE: 503,
    StatusCode.INTERNAL: 500,
}
