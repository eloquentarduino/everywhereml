class Selector:
    """
    Choose a board from a number of ones
    """
    def __init__(self, entries):
        """

        :param entries:
        """
        assert len(entries) > 0, 'list of entries is empty'

        self.entries = sorted(set(entries), key=lambda e: str(e))

    def select(self):
        """
        Select one of the entries
        :return:
        """
        if len(self.entries) == 1:
            return self.entries[0]

        while True:
            print('Choose one of the following:')

            for i, entry in enumerate(self.entries):
                print(f' [{i + 1}] {str(entry)}')

            try:
                idx = int(input('> '))

                if idx < 1:
                    continue

                return self.entries[idx - 1]
            except ValueError:
                pass
            except IndexError:
                pass