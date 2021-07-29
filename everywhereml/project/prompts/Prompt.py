from everywhereml.Exceptions import InvalidChoiceError


class Prompt:
    """
    User-interaction abstract base class
    """
    def __init__(self, project):
        """
        Constructor
        :param project: Project
        """
        self.project = project

    def print(self, *args, **kwargs):
        """
        Print
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplemented()

    def input(self, prompt):
        """
        Get input from user
        :param prompt:
        :return:
        """
        raise NotImplemented()

    def choose(self, prompt, options, required=False):
        """
        Ask user to choose one of the options
        :param prompt: str message prompt
        :param options: list options to choose from
        :param required: bool if the choice can be skipped
        :return:
        """
        assert isinstance(options, list) and len(options) > 1, 'there MUST be at least two options'

        self.print(prompt)

        for i, option in enumerate(options):
            self.print('[%i] %s' % (i, str(option)))

        input = self.input('Your choice: ')

        try:
            idx = int()

            assert 0 < idx < len(options), 'invalid choice (%d)' % idx

            return options[idx]
        except ValueError:
            if required:
                raise InvalidChoiceError(input)

        return None

