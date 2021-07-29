from logging import Logger, StreamHandler, Formatter, DEBUG, INFO


class Logger(Logger):
    """
    Custom logger
    """
    def __init__(self, name='ProjectLogger', level=DEBUG):
        """
        Init and configure
        :param name:
        """
        super().__init__(name)
        handler = StreamHandler()
        handler.setFormatter(Formatter('[%(levelname)s] %(message)s'))
        self.addHandler(handler)
        self.setLevel(level)
