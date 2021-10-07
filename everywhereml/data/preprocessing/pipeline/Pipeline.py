from copy import copy
from collections.abc import Iterable
from everywhereml.IsPortableMixin import IsPortableMixin
from everywhereml.data.preprocessing.BaseTransformer import BaseTransformer
from everywhereml.classification.utils import to_Xy


class Pipeline(BaseTransformer):
    def __init__(self, name=None, steps=None):
        """
        Constructor
        :param name: str
        :param steps: list
        """
        super().__init__(name or "Pipeline")

        assert isinstance(steps, Iterable), "steps MUST be an Iterable object"

        self.steps = []
        self.X_input = None
        self.y_input = None
        self.X_output = None
        self.y_output = None

        for step in steps:
            if isinstance(step, tuple):
                assert len(step) == 2, "when step is a tuple, is MUST be in the form (name, transformer)"
                name, step = step
                self.add(step, name=name)
            else:
                self.add(step)

    def __len__(self):
        """
        Returns the length of the Pipeline
        """
        return len(self.steps)

    def __getitem__(self, item):
        """
        Get a single item (by index or name) or a slice of the pipeline
        :param item: int|str|slice
        :return: step|Pipeline
        """
        if isinstance(item, int):
            return self.steps[item]

        elif isinstance(item, str):
            return [step for name, step in self.steps if name == item][0]

        elif isinstance(item, slice):
            if isinstance(item.start, int):
                start = item.start
            elif isinstance(item.start, str):
                start = self.index_of(item.start)
            else:
                start = 0

            if isinstance(item.stop, int):
                stop = item.stop
            elif isinstance(item.stop, str):
                stop = self.index_of(item.stop)
            else:
                stop = len(self.steps)

            return Pipeline("Slice of %s" % self.name, [copy(step) for step in self.steps[start:stop]])
        else:
            raise AssertionError("item MUST be either an int, a string or a slice: %s given" % str(type(item)))

    def __str__(self):
        """
        Convert to string
        :return: str
        """
        steps = "\n + ".join([str(step) for step in self.steps])

        return "Pipeline %s (%s)" % (self.name, steps)

    def __repr__(self):
        """
        Convert to string
        :return: str
        """
        return str(self)

    @property
    def input_shape(self):
        """
        Get input shape
        :param: tuple
        """
        return self.X_input.shape

    @property
    def output_shape(self):
        """
        Get output shape (only works after fit())
        """
        return self.X_output.shape

    def add(self, step, name=None):
        """
        Add step to pipeline
        :param step: Transformer
        :param name: str
        :return: self
        """
        if name is None:
            name = step.name

        assert hasattr(step, "fit"), "steps MUST implement fit()"
        assert hasattr(step, "transform") or hasattr(step, "predict"), "steps MUST implement transform() or predict()"
        assert all(step_name != name for step_name, step in self.steps), "step names MUST be unique: %s is already in use" % name

        self.steps.append((name, step))

    def clone(self):
        """
        Clone pipeline
        :return: Pipeline
        """
        return self[:]

    def _fit(self, X, y=None, **kwargs):
        """
        Fit data to steps
        :param X:
        :param y:
        :param kwargs:
        :return: X, y
        """
        self.X_input, self.y_input = to_Xy(X, y, allow_y_none=True)
        Xt = self.X_input
        yt = self.y_input

        for name, step in self.steps:
            step.fit(Xt, yt, **kwargs)

            if hasattr(step, "transform"):
                Xt, yt = step.transform(Xt, yt)
            else:
                Xt = step.predict(Xt)

        self.X_output = Xt
        self.y_output = yt

        return self

    def _transform(self, X, y=None, **kwargs):
        """
        Transform data
        :param X:
        :param y:
        :param kwargs:
        :return: X, y
        """
        Xt, yt = to_Xy(X, y, allow_y_none=True)

        for name, step in self.steps:
            if hasattr(step, "transform"):
                Xt, yt = step.transform(Xt, yt)
            else:
                # when a predictor is in the pipeline, return y_pred as Xt
                Xt = step.predict(Xt)

            # Xt must ALWAYS be a NxM matrix
            if len(Xt.shape) == 1:
                Xt = Xt.reshape((-1, 1))

        return Xt, yt if y is not None else Xt

    def index_of(self, name):
        """
        Get index of given step
        :param name: str
        :return: int
        """
        for i, (step_name, step) in enumerate(self.steps):
            if step_name == name:
                return i

        raise IndexError("no step named %s found" % name)

    def get_template_data(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        return {
            "steps": self.steps,
        }

    def get_template_data_cpp(self):
        """

        :return:
        """
        template_data = super(Pipeline, self).get_template_data_cpp()
        template_data.update(**{
            "buffer_size": max(max(step.output_dim, step.cpp_buffer_size) for name, step in self.steps),
            "_buffer_size": max(1, max(step.cpp_buffer_size for name, step in self.steps))
        })

        return template_data
