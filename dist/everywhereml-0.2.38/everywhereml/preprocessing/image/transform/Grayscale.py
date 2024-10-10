from skimage.color import rgb2gray, yuv2rgb


class Grayscale:
    """
    Convert color images to grayscale
    """
    def __init__(self, pixformat: str):
        """
        Constructor
        :param pixformat:
        """
        assert pixformat in ('gray', 'rgb', 'rgb5656', 'rgb888', 'yuv422')

        self.pixformat = pixformat

    def transform(self, image):
        """

        :param image:
        :return:
        """
        if self.pixformat == 'gray':
            return image
        if self.pixformat in ('rgb', 'rgb565', 'rgb888'):
            return rgb2gray(image)
        if self.pixformat == 'yuv422':
            return rgb2gray(yuv2rgb(image))
        raise ValueError(f'Bad pixformat: {self.pixformat}')
