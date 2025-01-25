import re
from typing import List, Union

camel_to_snake_regex = re.compile(r'(?<!^)(?=[A-Z])')


def camel_to_snake(word: str) -> str:
    return camel_to_snake_regex.sub('_', word).lower()


def find_section_entries(lines: List[str]) -> List[int]:
    """Find the strings which contains a section entry header."""
    section_idx = [
        idx
        for idx, line
        in enumerate(lines)
        if (
            line.startswith('[ZValue =')
            or line.startswith('[MontSection =')
            or line.startswith('[FrameSet =')
        )
    ]

    return section_idx


def find_title_entries(lines: List[str]) -> List[int]:
    """Find mdoc title entries in a list of strings"""
    title_idxs = []
    for idx, line in enumerate(lines):
        if line.startswith('[T ='):
            title_idxs.append(idx)
    return title_idxs
