import numpy as np
from everywhereml.code_generators.jinja.Environment import Environment
from everywhereml.code_generators.jinja.FileSystemLoader import FileSystemLoader
from everywhereml.code_generators.jinja.filters import c_shape, to_c_array, to_c_comment, to_variable_name
from everywhereml.code_generators.jinja.filters import to_py_comment, to_py_list


class Jinja:
    """
    Render Jinja templates
    """
    def __init__(self, base_folder, language, dialect):
        """
        Constructor
        :param base_folder:
        :param language:
        :param dialect:
        """
        self.loader = FileSystemLoader(base_folder, language=language, dialect=dialect)
        self.env = Environment(loader=self.loader, extensions=['jinja2_workarounds.MultiLineInclude'])
        self.data = {}

        self.env.add_global('enumerate', enumerate)
        self.env.add_global('isinstance', isinstance)
        self.env.add_global('len', len)
        self.env.add_global('np', np)
        self.env.add_global('range', range)
        self.env.add_global('str', str)
        self.env.add_global('zip', zip)

        self.env.add_filter('c_shape', c_shape)
        self.env.add_filter('to_c_array', to_c_array)
        self.env.add_filter('to_c_comment', to_c_comment)

        self.env.add_filter('to_py_comment', to_py_comment)
        self.env.add_filter('to_py_list', to_py_list)

        self.env.add_filter('to_variable_name', to_variable_name)

    def update(self, **kwargs):
        """
        Update data
        :param kwargs:
        :return:
        """
        self.data.update(**kwargs)

    def render(self, template_name, template_data=None):
        """
        Return generated code
        :param template_name: str
        :param template_data: dict
        :return:
        """
        template_data = {
            **self.data,
            **(template_data or {})
        }
        return self.env.get_template(template_name).render(template_data)
