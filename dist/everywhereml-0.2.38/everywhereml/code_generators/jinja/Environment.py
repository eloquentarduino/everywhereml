import os.path
from jinja2 import Environment as Base


class Environment(Base):
    """
    Custom Jinja environment
    """
    def join_path(self, template, parent):
        """
        Enable relative template paths
        :param template: str
        :param parent: str
        """
        return os.path.normpath(os.path.join(os.path.dirname(parent), template))

    def add_filter(self, name, function):
        """
        Add filter
        :param name: str
        :param function: callable
        :return:
        """
        assert callable(function), 'filter function MUST be callable'

        self.filters[name] = function

    def add_global(self, name, value):
        """
        Add global
        :param name: str
        :param value:
        :return:
        """
        self.globals[name] = value
