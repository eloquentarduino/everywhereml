def to_py_comment(x):
    """
    Convert string or list to Python-style comment block
    :param x:
    :return:
    """
    if isinstance(x, str):
        x = x.split('\n')

    return '\n'.join([f'# {line}' for line in x])