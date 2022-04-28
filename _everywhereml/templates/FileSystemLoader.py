import os.path
from jinja2 import FileSystemLoader as Base, TemplateNotFound


class FileSystemLoader(Base):
    """
    Custom loader compatible with Windows and Unix
    """
    def __init__(self, folder, dialect=None, **kwargs):
        """

        :param folder:
        :param dialect:
        :param kwargs:
        """
        super(FileSystemLoader, self).__init__(folder, **kwargs)
        self.dialect = dialect

    def get_source(self, environment, template):
        """

        :param environment:
        :param template:
        :param dialect:
        :return:
        """
        template = template.replace(os.path.sep, '/')

        if self.dialect:
            # try dialect template
            try:
                return super().get_source(environment, template.replace('.jinja', '.%s.jinja' % self.dialect))
            except TemplateNotFound:
                pass

        return super().get_source(environment, template)
