import os.path
from pathlib import Path
from jinja2 import FileSystemLoader as Base, TemplateNotFound


class FileSystemLoader(Base):
    """
    Custom loader compatible with Windows and Unix
    """
    def __init__(self, template_folder, language, dialect=None, **kwargs):
        """
        Constructor
        :param template_folder: str
        :param language: str
        :param dialect: str
        :param kwargs:
        """
        base_folder = Path(__file__).absolute().parent.parent.parent
        super(FileSystemLoader, self).__init__(base_folder, **kwargs)
        self.template_folder = template_folder.replace('everywhereml/', '') + '/templates'
        self.language = language
        self.dialect = dialect

    def get_source(self, environment, template):
        """
        Return the most specific source file
        :param environment:
        :param template:
        :return:
        """
        template = template.replace(os.path.sep, '/')
        parent_folder = self.template_folder.replace(f'{template}/', '')
        attempts = [
            f'{self.template_folder}/{self.language}/{self.dialect or "dialect"}/{template}.jinja',
            f'{self.template_folder}/{self.language}/{template}.{self.dialect or "dialect"}.jinja',
            f'{self.template_folder}/{self.language}/{template}.jinja',
            f'{self.template_folder}/{template}.{self.language}.jinja',
            f'{self.template_folder}/{template}.jinja',
            f'{parent_folder}/{template}.{self.language}.{self.dialect or "dialect"}.jinja',
            f'{parent_folder}/{template}.{self.language}.jinja',
            f'{parent_folder}/{template}.jinja',
            f'{template}.{self.language}.{self.dialect or "dialect"}.jinja',
            f'{template}.{self.language}.jinja',
            f'{template}.jinja'
        ]

        for source in attempts:
            try:
                return super().get_source(environment, source)
            except TemplateNotFound:
                pass

        print('attempts')
        print(attempts)

        raise TemplateNotFound(template)
