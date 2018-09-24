"""General exceptions that can be risen in this project."""


class ServerBaseException(Exception):
    pass


class ServerException(ServerBaseException):
    pass


class CalculatorException(ServerBaseException):
    pass


class CalculatorLexicalException(CalculatorException):
    pass


class CalculatorSyntacticalException(CalculatorException):
    pass
