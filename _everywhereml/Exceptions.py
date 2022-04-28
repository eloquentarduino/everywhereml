class MCUMLError(Exception):
    """
    Library-specific exceptions base class
    """
    pass


class BoardQueryNotFoundError(MCUMLError):
    """
    No board can be found that matches the given query
    """
    pass


class PortQueryNotFoundError(MCUMLError):
    """
    No port can be found that matches the given query
    """
    pass


class InvalidChoiceError(MCUMLError):
    """
    The user selected an invalid choice
    """
    pass