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
        self.template_folder = template_folder.replace('everywhereml/', 'templates/')
        self.language = language
        self.dialect = dialect

    def get_source(self, environment, template):
        """
        Return the most specific source file
        :param environment:
        :param template:
        :return:
        """
        dialect = self.dialect or "dialect"
        template = template.replace(os.path.sep, '/')
        folder = self.template_folder.replace(f'{template}/', '')
        attempts = []

        while len(folder):
            attempts += [
                f'{folder}/{self.language}/{dialect}/{template}.{self.language}.{dialect}.jinja',
                f'{folder}/{self.language}/{dialect}/{template}.{self.language}.jinja',
                f'{folder}/{self.language}/{dialect}/{template}.jinja',
                f'{folder}/{self.language}/{template}.{self.language}.{dialect}.jinja',
                f'{folder}/{self.language}/{template}.{self.language}.jinja',
                f'{folder}/{self.language}/{template}.jinja',
                f'{folder}/{template}.{self.language}.{dialect}.jinja',
                f'{folder}/{template}.{self.language}.jinja',
                f'{folder}/{template}.jinja',
            ]
            folder = os.path.dirname(folder)

        for source in attempts:
            try:
                return super().get_source(environment, source)
            except TemplateNotFound:
                pass

        raise TemplateNotFound(f'{template} in {attempts}')
