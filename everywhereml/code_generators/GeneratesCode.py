import os.path
from os import makedirs
from everywhereml.code_generators.jinja.Jinja import Jinja
from everywhereml.code_generators.prettifiers.basic_python_prettifier import basic_python_prettify


class GeneratesCode:
    """
    Mixin with methods to export a given class to one of the supported languages
    """
    @property
    def class_name(self):
        """
        Get class name
        :return:
        """
        return type(self).__name__

    @property
    def package_name(self):
        """
        Get package name
        :return:
        """
        return '.'.join(self.__module__.__str__().split('.')[:-1])

    @property
    def template_folder(self):
        """
        Get base template folder
        :return:
        """
        return self.package_name.replace('.', '/')

    def get_template_data(self):
        """
        Abstract method to get template data
        :return:
        """
        raise NotImplementedError('get_template_data()')

    def to_cpp(self, class_name=None, namespace=None, instance_name=None, dialect=None, **kwargs):
        """
        Generate C++ code
        :param class_name: str
        :param namespace: str
        :param instance_name: str
        :param dialect: str
        :return:
        """
        return self.to_language(
            'cpp',
            class_name=class_name,
            namespace=namespace,
            instance_name=instance_name,
            dialect=dialect,
            **kwargs
        )

    def to_cpp_file(self, filename, **kwargs):
        """
        Save C++ code to file
        :param filename:
        :param kwargs:
        :return:
        """
        return self.to_file(filename, self.to_cpp(**kwargs))

    def to_arduino(self, **kwargs):
        """
        Generate C++/Arduino code
        :return:
        """
        return self.to_cpp(dialect='arduino', **kwargs)

    def to_arduino_file(self, filename, **kwargs):
        """
        Save C++/Arduino code to file
        :param filename:
        :param kwargs:
        :return:
        """
        return self.to_file(filename, self.to_arduino(**kwargs))

    def to_python(self, class_name=None, instance_name=None, dialect=None, **kwargs):
        """
        Generate Python code
        :param class_name: str
        :param instance_name: str
        :param dialect: str
        :return:
        """
        return basic_python_prettify(self.to_language(
            'py',
            class_name=class_name,
            instance_name=instance_name,
            dialect=dialect,
            **kwargs
        ))

    def to_micropython(self, **kwargs):
        """
        Generate Micropython code
        :return:
        """
        return self.to_python(dialect='micro', **kwargs)

    def to_python_file(self, filename, **kwargs):
        """
        Save Python code to file
        :param filename:
        :param kwargs:
        :return:
        """
        return self.to_file(filename, self.to_python(**kwargs))

    def to_micropython_file(self, filename, **kwargs):
        """
        Save Micropython code to file
        :param filename:
        :param kwargs:
        :return:
        """
        return self.to_python_file(filename, dialect='micro', **kwargs)

    def to_js(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        return self.to_language('js', **kwargs)

    def to_js_file(self, filename, **kwargs):
        """

        :param filename:
        :param kwargs:
        :return:
        """
        return self.to_file(filename, self.to_js(**kwargs))

    def to_language(self, language, dialect=None, **kwargs):
        """
        Generate code in given language
        :param language: str
        :param dialect: str
        :param language_data: dict
        :param kwargs:
        :return:
        """
        language_data_function = f'get_template_data_{language}'
        language_data = (getattr(self, language_data_function)(dialect=dialect)
                            if hasattr(self, language_data_function) else {})

        jinja = Jinja(self.template_folder, language=language, dialect=dialect)
        jinja.update(**self.get_template_data())
        jinja.update(**language_data)
        jinja.update(**kwargs)
        jinja.update(this=self, id=id(self), UUID=f'UUID{id(self)}', description=str(self).split('\n'))

        return jinja.render(self.class_name)

    def to_language_file(self, language, filename, **kwargs):
        """
        Save generated code to file
        :param language:
        :param file:
        :param kwargs:
        :return:
        """
        if os.path.dirname(filename):
            makedirs(os.path.dirname(filename), 0o777, exist_ok=True)

        with open(filename, 'w', encoding='utf-8') as file:
            contents = self.to_language(language=language, **kwargs)
            file.write(contents)

            return contents

    def to_file(self, filename, contents):
        """
        Save generated code to file
        :param language:
        :param contents:
        :return:
        """
        if os.path.dirname(filename):
            makedirs(os.path.dirname(filename), 0o777, exist_ok=True)

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(contents)

            return contents
