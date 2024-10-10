class Ino:
    """
    Sketch main file
    """
    def __init__(self, contents: str):
        """

        :param contents:
        """
        if contents.endswith('.ino'):
            with open(contents, encoding='utf-8') as file:
                contents = file.read()

        self.contents = contents
