import re
from everywhereml.project.Board import Board
from everywhereml.project.Serial import Serial
from everywhereml.Exceptions import BoardQueryNotFoundError, PortQueryNotFoundError


class Config:
    """
    Project configuration class
    """
    def __init__(self, project):
        """
        Constructor
        :param project: Project
        """
        self.project = project
        self.board = None

    def set_board(self, query=None, fqbn=None, label=None, **kwargs):
        """
        Set board model
        :param query: str|None search query to find the board
        :param fqbn: str|None fully-qualified board name
        :param label: str|None human-readable label for the board
        :param kwargs: board-specific options
        :return:
        """
        assert fqbn is None or isinstance(fqbn, str) and len(fqbn) > 0, 'fqbn MUST either be None or a string'

        if fqbn is not None:
            self.board = Board(fqbn=fqbn, label=label, **kwargs)
            return

        # search by query (delegate to toolchain)
        candidates = self.project.toolchain.list_boards(query=query)

        if len(candidates) == 0:
            raise BoardQueryNotFoundError(query)

        elif len(candidates) == 1:
            return Board(**candidates[0], **kwargs)

        else:
            if query is None or len(query) == 0:
                choice = self.project.prompt.choose('Multiple boards found, choose one:', candidates, required=True)
                self.board = Board(**choice)

            else:
                # toolchain may ignore query, so perform search here
                # 1) look for an exact match
                exact_matches = [board for board in candidates if
                                 board.get('label').lower() == query.lower() or
                                 board.get('fqbn') == query.lower()]

                if len(exact_matches) == 1:
                    self.board = Board(**exact_matches[0], **kwargs)
                    return

                # 2) search by glob pattern (* is a wildcard)
                glob_regex = re.compile(query.replace('*', '.*'))
                glob_matches = [board for board in candidates if
                                glob_regex.search(board.get('label')) is not None or
                                glob_regex.search(board.get('fqbn')) is not None]

                if len(glob_matches) == 1:
                    self.board = Board(**glob_matches[0], **kwargs)
                    return
                elif len(glob_matches) > 1:
                    choice = self.project.prompt.choose('Multiple boards found, choose one:', glob_matches, required=True)
                    self.board = Board(**choice)
                    return

                # 3) search by regex
                re_regex = re.compile(query)
                re_matches = [board for board in candidates if
                              re_regex.search(board.get('label')) is not None or
                              re_regex.search(board.get('fqbn')) is not None]

                if len(re_matches) == 1:
                    self.board = Board(**re_matches[0], **kwargs)
                    return
                elif len(re_matches) > 1:
                    choice = self.project.prompt.choose('Multiple boards found, choose one:', re_matches,
                                                        required=True)
                    self.board = Board(**choice)
                    return

        raise BoardQueryNotFoundError(query)

    def set_port(self, query, baudrate=115200):
        """
        Set serial port
        :param query: str
        :param baudrate: int
        :return:
        """
        if query.endswith('*'):
            candidates = [port for port in self.project.toolchain.list_ports(query) if
                          port.startswith(query)]

            if len(candidates) == 0:
                raise PortQueryNotFoundError(query)

            elif len(candidates) == 1:
                self.project.serial = Serial(candidates[0], baudrate=baudrate)
                return

            else:
                choice = self.project.prompt.choose('Multiple ports found, choose one:', candidates,
                                                    required=True)
                self.project.serial = Serial(choice, baudrate=baudrate)
                return

        self.project.serial = Serial(query, baudrate=baudrate)
