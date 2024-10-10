import re


def basic_python_prettify(python_code):
    """
    Apply basic Python prettifying
    :param python_code: str
    :return: str
    """
    blank_lines_re1 = re.compile(r'\n\s*\n([ \t]+)(if|else|while|return)')
    blank_lines_re2 = re.compile(r'\n\s*\n\s*\n([ \t]+)def ')
    blank_lines_re3 = re.compile(r'\n\s*\n\s*\n')

    for i in range(10):
        python_code = blank_lines_re1.sub(lambda m: f'\n{m.group(1)}{m.group(2)}', python_code)
        python_code = blank_lines_re2.sub(lambda m: f'\n\n{m.group(1)}def ', python_code)
        python_code = blank_lines_re3.sub('\n\n', python_code)

    return python_code.strip()