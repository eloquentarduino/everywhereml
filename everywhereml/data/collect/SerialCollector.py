import numpy as np
from serial import Serial
from tqdm import tqdm
from everywhereml.data import Dataset


class SerialCollector:
    """
    Collect dataset from Serial port
    (mainly for Arduino projects)
    """
    def __init__(self, port, baud=9600, start_of_frame=None):
        """

        :param port:
        :param baud:
        :param start_of_frame:
        """
        self.port = port
        self.baud = baud
        self.start_of_frame = start_of_frame

    def collect_many_classes(self, dataset_name, num_samples=0, feature_names=None, delimiter=',', timeout=5):
        """
        Collect samples for many classes
        :param dataset_name: str
        :param num_samples: int
        :param feature_names: list
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
                    class_samples = num_samples
                    class_data = []

                    if len(target_name) == 0 and input('Are you sure you want to exit? (y|n) ').strip().lower() == 'y':
                        break

                    if len(target_name) == 0:
                        continue

                    if class_samples == 0:
                        class_samples = int(input('How many samples do you want to record? '))

                    # discard first line to be sure new line is properly formatted
                    serial.readline()
                    serial.reset_input_buffer()

                    with tqdm(total=class_samples) as progress:
                        captured_samples = 0

                        while captured_samples < class_samples:
                            line = serial.readline().decode('utf-8').strip()

                            if len(line) == 0 or (self.start_of_frame is not None and not line.startswith(self.start_of_frame)):
                                continue

                            if self.start_of_frame is not None:
                                line = line.replace(self.start_of_frame, '').strip()

                            data = [float(x) for x in line.split(delimiter)]

                            if feature_names is None:
                                feature_names = [f'f{i}' for i in range(len(data))]

                            if len(feature_names) != len(data):
                                continue

                            class_data.append(data)
                            captured_samples += 1
                            progress.update(1)

                    if input('Is this class ok? (y|n) ').strip().lower() != 'y':
                        continue

                    target_names.append(target_name)
                    X += class_data
                    y += [target_idx] * len(class_data)
                    target_idx += 1
                except ValueError:
                    pass

            assert len(X) > 0, 'No data captured'

            return Dataset(name=dataset_name, X=np.asarray(X), y=np.asarray(y, dtype=np.int), feature_names=feature_names, target_names=target_names)