class Cpp:
    """
    Sketch C++ file
    """
    def __init__(self, filename: str, contents: str):
        """

        :param filename:
        :param contents:
        """
        if contents.endswith('.cpp'):
            with open(contents, encoding='utf-8') as file:
                contents = file.read()

        self.filename = filename
        self.contents = contents
