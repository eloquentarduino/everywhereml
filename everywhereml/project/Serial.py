class Serial:
    """
    Interact with the serial monitor
    """
    def __init__(self, port, baudrate):
        """
        Constructor
        :param port: str serial port
        :param baudrate: int
        """
        assert isinstance(port, str) and len(port) > 1, 'port MUST be a valid string'
        assert isinstance(baudrate, int) and baudrate > 0, 'baudrate MUST be a positive number'

        self.port = port
        self.baudrate = baudrate