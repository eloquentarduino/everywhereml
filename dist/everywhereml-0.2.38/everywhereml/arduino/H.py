from os.path import basename


class H:
    """
    Sketch header file
    """
    def __init__(self, filename: str, contents: str = ''):
        """

        :param filename:
        :param contents:
        """
        if contents == '':
            contents = filename
            filename = basename(filename)

        if contents.endswith('.h'):
            with open(contents, encoding='utf-8') as file:
                contents = file.read()

        self.filename = filename
        self.contents = contents
