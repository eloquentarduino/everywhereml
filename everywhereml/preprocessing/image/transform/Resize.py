from skimage.transform import resize
from everywhereml.code_generators import GeneratesCode


class Resize(GeneratesCode):
    """
    Resize image
    """
    def __init__(self, width: int, height: int, pixformat: str = None):
        """
        Constructor
        :param width:
        :param height:
        :param pixformat:
        """
        assert width > 0, 'width MUST be greater than 0'
        assert height > 0, 'height MUST be greater than 0'
        assert pixformat is None or pixformat in ('gray', 'rgb565', 'rgb888', 'yuv422'), 'pixformat MUST be one of (gray, rgb565, rgb888, yuv422)'

        # relative width
        if width < 1 < height:
            width *= height

        # relative height
        if height < 1 < width:
            height *= width

        assert width > 1 and height > 1, 'width and height CANNOT be both relative'

        self.width = width
        self.height = height
        self.pixformat = None
        self.input_shape = None

    def __repr__(self):
        """

        :return:
        """
        return str(self)

    def __str__(self):
        """

        :return:
        """
        input_shape = self.input_shape or ('?', '?')

        return f'Resize(from=({input_shape[1]}, {input_shape[0]}), to=({self.width}, {self.height}), pixformat={self.pixformat})'

    def __call__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        return self.transform(*args, **kwargs)

    def transform(self, image, *args, **kwargs):
        """

        :param image:
        :return:
        """
        if len(image.shape) == 2 or image.shape[2] == 1:
            self.pixformat = 'gray'
        else:
            assert self.pixformat != 'gray', 'pixformat is gray, but image has 3 components'

        self.input_shape = image.shape

        return resize(image, (self.height, self.width))

    def get_template_data(self) -> dict:
        """

        :return: dict
        """
        return {
            'source_width': self.input_shape[1],
            'source_height': self.input_shape[0],
            'dest_width': self.width,
            'dest_height': self.height,
            'pixformat': self.pixformat
        }
