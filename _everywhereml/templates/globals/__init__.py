import numpy as np
from everywhereml.templates.globals.chunk import chunk, chunk_indices


globals = {
    'list': list,
    'enumerate': enumerate,
    'isinstance': isinstance,
    'zip': zip,
    'chunk': chunk,
    'chunk_indices': chunk_indices,
    'np': np
}
