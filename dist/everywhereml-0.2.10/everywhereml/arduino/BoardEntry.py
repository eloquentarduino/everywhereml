import re


class BoardEntry:
    """
    Interact with board entries from the Arduino CLI
    """
    def __init__(self, entry: str):
        """

        :param entry:
        :return:
        """
        self.entry = entry.strip()
        self.name = ''
        self.fqbn = ''

        match = re.search(r'^(.+?)\s+([-a-zA-Z0-9_]+:[-a-zA-Z0-9_]+:[-a-zA-Z0-9_]+)', self.entry)

        if match is not None:
            self.name, self.fqbn = match.groups()

    def __str__(self) -> str:
        """

        :return:
        """
        return f'{self.name} ({self.fqbn})'

    def __repr__(self) -> str:
        """

        :return:
        """
        return f'{self.name} ({self.fqbn})'

    def exact_match(self, query: str) -> bool:
        """
        Test if entry matches exactly query
        :param query:
        :return:
        """
        return self.name.lower() == query.lower() or self.fqbn.lower() == query.lower()

    def starts_with(self, query: str) -> bool:
        """
        Test if entry starts with query
        :param query:
        :return:
        """
        return self.name.lower().startswith(query.lower()) or self.fqbn.lower().startswith(query.lower())

    def ends_with(self, query: str) -> bool:
        """
        Test if entry ends with query
        :param query:
        :return:
        """
        return self.name.lower().endswith(query.lower()) or self.fqbn.lower().endswith(query.lower())

    def contains(self, query: str) -> bool:
        """
        Test if entry contains query
        :param query:
        :return:
        """
        return query.lower() in self.name.lower() or query.lower() in self.fqbn.lower()