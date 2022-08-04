import numpy as np
import os.path
import random
from os import listdir
from skimage.io import imread
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
from skimage import transform
from skimage.transform import resize, rotate, AffineTransform
from skimage.util import random_noise
from skimage.filters import gaussian
from skimage.exposure import adjust_log
from everywhereml.data import Dataset


class ImageDataset:
    """
    Dataset of images
    """
    @staticmethod
    def from_nested_folders(name, base_folder, file_types=None, skip_folders=None, only_folders=None, images_per_folder=0):
        """
        Load images from nested folders
        :param images_per_folder:
        :param only_folders:
        :param skip_folders:
        :param file_types:
        :param name:
        :param base_folder:
        :return:
        """
        if file_types is None:
            file_types = ['jpg', 'jpeg', 'png']

        # ignore file type case
        file_types = [ftype.lower() for ftype in file_types]

        images = []
        labels = []

        if skip_folders is None:
            skip_folders = []

        for child_folder in sorted(listdir(base_folder)):
            label = child_folder
            child_folder = f'{base_folder}/{child_folder}'

            if not os.path.isdir(child_folder):
                continue

            if label in skip_folders:
                continue

            if only_folders is not None and label not in only_folders:
                continue

            for i, filename in enumerate(sorted(listdir(child_folder))):
                if 0 < images_per_folder < i:
                    break

                image_name, ext = os.path.splitext(filename)

                if ext[1:].lower() not in file_types:
                    continue

                images.append(imread(f'{child_folder}/{filename}'))
                labels.append(label)

        return ImageDataset(name=name, images=images, labels=labels)

    @staticmethod
    def from_csv(filename: str, shape: tuple, name=None, **kwargs):
        """

        :param filename: str
        :param shape: tuple
        :param name: str
        :return:
        """
        if name is None:
            name = os.path.basename(filename)

        dataset = Dataset.from_csv(filename=filename, name=name, **kwargs)
        images = dataset.X.reshape((-1,) + shape)
        labels = [dataset.target_names[yi] for yi in dataset.y.astype(np.uint8)]

        return ImageDataset(
            name=name,
            images=images,
            labels=labels
        )

    def __init__(self, name, images, labels, **kwargs):
        """

        :param name:
        :param images:
        :param labels:
        """
        self.name = name
        self.images = np.asarray(images)
        self.labels = labels

    def __str__(self):
        """
        Describe dataset
        :return:
        """
        return f'ImageDataset[{self.name}](num_images={len(self.images)}, num_labels={len(self.target_names)}, labels={self.target_names})'

    @property
    def target_names(self):
        """
        Get unique labels list
        :return: list
        """
        target_names = []

        for label in self.labels:
            if label not in target_names:
                target_names.append(label)

        return target_names

    @property
    def num_classes(self):
        """
        Get number of classes
        :return: int
        """
        return len(self.target_names)

    @property
    def shape(self):
        """
        Get shape of images
        :return: tuple
        """
        return self.images[0].shape

    @property
    def width(self):
        """
        Get images' width
        :return: int
        """
        return self.shape[1]

    @property
    def height(self):
        """
        Get images' height
        :return: int
        """
        return self.shape[0]

    @property
    def depth(self):
        """
        Get images' depth
        :return: int
        """
        return self.shape[2] if len(self.shape) == 3 else 1

    @property
    def num_inputs(self):
        """
        Get number of inputs
        :return:
        """
        return self.width * self.height * self.depth

    @property
    def X(self):
        """

        :return:
        """
        return np.asarray(self.images, dtype=self.images[0].dtype).reshape((-1, self.num_inputs))

    @property
    def y(self):
        """

        :return:
        """
        inverse_classmap = {label: i for i, label in enumerate(self.target_names)}

        return np.asarray([inverse_classmap[label] for label in self.labels], dtype=np.uint8)

    def class_iterator(self):
        """

        :return:
        """
        y = self.y

        for class_idx in range(self.num_classes):
            images = self.images[y == class_idx]

            yield class_idx, images

    def clone(self, shallow=True, **kwargs):
        """

        :param shallow:
        :return:
        """
        kwargs = {
            **self.__dict__,
            **kwargs
        }

        if not shallow:
            kwargs['images'] = [np.copy(im) for im in kwargs['images']]

        return ImageDataset(**kwargs)

    def uint8(self):
        """
        Convert images to uint8
        :return:
        """
        if np.asarray(self.images).max() <= 1:
            images = [(im * 255).astype(np.uint8) for im in self.images]
        else:
            images = self.images

        return self.clone(images=images)

    def gray(self):
        """
        Convert images to grayscale
        :return:
        """
        if self.depth == 3:
            return self.clone(images=[rgb2gray(im) for im in self.images])

        return self

    def log_gradient(self):
        """

        :return:
        """
        log_images = [np.log(1 + im.astype(np.uint16)) for im in self.images]
        gradient_images = [im[2:, 1:-1] - im[0:-2, 1:-1] + im[1:-1, 2:] - im[1:-1, :-2] for im in log_images]

        return self.clone(images=gradient_images)

    def resize(self, new_shape, **kwargs):
        """
        Resize images to new shape
        :param new_shape:
        :return:
        """
        return self.clone(images=[resize(im, new_shape, **kwargs) for im in self.images])

    def map(self, fn):
        """
        Map images and labels
        :param fn:
        :return:
        """
        mapped = [fn(im, label) for im, label in zip(self.images, self.labels)]
        self.images = [m[0] if len(m) == 2 else m for m in mapped]
        self.labels = [m[1] if len(m) == 2 else label for m, label in zip(mapped, self.labels)]

        return self

    def apply(self, pipeline):
        """
        Apply pipeline
        :param pipeline:
        :return:
        """
        dataset = pipeline.fit_transform(self)

        return self.clone(**dataset.__dict__)

    def preview(self, samples_per_class, rows_per_class=1, figsize=(20, 10), **kwargs):
        """
        Show preview of images
        :param rows_per_class: int
        :param samples_per_class: int
        :param figsize:
        :return:
        """
        rows = self.num_classes * rows_per_class
        cols = samples_per_class // rows_per_class
        fig, ax = plt.subplots(rows, cols)
        fig.set_size_inches(figsize[0], figsize[1])

        for i, images in self.class_iterator():
            for j, k in enumerate(np.random.choice(len(images), samples_per_class)):
                row = j // cols
                col = j % cols
                ax[i * rows_per_class + row, col].imshow(images[k], **kwargs)

    def augment(
            self,
            augment_factor,
            scale_range=(1, 1.2),
            rotation_range=(-20, 20),
            translation_range=(-10, 10),
            illumination_range=(-0.1, 0.1),
            contrast_range=(0.95, 1.05),
            shear_range=(-0.05, 0.05),
            noise_range=(0.001, 0.002),
            blur_range=(0.9, 1.1)
    ):
        """
        Perform image augmentation
        :param translation_range:
        :param scale_range:
        :param blur_range:
        :param noise_range:
        :param shear_range:
        :param augment_factor:
        :param rotation_range:
        :param illumination_range:
        :param contrast_range:
        :return:
        """
        augmented_images = []
        augmented_labels = []
        target_names = self.target_names
        M = 255 if self.images.max() > 1 else 1

        def lin(r):
            return np.linspace(*r, 30)

        def cap(im):
            return np.where(im > 1, 1, np.where(im < 0, 0, im))

        def roi(im):
            h, w = self.images[0].shape[:2]
            H, W = im.shape[:2]
            return im[H // 2 - h // 2:H // 2 - h // 2 + h, W // 2 - w // 2:W // 2 - w // 2 + W]

        available_transforms = [
            [lambda im: roi(resize(im, (im.shape[0] * zoom, im.shape[1] * zoom))) for zoom in lin(scale_range)] if scale_range is not None else None,
            [lambda im: rotate(im, angle, mode='edge') for angle in lin(rotation_range)] if rotation_range is not None else None,
            [lambda im: transform.warp(im, AffineTransform(translation=(t, 0)), mode='edge') for t in lin(translation_range)] if translation_range is not None else None,
            [lambda im: transform.warp(im, AffineTransform(translation=(0, t)), mode='edge') for t in lin(translation_range)] if translation_range is not None else None,
            [lambda im: cap(im + illu) for illu in lin(illumination_range)] if illumination_range is not None else None,
            [lambda im: adjust_log(im, gain) for gain in lin(contrast_range)] if contrast_range is not None else None,
            [lambda im: transform.warp(im, AffineTransform(shear=shear), mode='edge') for shear in lin(shear_range)] if shear_range is not None else None,
            [lambda im: random_noise(im, var=noise) for noise in lin(noise_range)] if noise_range is not None else None,
            [lambda im: gaussian(im, sigma=sigma) for sigma in lin(blur_range)] if blur_range is not None else None,
        ]
        available_transforms = [t for t in available_transforms if t is not None]

        for class_idx, images in self.class_iterator():
            images_to_generate = int(len(images) * augment_factor)

            while images_to_generate > 0:
                im = random.choice(images)
                num_transformations_to_apply = random.randint(1, len(available_transforms))
                transform_indices = np.random.choice(np.arange(len(available_transforms)), size=num_transformations_to_apply, replace=False)
                transforms = [random.choice(available_transforms[i]) for i in transform_indices]

                if M > 1:
                    im = im.astype(np.float) / 255

                for t in transforms:
                    im = t(im)

                if im.shape != self.images[0].shape:
                    continue

                if M >= 1:
                    im = (im * 255).astype(np.uint8)

                augmented_images.append(im)
                augmented_labels.append(target_names[class_idx])
                images_to_generate -= 1

        self.augmented_images = augmented_images
        augmented_images = np.asarray(augmented_images, dtype=self.images.dtype).reshape((-1,) + self.images.shape[1:])

        return self.clone(images=np.vstack((self.images, augmented_images)), labels=self.labels + augmented_labels)



