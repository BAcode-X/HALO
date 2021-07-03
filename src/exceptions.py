class InvalidCreaditioal(Exception):
    def __init__(self, message):
        super().__init__(message)


class TypeDoesNotExist(Exception):
    def __init__(self, message):
        super().__init__(message)


class TypeAlreadyExist(Exception):
    def __init__(self, message):
        super().__init__(message)


class DuplicatedPrimaryKey(Exception):
    def __init__(self, message):
        super().__init__(message)


class ForbidenAccess(Exception):
    def __init__(self, message):
        super().__init__(message)


class MultipleValueReturned(Exception):
    def __init__(self, message):
        super().__init__(message)


class UniqueConstraintError(Exception):
    def __init__(self, message):
        super().__init__(message)
