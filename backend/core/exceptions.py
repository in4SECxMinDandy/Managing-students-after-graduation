"""Custom exceptions for the application."""
from typing import Any


class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}


class NotFoundError(AppException):
    """Resource not found."""

    def __init__(self, resource: str, identifier: str | int) -> None:
        super().__init__(
            message=f"{resource} with identifier '{identifier}' not found.",
            details={"resource": resource, "identifier": identifier},
        )


class AlreadyExistsError(AppException):
    """Resource already exists."""

    def __init__(self, resource: str, identifier: str | int) -> None:
        super().__init__(
            message=f"{resource} with identifier '{identifier}' already exists.",
            details={"resource": resource, "identifier": identifier},
        )


class ValidationError(AppException):
    """Validation error."""

    def __init__(self, message: str, field: str | None = None) -> None:
        details: dict[str, Any] = {}
        if field:
            details["field"] = field
        super().__init__(message=message, details=details)


class UnauthorizedError(AppException):
    """Unauthorized access."""

    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__(message=message)


class ForbiddenError(AppException):
    """Forbidden access."""

    def __init__(self, message: str = "Access forbidden") -> None:
        super().__init__(message=message)


class BusinessRuleError(AppException):
    """Business rule violation."""

    def __init__(self, rule: str, message: str) -> None:
        super().__init__(
            message=f"Business rule '{rule}' violated: {message}",
            details={"rule": rule},
        )
