import re
import json
import numpy as np
from tempfile import TemporaryDirectory
from subprocess import check_output


class BaseRuntime:
    """
    Actually run code in a given language to test it works as expected
    """
    def __init__(self):
        """
        Constructor
        """
        self.files = []

    def __str__(self):
        """
        Get runtime name
        :return: str
        """
        return f'Runtime(language={self.language}, dialect={self.dialect})'

    def __repr__(self):
        """
        Get runtime name
        :return: str
        """
        return str(self)

    @property
    def main_file(self):
        raise NotImplementedError('main_file')

    @property
    def language(self):
        raise NotImplementedError('language')

    @property
    def dialect(self):
        raise NotImplementedError('dialect')

    def add_main(self, contents):
        """

        :param contents:
        :return:
        """
        self.add_file(self.main_file, contents)

    def add_file(self, filename, contents):
        """
        Save file in project directory
        :param filename: str
        :param contents: str
        :return:
        """
        self.files.append((filename, contents))

    def output(self, tmp_folder=None):
        """
        Run program and get results back
        :return:
        """
        with TemporaryDirectory() as folder:
            # write files
            if tmp_folder is not None:
                folder = tmp_folder

            for filename, contents in self.files:
                with open('%s/%s' % (folder, filename), 'w', encoding='utf-8') as file:
                    file.write(contents)

            # exec runtime and get output
            commands = self.get_cmd()

            if isinstance(commands[0], str):
                commands = [commands]

            for cmd in commands:
                output = check_output(cmd, cwd=folder).decode('utf-8').strip()

            # format output as json
            if not output.startswith('['):
                output = '[%s]' % output

            output = re.sub(r'\]\s*\[', '],[', output)
            output = re.sub(r',\s*\]', ']', output)

            try:
                return np.asarray(json.loads(output), dtype=np.float)
            except json.decoder.JSONDecodeError:
                return None

    def get_cmd(self):
        """
        Get exec command
        :return: list
        """
        raise NotImplementedError('you MUST implement get_cmd()')