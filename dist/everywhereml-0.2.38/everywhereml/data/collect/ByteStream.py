from time import time


class ByteStream:
    """
    Read a binary stream
    """
    def __init__(self, source, start_of_frame, end_of_frame, max_fps=0):
        """

        :param source:
        :param start_of_frame:
        :param end_of_frame:
        :param max_fps:
        """
        assert callable(source), 'source MUST be callable'

        self.source = source
        self.start_of_frame = self.to_bytes(start_of_frame)
        self.end_of_frame = self.to_bytes(end_of_frame)
        self.max_fps = max_fps

    def collect_samples(self, count):
        """

        :param count:
        :return:
        """
        return self.collect(stop_condition=lambda c, d: c >= count)

    def collect_duration(self, duration):
        """

        :param duration:
        :return:
        """
        return self.collect(stop_condition=lambda c, d: d > duration)

    def collect(self, stop_condition):
        """

        :param duration: int
        :return:
        """
        assert callable(stop_condition), 'stop_condition MUST be callable'

        start = time()
        last_frame = start
        count = 0
        duration = 0
        buffer = b''

        while not stop_condition(count, duration):
            buffer += self.source()
            a = buffer.find(self.start_of_frame)
            b = buffer.find(self.end_of_frame)

            if a > b:
                buffer = buffer[a:]
                continue

            if a != -1 and b != -1:
                frame = buffer[a + len(self.start_of_frame):b]
                buffer = buffer[b + len(self.end_of_frame):]

                if self.max_fps == 0 or time() - last_frame >= 1.0 / self.max_fps:
                    yield frame
                    count += 1

            duration = time() - start

    def to_bytes(self, x):
        """

        :param x:
        :return:
        """
        if isinstance(x, str):
            return str.encode(x)
        if isinstance(x, bytes):
            return x
        raise AssertionError('x MUST either be a string or a byte array')