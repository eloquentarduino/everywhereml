from everywhereml.code_generators.GeneratesCode import GeneratesCode


class Pipeline(GeneratesCode):
    """
    Run many pre-processing steps in sequence
    """
    def __init__(self, steps, name=''):
        """
        Constructor
        :param steps: list
        :param name: str
        """
        self.steps = steps
        self.name = name
        self.dataset = None
        self.num_inputs = 0
        self.num_outputs = 0
        self.working_size = 0

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
        steps = [' > %s' % str(step) for step in self.steps]

        return 'Pipeline:\n---------\n' + '\n'.join(steps)

    def describe(self):
        """
        Convert to string
        :return:
        """
        return str(self)

    def fit(self, dataset):
        """
        Fit dataset
        :param dataset:
        :return:
        """
        self.num_inputs = dataset.num_inputs

        for step in self.steps:
            step.fit(dataset)
            dataset = step.transform(dataset)
            self.working_size = max(self.working_size, dataset.num_inputs)

        self.dataset = dataset
        self.num_outputs = dataset.num_inputs

        return self

    def transform(self, dataset):
        """
        Transform dataset
        :param dataset:
        :return:
        """
        assert self.dataset is not None, 'Unfitted'

        for step in self.steps:
            dataset = step.transform(dataset)

        self.dataset = dataset

        return dataset

    def fit_transform(self, dataset):
        """
        Fit then transform dataset
        :param dataset:
        :return:
        """
        return self.fit(dataset).dataset

    def get_template_data(self):
        """
        Get data for code generation
        :return: dict
        """
        assert self.dataset is not None, 'Unfitted'

        return {
            'pipeline': self,
            'steps': self.steps,
            'dataset': self.dataset,
            'num_inputs': self.num_inputs,
            'num_outputs': self.num_outputs,
            'working_size': self.working_size
        }