import numpy as np
from os import mkdir
from os.path import isdir
from serial import Serial
from time import time
from tqdm import tqdm
from skimage.io import imsave
from everywhereml.data import Dataset, ImageDataset
from everywhereml.data.collect.ByteStream import ByteStream
from everywhereml.data.collect.BaseCollector import BaseCollector


class SerialCollector(BaseCollector):
    """
    Collect dataset from Serial port
    (mainly for Arduino projects)
    """
    def __init__(
            self,
            port,
            baud=9600,
            start_of_frame=None,
            end_of_frame=None,
            num_features=None,
            feature_names=None,
            delimiter=',',
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
        assert end_of_frame is None or isinstance(end_of_frame, str), 'end_of_frame MUST be a stirng'
        assert num_features is None or isinstance(num_features, int) and num_features > 0, 'num_features MUST be greater than 0'
        assert feature_names is None or num_features is None or len(feature_names) == num_features, 'feature_names count MUST match num_features'

        self.port = port
        self.baud = baud
        self.start_of_frame = start_of_frame
        self.end_of_frame = end_of_frame
        self.num_features = num_features
        self.feature_names = feature_names
        self.delimiter = delimiter

    def collect_many_classes(
            self,
            dataset_name,
            num_samples=0,
            duration=0,
            timeout=5,
            decode=None,
            **kwargs
    ):
        """
        Collect samples for many classes
        :param duration:
        :param dataset_name: str
        :param num_samples: int
        :param timeout: int timeout for serial
        :return:
        """
        assert decode is None or callable(decode), 'decode MUST be callable'

        target_names = []
        X = []
        y = []
        target_idx = 0

        for target_name in self.ask_target_name():
            with Serial(port=self.port, baudrate=self.baud, timeout=timeout) as serial:
                # discard first line to be sure new line is properly formatted
                serial.readline()
                serial.reset_input_buffer()

                if duration > 0:
                    class_data = self._collect_by_duration(serial=serial, duration=duration, decode=decode)
                else:
                    class_data = self._collect_by_samples(serial=serial, num_samples=num_samples, decode=decode)

            print('Captured %d samples' % len(class_data))

            if input('Is this class ok? (y|n) ').strip().lower() != 'y':
                continue

            target_names.append(target_name)
            X += class_data
            y += [target_idx] * len(class_data)
            target_idx += 1

        assert len(X) > 0, 'No data captured'

        feature_names = [f'f{i}' for i in range(len(X[0]))] if self.feature_names is None else self.feature_names

        return Dataset(
            name=dataset_name,
            X=np.asarray(X),
            y=np.asarray(y, dtype=np.int),
            feature_names=feature_names,
            target_names=target_names
        )

    def collect_many_images(
            self,
            dataset_name,
            base_folder,
            shape,
            num_samples=0,
            duration=0,
            max_fps=0,
            timeout=5,
            **kwargs
    ):
        """
        Collect images for many classes
        :param shape:
        :param max_fps:
        :param base_folder:
        :param duration:
        :param dataset_name: str
        :param num_samples: int
        :param timeout: int timeout for serial
        :return:
        """
        target_names = []
        image_length = shape[0] * shape[1]

        for target_name in self.ask_target_name():
            with Serial(port=self.port, baudrate=self.baud, timeout=timeout) as serial:
                # discard first line to be sure new line is properly formatted
                serial.readline()
                serial.reset_input_buffer()

                stream = ByteStream(
                    source=lambda: serial.read(1024),
                    start_of_frame=self.start_of_frame,
                    end_of_frame=self.end_of_frame,
                    max_fps=max_fps
                )

                if duration > 0:
                    images = list(stream.collect_duration(duration))
                else:
                    images = list(stream.collect_samples(num_samples))

                print(f'Collected {len(images)} images')

                if input('Is this class ok? (y|n) ').strip().lower() != 'y':
                    continue

                assert len(images) > 0, 'No image captured'

                if not isdir(base_folder):
                    mkdir(base_folder, 0o777)

                if not isdir(f'{base_folder}/{target_name}'):
                    mkdir(f'{base_folder}/{target_name}', 0o777)

                for i, image in enumerate(images):
                    arr = np.asarray([int(b) for b in image], dtype=np.uint8)

                    if len(arr) == image_length:
                        imsave(f'{base_folder}/{target_name}/{time()}.{i}.jpg', arr.reshape(shape))

                target_names.append(target_name)

        return ImageDataset.from_nested_folders(
            name=dataset_name,
            base_folder=base_folder,
            file_types=['jpg'],
            only_folders=target_names
        )

    def _collect_by_duration(self, serial, duration, decode=None):
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
                try:
                    line = serial.readline().decode('utf-8').strip()
                except UnicodeDecodeError:
                    continue

                if decode is not None:
                    try:
                        record = decode(line)
                    except:
                        continue
                else:
                    if not self._line_is_well_formatted(line):
                        continue

                    record = [float(x) for x in self._trim(line).split(self.delimiter)]

                records.append(record)

                if last_tick != current_tick:
                    progress.update(1)
                    last_tick = current_tick

        return records

    def _collect_by_samples(self, serial, num_samples, decode):
        """
        Collect the given number of samples
        :param serial:
        :param num_samples:
        :param decode:
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
                try:
                    line = serial.readline().decode('utf-8').strip()
                except UnicodeDecodeError:
                    continue

                if decode is not None:
                    try:
                        record = decode(line)
                    except:
                        continue
                else:
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