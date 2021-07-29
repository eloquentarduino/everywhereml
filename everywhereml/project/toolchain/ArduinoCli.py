import re
from subprocess import STDOUT, CalledProcessError, check_output
from everywhereml.project.toolchain.Toolchain import Toolchain


class ArduinoCli(Toolchain):
    """
    Interact with the arduino-cli
    """
    def __init__(self, executable='arduino-cli', cwd=None):
        """
        Constructor
        :param executable: str path to executable
        :param executable: str path to current working directory
        """
        super().__init__(executable, cwd)

    def list_boards(self, query=None):
        """
        List available board
        :param query: str|None search query (ignored)
        :return: list
        """
        if self.exec(['board', 'listall']):
            regex = re.compile(r'^(.+?)\s+([^ :]+?:[^ :]+?:[^ :]+?)$')
            matches = [regex.search(line) for line in self.output_lines]

            return [{'label': match.group(1), 'fqbn': match.group(2)} for match in matches if match is not None]

        return []

    def list_ports(self, query=None):
        """
        List available board
        :param query: str|None search query (ignored)
        :return: list
        """
        if self.exec(['board', 'list']):
            return [line.split(' ')[0] for line in self.output_lines if ' ' in line]

        return []

    def compile(self, project):
        """
        Compile project
        :param project: Project
        :return:
        """
        return self.exec(['compile', '--verify', '--fqbn', project.config.fqbn, project.sketch_path])

    def exec(self, args):
        """
        Run cli command and save output
        :param args: list arduino-cli command
        :return: bool success or failure
        """
        assert isinstance(args, list), 'arduino-cli arguments MUST be a list'

        try:
            return self.set_output(check_output([self.executable] + args, stderr=STDOUT, cwd=self.cwd).decode('utf-8'))
        except CalledProcessError as error:
            return self.set_error(error.output.decode('utf-8'))
