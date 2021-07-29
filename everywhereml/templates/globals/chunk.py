def chunk(lst, n):
    """
    Yield successive n-sized chunks from lst
    :param lst: list
    :param n: int
    :return: generator
    """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def chunk_indices(size, n):
    """
    Yield successive n-sized indices up to size
    :param size: int
    :param n: int
    :return: generator
    """
    for i in range(0, size, n):
        yield i, min(size, i + n)
