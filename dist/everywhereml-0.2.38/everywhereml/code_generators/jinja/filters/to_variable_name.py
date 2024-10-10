from slugify import slugify


def to_variable_name(name: str) -> str:
    """
    Convert name to well formed variable name
    :param name:
    :return:
    """
    return slugify(name).replace('-', '_')
