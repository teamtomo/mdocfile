import re
from typing import List, Union

camel_to_snake_regex = re.compile(r'(?<!^)(?=[A-Z])')


def camel_to_snake(word: str) -> str:
    return camel_to_snake_regex.sub('_', word).lower()


def find_z_value_entries(lines: List[str]) -> List[int]:
    """Find the strings which contains a z-value entry.
    """
    z_value_idxs = []
    for idx, line in enumerate(lines):
        if line.startswith('[ZValue ='):
            z_value_idxs.append(idx)
    return z_value_idxs


def find_title_entries(lines: List[str]) -> List[int]:
    """Find mdoc title entries in a list of strings"""
    title_idxs = []
    for idx, line in enumerate(lines):
        if line.startswith('[T ='):
            title_idxs.append(idx)
    return title_idxs