from http import HTTPStatus
from sqlalchemy.exc import IntegrityError  # noqa
from starlette.exceptions import HTTPException


class HTTPExceptionBadRequest(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=detail
        )


class HTTPExceptionMethodNotAllowed(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=HTTPStatus.METHOD_NOT_ALLOWED,
            detail=detail
        )


class HTTPExceptionUnprocessableEntity(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=detail
        )


class HTTPExceptionInternalServerError(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=detail
        )
