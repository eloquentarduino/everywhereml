import re
from os import getcwd
from os.path import abspath
from platform import system
from timeit import default_timer
from subprocess import STDOUT, CalledProcessError, check_output
from everywhereml.arduino.BoardEntry import BoardEntry
from everywhereml.arduino.PortEntry import PortEntry
from everywhereml.arduino.Selector import Selector


class Cli:
    """
    Arduino-CLI wrapper
    """
    def __init__(self, cwd: str = None):
        """

        """
        self.cwd = None
        self.exe = None
        self.output = None
        self.error = None
        self.exec_time = 0

        self.configure_exe('arduino-cli.exe' if system().lower() == 'window' else 'arduino-cli')
        self.set_working_dir(cwd)

    @property
    def is_successful(self) -> bool:
        """
        Test if command was successful
        @return bool True on success, False on error
        """
        return self.error is None

    @property
    def any_output(self):
        """
        Return either output or error
        :return: str
        """
        return self.output or self.error or ''

    @property
    def lines(self) -> list:
        """
        Get command output as lines
        @return list
        """
        return [line.strip() for line in (self.output or "").split("\n")]

    def configure_exe(self, exe: str):
        """
        Set executable path
        :param exe: str
        :return:
        """
        self.exe = exe

    def set_working_dir(self, cwd: str):
        """
        Set current working directory
        :param cwd: str
        :return:
        """
        self.cwd = abspath(cwd or getcwd())

    def find_fqbn(self, query: str):
        """
        Find fqbn from fuzzy query
        :param query: str
        :return:
        """
        assert query is not None, 'query cannot be None'

        boards = [BoardEntry(b.strip()) for b in self.exec('board', 'listall').split('\n') if b.strip()]
        exact_matches = [b for b in boards if b.exact_match(query)]

        if len(exact_matches) > 0:
            return Selector(exact_matches).select().fqbn

        partial_matches = (
                [b for b in boards if b.starts_with(query)] +
                [b for b in boards if b.ends_with(query)] +
                [b for b in boards if b.contains(query)])

        if len(partial_matches) > 0:
            return Selector(partial_matches).select().fqbn

        raise IndexError(f'Cannot find board that matches query "{query}"')

    def find_port(self, query: str = None, fqbn: str = None):
        """
        Find port by fuzzy query
        :param query:
        :param fqbn:
        :return:
        """
        ports = [PortEntry(p.strip()) for p in self.exec('board', 'list').split('\n') if p.strip()]
        exact_matches = [p for p in ports if p.exact_match(query, fqbn)]

        if len(exact_matches) > 0:
            return Selector(exact_matches).select().port

        partial_matches = (
            [p for p in ports if p.starts_with(query)] +
            [p for p in ports if p.ends_with(query)] +
            [p for p in ports if p.contains(query)])

        if len(partial_matches) > 0:
            return Selector(partial_matches).select().port

        return query

    def exec(self, command: str, *args, cwd: str = None) -> str:
        """
        Execute command
        :return: str command output
        """
        try:
            start_time = default_timer()
            self.output = check_output([self.exe, command] + list(args), stderr=STDOUT, cwd=(cwd or self.cwd)).decode('utf-8')
            self.error = None
            self.exec_time = default_timer() - start_time

            return self.output
        except CalledProcessError as err:
            self.error = err.output.decode('utf-8')
            self.output = None

            return self.error

        return ''

    def get_directory(self, which: str) -> str:
        """
        Get system directory

        :param which:
        :return: str
        """
        try:
            config = self.exec('config', 'dump')
            directories = config.split('directories:')[1]

            return [line.strip() for line in directories.split('\n') if line.strip().startswith(f'{which}:')][0][len(which)+1:].strip()
        except IndexError:
            return 'error'

    def get_user_directory(self) -> str:
        """
        Get system user directory
        :return:
        """
        return self.get_directory('user')


cli = Cli()