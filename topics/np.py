from typing import List, Union

import numpy as np


def save_numpy(inputs: Union[List, np.ndarray], path: str):
    arr: np.ndarray = np.array(inputs) if isinstance(inputs, list) else inputs
    np.save(file=path, arr=arr)


def load_numpy(path: str, as_list: bool = False):
    arr = np.load(path)
    return arr if not as_list else list(arr)
