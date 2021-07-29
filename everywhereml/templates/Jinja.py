import os.path
from jinja2 import BaseLoader
from everywhereml.templates.Environment import Environment
from everywhereml.templates.FileSystemLoader import FileSystemLoader


class Jinja:
    """
    Jinja template renderer, with some smart defaults
    """
    def __init__(self, template_folder, cwd=None, prettifier=None, language=None, dialect=None):
        """
        Constructor
        :param template_folder: str
        :param cwd: str folder to which the template_folder is relative to
        :param prettifier: callable a callable that can prettify generated code
        :param language: str language of the template, used to get a default prettyfier
        :param dialect: str dialect of the language
        """
        if cwd is None:
            cwd = __file__

        if os.path.isfile(cwd):
            cwd = os.path.dirname(os.path.relpath(cwd))

        if language is not None:
            template_folder = os.path.join('languages', language, template_folder)

        template_folder = os.path.abspath(os.path.join(cwd, template_folder))

        assert os.path.isdir(template_folder), 'template folder %s MUST exist' % template_folder

        self.env = Environment(language=language, loader=FileSystemLoader(template_folder, dialect=dialect))
        self.prettifier = prettifier

    def add_filter(self, name, function):
        """
        Add filter
        :param name:
        :param function: callable
        :return:
        """
        self.env.add_filter(name, function)

    def add_global(self, name, value):
        """
        Add global
        :param name:
        :param value:
        :return:
        """
        self.env.add_global(name, value)

    def render(self, template_name, template_data={}):
        """
        Render template
        :param template_name: str
        :param template_data: dict
        :return: str
        """
        return self.prettify(self.env.get_template(template_name).render(template_data))
    
    def render_string(self, template_string, template_data=None):
        """
        Render a Jinja template from string
        :param template_string: str
        :param template_data: dict
        :return:
        """
        if template_data is None:
            template_data = {}

        return self.prettify(Environment(loader=BaseLoader()).from_string(template_string).render(template_data))

    def prettify(self, output):
        """
        Prettify output
        :param output: str
        :return: str
        """
        if self.prettifier is None:
            return output

        assert callable(self.prettifier), 'prettifier MUST be callable'

        return self.prettifier(output)
