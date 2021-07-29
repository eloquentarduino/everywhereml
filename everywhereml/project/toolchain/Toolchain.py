class Toolchain:
    """
    Abstract toolchain class
    """
    def __init__(self, executable, cwd=None):
        """
        Constructor
        :param executable: str path to executable
        :param cwd: str path to current working directory
        """
        assert isinstance(executable, str) and len(executable) > 0, 'you MUST set an executable file'
        assert cwd is None or isinstance(cwd, str) and len(cwd) > 0, 'you MUST set a valid cwd'

        self.executable = executable
        self.cwd = cwd
        self.output = ''
        self.error = ''

    @property
    def is_successful(self):
        """
        Test if last command of toolchain was successful
        :return: bool
        """
        return self.error == ''

    @property
    def output_lines(self):
        """
        Get command output as lines
        """
        return [line.strip() for line in self.output.split("\n")]

    @property
    def error_lines(self):
        """
        Get command error as lines
        """
        return [line.strip() for line in self.error.split("\n")]

    def list_boards(self, query=None):
        """
        List available board
        :param query: str|None search query
        :return:
        """
        raise NotImplemented()

    def list_ports(self, query=None):
        """
        List available ports
        :param query: str|None search query
        :return:
        """
        raise NotImplemented()

    def compile(self, project):
        """
        Compile a project
        :param project: Project
        :return:
        """
        raise NotImplemented()

    def upload(self, project, port=None):
        """
        Upload a project
        :param project: Project
        :param port: str|None port to upload project to
        :return:
        """
        raise NotImplemented()

    def set_output(self, output):
        """
        Set command output
        :param output: str
        :return: bool always True
        """
        assert isinstance(output, str), 'output MUST be a string'

        self.output = output
        self.error = ''

        return True

    def set_error(self, error):
        """
        Set command error
        :param error: str
        :return: bool always False
        """
        assert isinstance(error, str), 'error MUST be a string'

        self.output = ''
        self.error = error
