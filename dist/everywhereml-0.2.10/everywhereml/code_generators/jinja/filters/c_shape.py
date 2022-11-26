from everywhereml.code_generators.jinja.helpers import is_list


def c_shape(arr):
    """
    Convert array shape to C format
    :param arr:
    :return:
    """
    current = arr
    shapes = []

    while is_list(current):
        shapes.append(str(len(current)))
        current = current[0]

    return ']['.join(shapes)