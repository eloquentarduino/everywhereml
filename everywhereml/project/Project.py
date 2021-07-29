import os.path
from os import makedirs
from everywhereml.project.toolchain.Toolchain import Toolchain
from everywhereml.project.prompts import SysPrompt
from everywhereml.project.Config import Config
from everywhereml.project.Logger import Logger
#from everywhereml.templates import jinja


class Project:
    """
    A microcontroller project
    """
    def __init__(self, name, toolchain, prompt=None, logger=None):
        """
        Constructor
        :param name: str name of the project
        :param toolchain: Toolchain
        :param prompt: Prompt|None
        """
        assert isinstance(name, str) and len(name) > 0, 'you MUST set a project name'
        assert isinstance(toolchain, Toolchain), 'toolchain MUST be an instance of Toolchain'

        self.name = name
        self.toolchain = toolchain
        self.config = Config(self)
        self.prompt = (prompt or SysPrompt)(self)
        self.logger = (logger or Logger())

    @property
    def sketch_path(self):
        """
        Get path to sketch folder
        :return: str
        """
        return os.path.join('sketches', self.name)

    @property
    def ino_name(self):
        """
        Get name of the .ino file
        :return: str
        """
        return '%s.ino' % self.name

    @property
    def cpp_name(self):
        """
        Get name of the main file
        :return: str
        """
        return '%s.cpp' % self.name

    def setup(self, mkdir_mode=0o777):
        """
        Setup project (create directory and main files)
        :return:
        """
        if not os.path.isdir(self.sketch_path):
            makedirs(self.sketch_path, mkdir_mode)

        self.files.add(self.ino_name, jinja('project/templates/empty_ino.jinja'), exists_ok=False)
        self.files.add(self.cpp_name, jinja('project/templates/empty_main.jinja'), exists_ok=False)

