from everywhereml.preprocessing.image import HOG
from everywhereml.preprocessing.image.object_detection.BaseObjectDetectionPipeline import BaseObjectDetectionPipeline


class HogPipeline(BaseObjectDetectionPipeline):
    """
    Classify objects by Histogram of Oriented Gradients (HOG)
    """
    def __init__(self, hog_params: dict = None, **kwargs):
        """

        :param hog_params:
        :param kwargs:
        """
        kwargs.setdefault('name', 'HogPipeline')
        BaseObjectDetectionPipeline.__init__(self, **kwargs)
        self.steps = [HOG(**(hog_params or {}))]
