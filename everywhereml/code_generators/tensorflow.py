import hexdump
import tensorflow as tf
from everywhereml.code_generators import GeneratesCode


class TensorFlowPorter(GeneratesCode):
    """
    Convert TF models to C++
    """
    def __init__(self, model, X, y):
        """

        :param model:
        """
        self.model = model
        self.num_inputs = X.shape[1] if len(X.shape) > 1 else 1

        if y.dtype == int:
            self.num_outputs = len(set(y)) if len(y.shape) == 1 or y.shape[1] == 1 else y.shape[1]
        else:
            # float ys -> regression
            self.num_outputs = 1

    def get_template_data(self):
        """

        :return:
        """
        return {
            'num_inputs': self.num_inputs,
            'num_outputs': self.num_outputs
        }

    def get_template_data_cpp(self, **kwargs):
        """

        :return:
        """
        converter = tf.lite.TFLiteConverter.from_keras_model(self.model)
        converted = converter.convert()
        bytes = hexdump.dump(converted).split(' ')
        bytes_array = ', '.join(['0x%02x' % int(byte, 16) for byte in bytes])

        return {
            'model_size': len(bytes),
            'bytes_array': bytes_array
        }


def tf_porter(*args, **kwargs):
    """
    Factory method
    :param kwargs:
    :return:
    """
    return TensorFlowPorter(*args, **kwargs)