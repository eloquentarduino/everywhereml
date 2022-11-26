from everywhereml.code_generators.GeneratesCode import GeneratesCode


class BaseObjectDetectionPipeline(GeneratesCode):
    """
    Base class for object detection pipelines
    """
    def __init__(self, transforms: list = None, name: str = 'ObjectDetectionPipeline', **kwargs):
        """
        Constructor
        :param name: str
        :param transforms: list
        """
        self.name = name
        self.dataset = None
        self.transformed_dataset = None
        self.transforms = transforms or []
        self.num_inputs = 0
        self.num_outputs = 0
        self.input_shape = None
        self.transformed_shape = None

    def __repr__(self):
        """
        Convert to string
        :return:
        """
        return str(self)

    def __str__(self):
        """
        Convert to string
        :return:
        """
        transforms = '\n'.join([' - %s' % str(transform) for transform in self.transforms])
        steps = '\n'.join([' > %s' % str(step) for step in self.steps])

        return f'ImagePipeline: {self.name}\n---------\n{transforms}\n{steps}'

    def fit(self, image_dataset):
        """
        Fit pipeline
        :param image_dataset:
        :return:
        """
        self.input_shape = image_dataset.images[0].shape
        self.transformed_dataset = image_dataset = self.preprocess(image_dataset)
        self.num_inputs = image_dataset.num_inputs
        self.transformed_shape = self.transformed_dataset.images[0].shape

        for step in self.steps:
            step.fit(image_dataset)
            image_dataset = step.transform(image_dataset)

        self.dataset = image_dataset
        self.num_outputs = image_dataset.num_inputs

        return self

    def transform(self, image_dataset):
        """
        Transform dataset
        :param image_dataset:
        :return:
        """
        assert self.dataset is not None, 'Unfitted'
        image_dataset = self.preprocess(image_dataset)

        for step in self.steps:
            image_dataset = step.transform(image_dataset)

        self.dataset = image_dataset

        return image_dataset

    def fit_transform(self, image_dataset):
        """
        Fit then transform image_dataset
        :param image_dataset:
        :return:
        """
        return self.fit(image_dataset).dataset

    def preprocess(self, image_dataset):
        """
        Apply pre-processing transforms
        :param image_dataset:
        :return:
        """
        for transform in self.transforms:
            image_dataset = image_dataset.map(transform)

        return image_dataset

    def get_template_data(self):
        """

        :return: dict
        """
        return {
            'name': self.name,
            'transforms': self.transforms,
            'steps': self.steps,
            'num_inputs': self.num_inputs,
            'num_outputs': self.num_outputs,
            'source_width': self.input_shape[1],
            'source_height': self.input_shape[0],
            'transformed_shape': self.transformed_shape
        }

    def get_template_data_cpp(self, dialect=None):
        """

        :return: dict
        """
        working_size = max([step.num_outputs for step in self.steps])

        return {
            'working_size': working_size
        }
