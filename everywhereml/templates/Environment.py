import os.path
from importlib import import_module
from jinja2 import Environment as Base
from everywhereml.templates.globals import globals


class Environment(Base):
    """
    Custom Jinja environment
    """
    def __init__(self, language, **kwargs):
        """
        Constructor
        :param language: str
        :param kwargs:
        """
        super().__init__(**kwargs)

        # inject language-specific filters
        filters = import_module('everywhereml.templates.filters.%s' % language)
        [self.add_filter(name, getattr(filters, name)) for name in dir(filters) if callable(getattr(filters, name))]

        # inject language-agnostic globals
        [self.add_global(name, value) for name, value in globals.items()]

    def join_path(self, template, parent):
        """
        Override join_path() to enable relative template paths
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
