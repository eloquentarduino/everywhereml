from time import time
from tqdm import tqdm
from serial import Serial, SerialException


class SerialIO:
    """
    Interact with the Serial port
    """
    def __init__(self, port, baud : int = 115200):
        """
        :param port:
        :param baud: int
        """
        self.port = port
        self.baud = baud

    def read_lines(self, limit: int = -1, timeout: int = 120, confirm: bool = True, start_of_line: str = "", **kwargs):
        """
        Read lines
        :param limit:
        :param timeout:
        :param confirm:
        :param start_of_line:
        :return: list
        """
        with Serial(self.port, baudrate=self.baud, timeout=10, **kwargs) as serial:
            lines = []
            last_update = 0
            current_update = 0

            if confirm:
                input("Serial port is open. Press [Enter] when you're ready to start capturing ")

            with tqdm(total=100) as progress:
                elapsed = 0
                started_at = time()

                while (limit < 0 or len(lines) < limit) and elapsed < timeout:
                    try:
                        line = serial.readline().decode("utf-8").strip()

                        if start_of_line == "" or line.startswith(start_of_line):
                            lines.append(line[len(start_of_line):])

                        if limit > 0:
                            current_update = (100 * len(lines)) // limit
                        else:
                            current_update = (100 * elapsed) // timeout

                        progress.update(current_update - last_update)
                        last_update = current_update

                    except UnicodeDecodeError:
                        pass

                    finally:
                        elapsed = time() - started_at

            return lines[1:-1]