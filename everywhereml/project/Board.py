class Board:
    """
    Abstraction of a microcontroller board
    """
    def __init__(self, fqbn, label, **kwargs):
        """
        Constructor
        :param fqbn: str fully-qualified board name
        :param label: str human-readable name
        :param kwargs: dict board-specific options
        """
        assert isinstance(fqbn, str) and len(fqbn) > 0, 'you MUST se a fqbn'
        assert label is None or isinstance(label, str), 'label MUST either be None or a string'

        self.fqbn = fqbn
        self.label = label or ''
        self.options = kwargs
