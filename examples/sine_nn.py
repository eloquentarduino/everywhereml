import math
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers
from everywhereml.code_generators.tensorflow import tf_porter


def get_model():
    SAMPLES = 1000
    np.random.seed(1337)
    x_values = np.random.uniform(low=0, high=2*math.pi, size=SAMPLES)

    # shuffle and add noise
    np.random.shuffle(x_values)
    y_values = np.sin(x_values)
    y_values += 0.1 * np.random.randn(*y_values.shape)

    # split into train, validation, test
    TRAIN_SPLIT =  int(0.6 * SAMPLES)
    TEST_SPLIT = int(0.2 * SAMPLES + TRAIN_SPLIT)
    x_train, x_test, x_validate = np.split(x_values, [TRAIN_SPLIT, TEST_SPLIT])
    y_train, y_test, y_validate = np.split(y_values, [TRAIN_SPLIT, TEST_SPLIT])

    # create a NN with 2 layers of 16 neurons
    model = tf.keras.Sequential()
    model.add(layers.Dense(16, activation='relu', input_shape=(1,)))
    model.add(layers.Dense(16, activation='relu'))
    model.add(layers.Dense(1))
    model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
    model.fit(x_train, y_train, epochs=50, batch_size=16, validation_data=(x_validate, y_validate))

    return model, x_train, y_train


if __name__ == '__main__':
    tf_model, x_train, y_train = get_model()
    cpp_code = tf_porter(tf_model, x_train, y_train).to_cpp(instance_name='sineNN', arena_size=4096)

    print(cpp_code)