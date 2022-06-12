import numpy as np
from serial import Serial
from time import time
from tqdm import tqdm
from everywhereml.data import Dataset


class SerialCollector:
    """
    Collect dataset from Serial port
    (mainly for Arduino projects)
    """
    def __init__(
            self,
            port,
            baud=9600,
            start_of_frame=None,
            num_features=None,
            feature_names=None,
            delimiter=','
    ):
        """

        :param port:
        :param baud:
        :param start_of_frame:
        :param num_features: int
        :param delimiter: str
        """
        if feature_names is not None and num_features == 0:
            num_features = len(feature_names)

        assert start_of_frame is None or isinstance(start_of_frame, str), 'start_of_frame MUST be a stirng'
        assert num_features is None or isinstance(num_features, int) and num_features > 0, 'num_features MUST be greater than 0'
        assert feature_names is None or num_features is None or len(feature_names) == num_features, 'feature_names count MUST match num_features'

        self.port = port
        self.baud = baud
        self.start_of_frame = start_of_frame
        self.num_features = num_features
        self.feature_names = feature_names
        self.delimiter = delimiter

    def collect_many_classes(
            self,
            dataset_name,
            num_samples=0,
            duration=0,
            timeout=5,
            **kwargs
    ):
        """
        Collect samples for many classes
        :param duration:
        :param dataset_name: str
        :param num_samples: int
        :param delimiter: str
        :param timeout: int timeout for serial
        :return:
        """
        with Serial(port=self.port, baudrate=self.baud, timeout=timeout) as serial:
            target_names = []
            X = []
            y = []
            target_idx = 0

            print('This is an interactive data capturing procedure.')
            print('Keep in mind that as soon as you will enter a class name, the capturing will start, so be ready!')

            while True:
                try:
                    target_name = input('Which class are you going to capture? (leave empty to exit) ').strip()

                    if len(target_name) == 0 and input('Are you sure you want to exit? (y|n) ').strip().lower() == 'y':
                        break

                    if len(target_name) == 0:
                        continue

                    # discard first line to be sure new line is properly formatted
                    serial.readline()
                    serial.reset_input_buffer()

                    if duration > 0:
                        class_data = self._collect_by_duration(serial=serial, duration=duration)
                    else:
                        class_data = self._collect_by_samples(serial=serial, num_samples=num_samples)

                    print('Captured %d samples' % len(class_data))

                    if input('Is this class ok? (y|n) ').strip().lower() != 'y':
                        continue

                    target_names.append(target_name)
                    X += class_data
                    y += [target_idx] * len(class_data)
                    target_idx += 1
                except ValueError:
                    pass

            assert len(X) > 0, 'No data captured'

            feature_names = [f'f{i}' for i in len(X[0])] if self.feature_names is None else self.feature_names

            return Dataset(
                name=dataset_name,
                X=np.asarray(X),
                y=np.asarray(y, dtype=np.int),
                feature_names=feature_names,
                target_names=target_names
            )

    def _collect_by_duration(self, serial, duration):
        """
        Collect data for the given amount of time
        :param serial:
        :param duration: int
        :return:
        """
        records = []

        with tqdm(total=duration) as progress:
            last_tick = int(time())
            current_tick = last_tick
            end_time = current_tick + duration

            while current_tick <= end_time:
                current_tick = int(time())
                line = serial.readline().decode('utf-8').strip()

                if not self._line_is_well_formatted(line):
                    continue

                record = [float(x) for x in self._trim(line).split(self.delimiter)]
                records.append(record)

                if last_tick != current_tick:
                    progress.update(1)
                    last_tick = current_tick

        return records

    def _collect_by_samples(self, serial, num_samples):
        """
        Collect the given number of samples
        :param serial:
        :param num_samples:
        :return:
        """
        records = []

        while num_samples < 1:
            try:
                num_samples = int(input('How many samples do you want to record? '))
            except ValueError:
                pass

        with tqdm(total=num_samples) as progress:
            captured_samples = 0

            while captured_samples < num_samples:
                line = serial.readline().decode('utf-8').strip()

                if not self._line_is_well_formatted(line):
                    continue

                record = [float(x) for x in self._trim(line).split(self.delimiter)]
                records.append(record)
                captured_samples += 1
                progress.update(1)

        return records

    def _line_is_well_formatted(self, line):
        """
        Test if line matches expected format
        :param line:
        :return:
        """
        if len(line) == 0:
            return False

        if self.start_of_frame is not None and not line.startswith(self.start_of_frame):
            return False

        if self.num_features is not None and self._trim(line).count(self.delimiter) != self.num_features - 1:
            return False

        return True

    def _trim(self, line):
        """
        Remove start of frame from line
        :param line: str
        :return: str
        """
        if self.start_of_frame is not None and line.startswith(self.start_of_frame):
            return line.replace(self.start_of_frame, '').strip()

        return line.strip()