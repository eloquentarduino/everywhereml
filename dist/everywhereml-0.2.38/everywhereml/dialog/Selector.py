from logging import info


class Selector:
    """
    Choose a board from a number of ones
    """
    def __init__(self, entries):
        """

        :param entries:
        """
        assert len(entries) > 0, 'list of entries is empty'

        self.entries = sorted(set(entries), key=lambda e: self.to_string(e))
        self._allow_none = False

    def log(self, objects_name: str):
        """
        Log choices
        :param objects_name:
        :return:
        """
        info(f"Found {len(self.entries)} {objects_name}")

        if len(self.entries) == 1:
            info(f"Choosing {self.to_string(self.entries[0])} automatically")

        return self

    def allow_none(self):
        """
        Allow user to exit from selection
        """
        self._allow_none = True

        return self

    def select(self):
        """
        Select one of the entries
        :return:
        """
        if len(self.entries) == 1:
            return self.to_value(self.entries[0])

        while True:
            print('Choose one of the following:')

            for i, entry in enumerate(self.entries):
                print(f' [{i + 1}] {self.to_string(entry)}')

            if self._allow_none:
                print("(0 to exit)")

            try:
                idx = int(input('> '))

                if self._allow_none and idx == 0:
                    return None

                if idx < 1:
                    continue

                return self.to_value(self.entries[idx - 1])
            except ValueError:
                pass
            except IndexError:
                pass

    def to_string(self, entry) -> str:
        """
        Convert entry to string
        """
        return entry[0] if isinstance(entry, tuple) else str(entry)

    def to_value(self, entry):
        """
        Convert entry to value
        """
        return entry[1] if isinstance(entry, tuple) else entry