import requests
from os import mkdir
from os.path import isdir
from time import time
from everywhereml.data import ImageDataset


class MjpegCollector:
    """
    Collect frames from MJPEG HTTP stream
    """
    def __init__(self, address, max_fps=0):
        """

        :param address:
        :param max_fps:
        """
        self.address = address
        self.max_fps = max_fps

    def collect_many_classes(self, dataset_name, base_folder, samples_per_class=0, duration=0, preview=False):
        """

        :param dataset_name:
        :param base_folder:
        :param num_samples:
        :param duration:
        :param preview:
        :return:
        """
        assert samples_per_class > 0 or duration > 0, 'you MUST set either samples_per_class or duration'

        print('This is an interactive data capturing procedure.')
        print('Keep in mind that as soon as you will enter a class name, the capturing will start, so be ready!')

        while True:
            try:
                target_name = input('Which class are you going to capture? (leave empty to exit) ').strip()

                if len(target_name) == 0 and input('Are you sure you want to exit? (y|n) ').strip().lower() == 'y':
                    break

                if len(target_name) == 0:
                    continue

                if duration > 0:
                    images = self.collect_by_duration(duration)
                else:
                    images = self.collect_by_samples(samples_per_class)

                print('Captured %d images' % len(images))

                if input('Is this class ok? (y|n) ').strip().lower() != 'y':
                    continue

                # save to disk
                if not isdir(base_folder):
                    print(f'creating {base_folder} folder')
                    mkdir(base_folder)

                if not isdir(f'{base_folder}/{target_name}'):
                    print(f'creating {base_folder}/{target_name} folder')
                    mkdir(f'{base_folder}/{target_name}')

                timestamp = time()

                for i, im in enumerate(images):
                    with open(f'{base_folder}/{target_name}/{timestamp}_{i}.jpg', 'wb') as file:
                        file.write(im)
            except Exception as ex:
                print('ex', ex)

        return ImageDataset.from_nested_folders(
            name=dataset_name,
            base_folder=base_folder,
            file_types=['jpg']
        )

    def collect_by_duration(self, duration):
        """
        Collect for a given duration
        :param duration:
        :return:
        """
        return self._collect(stop=lambda _i, _duration: _duration >= duration)

    def collect_by_samples(self, num_samples):
        """
        Collect a given number of samples
        :param num_samples:
        :return:
        """
        return self._collect(stop=lambda _i, _duration: _i >= num_samples)

    def _collect(self, stop):
        """
        Collect until stop condition
        :param stop: callable
        :return:
        """
        bytes = b''
        count = 0
        start = time()
        last_frame = start
        frames = []

        with requests.get(self.address, stream=True) as res:
            for data in res.iter_content(1024):
                bytes += data
                a = bytes.find(b'\xff\xd8')
                b = bytes.find(b'\xff\xd9')

                if a != -1 and b != -1:
                    jpg = bytes[a:b + 2]
                    bytes = bytes[b + 2:]

                    if self.max_fps == 0 or time() - last_frame >= 1.0 / self.max_fps:
                        frames.append(jpg)
                        count += 1
                        last_frame = time()

                if stop(count, time() - start):
                    break

        return frames


"""
How to use

mjpeg_collector = MjpegCollector(
    address='http://192.168.1.100',
    max_fps=10
)
image_dataset = mjpeg_collector.collect_many_classes(
    dataset_name='Dataset', 
    base_folder='dataset',
    duration=20
)
"""