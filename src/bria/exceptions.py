class BriaError(Exception):
    """Base class for all Bria SDK exceptions."""
    pass


class AuthenticationError(BriaError):
    """Raised when authentication fails (401/403)."""
    pass


class RateLimitError(BriaError):
    """Raised when hitting API rate limits (429)."""
    pass


class InvalidRequestError(BriaError):
    """Raised when the request is invalid (400/422)."""
    pass


class ServerError(BriaError):
    """Raised for 5xx errors from Bria API."""
    pass

class NotFoundError(BriaError):
    """Raised when a request_id is not found (404)."""
    pass