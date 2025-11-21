class Exceptions(Exception):
    def __init__(self, message, error_code):
        self.message = message
        self.error_code = error_code

    def __str__(self):
        return f"[{self.error_code}] {self.message}."


class NotFound(Exceptions):
    code = 'NOT_FOUND'
    message = 'Entity not found'

    def __init__(self, detail=None):
        if detail:
            self.message = detail
        super().__init__(self.message, self.code)


class BadLogin(Exceptions):
    code = 'BAD_LOGIN'
    message = 'Username or password is incorrect'

    def __init__(self):
        super().__init__(self.message, self.code)


class AlreadyLogin(Exceptions):
    code = 'ALREADY_LOGIN'
    message = 'You are currently logged in'

    def __init__(self):
        super().__init__(self.message, self.code)


class Unauthorized(Exceptions):
    code = 'UNAUTHORIZED'
    message = 'Not authenticated'

    def __init__(self, detail=None):
        if detail:
            self.message = detail
        super().__init__(self.message, self.code)


class Forbidden(Exceptions):
    code = 'FORBIDDEN'
    message = 'You are not allowed to perform this action'

    def __init__(self, detail=None):
        if detail:
            self.message = detail
        super().__init__(self.message, self.code)


class Conflict(Exceptions):
    code = 'CONFLICT'
    message = 'Entity already exists'

    def __init__(self, detail=None):
        if detail:
            self.message = detail
        super().__init__(self.message, self.code)


class BadRequest(Exceptions):
    code = 'BAD_REQUEST'
    message = 'Bad request'

    def __init__(self, detail=None):
        if detail:
            self.message = detail
        super().__init__(self.message, self.code)


class ValidationError(Exceptions):
    code = 'VALIDATION_ERROR'
    message = 'Validation error'

    def __init__(self, detail=None):
        if detail:
            self.message = detail
        super().__init__(self.message, self.code)


class HTTPException(Exceptions):
    code = 'HTTP_ERROR'
    message = 'HTTP error occurred'

    def __init__(self, status_code, detail=None):
        self.status_code = status_code
        if detail:
            self.message = detail
        super().__init__(self.message, self.code)