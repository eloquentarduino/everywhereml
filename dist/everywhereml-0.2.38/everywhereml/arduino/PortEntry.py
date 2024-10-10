import re


class PortEntry:
    """
    Interact with port entries from the Arduino CLI
    """
    def __init__(self, entry: str):
        """

        :param entry:
        :return:
        """
        self.entry = entry.strip()
        self.port = ''
        self.description = ''

        match = re.search(r'^([-_/.a-zA-z0-9]+?)\s+(.+)$', self.entry)

        if match is not None:
            self.port, self.description = match.groups()

    def __str__(self) -> str:
        """

        :return:
        """
        return f'{self.port} ({self.description})'

    def __repr__(self) -> str:
        """

        :return:
        """
        return f'{self.port} ({self.description})'

    def exact_match(self, query: str, fqbn: str = None) -> bool:
        """
        Test if entry matches exactly query
        :param query:
        :param fqbn:
        :return:
        """
        return (self.port.lower() == query.lower()
                or self.description.lower() == query.lower()
                or (fqbn is not None and fqbn in self.description))

    def starts_with(self, query: str) -> bool:
        """
        Test if entry starts with query
        :param query:
        :return:
        """
        return (self.port.lower().startswith(query.lower())
                or self.description.lower().startswith(query.lower()))

    def ends_with(self, query: str) -> bool:
        """
        Test if entry ends with query
        :param query:
        :return:
        """
        return (self.port.lower().endswith(query.lower())
                or self.description.lower().endswith(query.lower()))

    def contains(self, query: str) -> bool:
        """
        Test if entry contains query
        :param query:
        :return:
        """
        return (query.lower() in self.port.lower()
                or query.lower() in self.description.lower())