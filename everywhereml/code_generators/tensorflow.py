import hexdump
import numpy as np
import tensorflow as tf
from everywhereml.code_generators import GeneratesCode
from everywhereml.code_generators.jinja.Jinja import Jinja


def convert_model(model, X: np.ndarray, y: np.ndarray, model_name: str = 'tfData') -> str:
    """
    Convert model to C++ header
    :param model_name:
    :param model:
    :param X:
    :param y:
    :return:
    """
    assert y.dtype != int or len(y.shape) == 2, 'y must be of dtype=float (regression) or one-hot encoded'

    num_inputs = X.shape[1] if len(X.shape) > 1 else 1
    num_outputs = 1 if y.dtype != int else y.shape[1]
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    bytes = hexdump.dump(converter.convert()).split(' ')
    bytes_array = ', '.join(['0x%02x' % int(byte, 16) for byte in bytes])
    model_size = len(bytes)

    # give user hint of which layers to include
    unique_layers = set([l.__class__.__name__ for l in model.layers])
    layer_mapping = {
        'Add': 'Add',
        'AveragePooling2D': 'AveragePool2D',
        'Concatenate': 'Concatenation',
        'Conv2D': 'Conv2D',
        'DepthwiseConv2D': 'DepthwiseConv2D',
        'ELU': 'Elu',
        'Dense': 'FullyConnected',
        'LeakyReLU': 'LeakyRelu',
        'MaxPool2D': 'MaxPool2D',
        'Maximum': 'Maximum',
        'Minimum': 'Minimum',
        'ReLU': 'Relu',
        'Reshape': 'Reshape',
        'Softmax': 'Softmax'
    }

    if num_outputs > 1:
        unique_layers.add('Softmax')

    allowed_unique_layers = [layer_mapping[l] for l in unique_layers if l in layer_mapping.keys()]
    not_allowed_unique_layers = [l for l in unique_layers if l not in layer_mapping.keys()]

    # generate one sample for each class
    y_ord = list(np.argmax(y, axis=1))
    samples_idx = [y_ord.index(i) for i in sorted(list(set(y_ord)))]
    x_samples = [X[i] for i in samples_idx]
    y_samples = [y_ord[i] for i in samples_idx]

    return Jinja(base_folder='', language='cpp', dialect=None).render('convert_tf_model', {
        'num_inputs': num_inputs,
        'num_outputs': num_outputs,
        'bytes_array': bytes_array,
        'model_size': model_size,
        'allowed_layers': allowed_unique_layers,
        'not_allowed_layers': not_allowed_unique_layers,
        'model_name': model_name or 'tfData',
        'x_samples': x_samples,
        'y_samples': y_samples
    })


class TensorFlowPorter(GeneratesCode):
    """
    Convert TF models to C++
    @deprecated
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