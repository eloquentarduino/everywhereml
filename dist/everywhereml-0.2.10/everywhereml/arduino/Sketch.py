import re
from os import makedirs
from os.path import join, abspath, basename, isdir
from everywhereml.arduino.Ino import Ino
from everywhereml.arduino.Cli import Cli, cli as cli_singleton


class Sketch:
    """
    Write Arduino sketches from Python
    """
    def __init__(self, name: str, folder: str = '', board: str = None):
        """

        :param name: str
        :param folder: str
        :param board: str
        """
        if folder == ':system:':
            folder = join(cli_singleton.get_user_directory(), 'sketches')

        folder = folder.rstrip('/')

        self.name = name
        self.board = board
        self.folder = folder if basename(folder) == self.name else join(folder, self.name)
        self.fqbn = None
        self.port = None
        self.output = ''
        self.is_successful = True
        self.files = {}
        self.stats = {}

        if not isdir(self.folder):
            makedirs(self.folder, 0o777)

    def __add__(self, other):
        """

        :param other:
        :return:
        """
        filename = f'{self.name}.ino' if isinstance(other, Ino) else other.filename
        self.files[filename] = {
            'contents': other.contents
        }

        with open(self.path_to(filename), 'w', encoding='utf-8') as file:
            file.write(other.contents)

        return self

    @property
    def path(self):
        """
        Get absolute path to project folder
        :return:
        """
        return abspath(self.folder)

    def path_to(self, filename: str) -> str:
        """
        Convert relative path to absolute path
        :param filename:
        :return:
        """
        return abspath(join(self.folder, filename))

    def compile(self, cli : Cli = None, board: str = None, *args):
        """
        Compile sketch
        :param cli:
        :param board:
        :return: str|bool
        """
        self.is_successful = False
        cli = cli or cli_singleton
        self.fqbn = cli.find_fqbn(board or self.fqbn or self.board)
        self.stats.update(
            flash=0,
            flash_max=0,
            flash_percent=0,
            ram=0,
            ram_max=0,
            ram_percent=0)

        cli.exec('compile', '--verify', '--fqbn', self.fqbn, *args, cwd=self.path)
        self.output = cli.any_output
        self.stats['compile_time'] = cli.exec_time

        # parse compile log
        flash_pattern = r'Sketch uses (\d+) bytes(.+?Maximum is (\d+))?'
        memory_pattern = r'Global variables use (\d+)(.+?Maximum is (\d+))?'
        flash_match = re.search(flash_pattern, self.output.replace("\n", ""))
        memory_match = re.search(memory_pattern, self.output.replace("\n", ""))

        if flash_match is not None:
            self.stats['flash'] = int(flash_match.group(1))

            if len(flash_match.groups()) > 2:
                self.stats['flash_max'] = int(flash_match.group(3))
                self.stats['flash_percent'] = self.stats['flash'] / self.stats['flash_max']

        if memory_match is not None:
            self.stats['ram'] = int(memory_match.group(1))

            if len(memory_match.groups()) > 2:
                self.stats['ram_max'] = int(memory_match.group(3))
                self.stats['ram_percent'] = self.stats['ram'] / self.stats['ram_max']

        self.is_successful = self.stats['flash'] > 0

        return self

    def upload(self, port: str = None, cli : Cli = None, board: str = None, return_success: bool = False, *args):
        """
        Upload sketch
        :param port:
        :param cli:
        :param board:
        :param return_success:
        :param args:
        :return:
        """
        self.is_successful = False
        cli = cli or cli_singleton
        self.fqbn = cli.find_fqbn(board or self.fqbn or self.board)
        self.port = cli.find_port(port or self.port, fqbn=self.fqbn)

        cli.exec('upload', '--verify', '--fqbn', self.fqbn, '--port', self.port, *args, cwd=self.path)

        self.output = cli.any_output
        self.is_successful = re.search(r'leaving...|ok|success', self.output.lower()) is not None
        self.stats['upload_time'] = cli.exec_time

        return self

