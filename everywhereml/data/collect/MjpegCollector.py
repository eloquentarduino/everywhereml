import requests
from os import mkdir
from os.path import isdir, join, abspath
from time import time, sleep
from tqdm.auto import tqdm
from logging import info, debug, warning
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
        print('Keep in mind that when you enter a class name, the capturing will start in 2 seconds, so be ready!')

        while True:
            try:
                target_name = input('Which class are you going to capture? (leave empty to exit) ').strip()

                if len(target_name) == 0 and input('Are you sure you want to exit? (y|n) ').strip().lower() == 'y':
                    break

                if len(target_name) == 0:
                    continue

                # allow some time for the user to settle
                sleep(2)

                if duration > 0:
                    images = self.collect_by_duration(duration)
                else:
                    images = self.collect_by_samples(samples_per_class)

                info('Captured %d images' % len(images))

                if input('Is this class ok? (y|n) ').strip().lower()[0] != 'y':
                    continue

                # save to disk
                if not isdir(base_folder):
                    info(f'creating {abspath(base_folder)} folder')
                    mkdir(base_folder)

                # make sure folder is created
                while not isdir(base_folder):
                    info(f'Folder {abspath(base_folder)} does not exists and cannot be created. Please create manually')
                    input('Press [Enter] when you\'re done')

                target_folder = abspath(join(base_folder, target_name))

                if not isdir(target_folder):
                    info(f'creating {target_folder} folder')
                    mkdir(target_folder)

                # make sure folder is created
                while not isdir(target_folder):
                    info(f'Folder {target_folder} does not exists and cannot be created. Please create manually')
                    input('Press [Enter] when you\'re done')

                timestamp = time()

                for i, im in enumerate(images):
                    image_path = join(target_folder, f'{timestamp}_{i}.jpg')

                    with open(image_path, 'wb') as file:
                        debug(f'Saving image to {image_path}')
                        file.write(im)
            except Exception as ex:
                warning(ex)

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
        return self._collect(progress=lambda _i, _duration: _duration / duration)

    def collect_by_samples(self, num_samples):
        """
        Collect a given number of samples
        :param num_samples:
        :return:
        """
        return self._collect(progress=lambda _i, _duration: _i / num_samples)

    def _collect(self, progress):
        """
        Collect until progress reaches 1
        :param progress: callable
        :return:
        """
        bytes = b''
        count = 0
        start = time()
        last_frame = start
        last_progress = 0
        frames = []

        with tqdm(total=100) as progress_bar:
            with requests.get(self.address, stream=True) as res:
                for data in res.iter_content(1024):
                    bytes += data
                    a = bytes.find(b'\xff\xd8')
                    b = bytes.find(b'\xff\xd9')

                    if a != -1 and b != -1:
                        debug("detected new jpeg frame")
                        jpg = bytes[a:b + 2]
                        bytes = bytes[b + 2:]

                        if self.max_fps == 0 or time() - last_frame >= 1.0 / self.max_fps:
                            debug("appending to dataset")
                            frames.append(jpg)
                            count += 1
                            last_frame = time()

                    current_progress = progress(count, time() - start)
                    progress_bar.update(100 * (current_progress - last_progress))
                    last_progress = current_progress

                    if current_progress >= 1:
                        break

        return frames
