from typing import Optional, Tuple, List

from pydantic import BaseModel, validator

from .utils import camel_to_snake

from pathlib import Path


class MdocGlobalData(BaseModel):
    data_mode: Optional[int]
    image_size: Optional[Tuple[int, int]]
    montage: Optional[bool]
    pixel_spacing: Optional[float]
    image_file: Optional[Path]

    @validator('image_size', pre=True)
    def multi_number_string_to_tuple(cls, value: str):
        return tuple(value.split())

    @classmethod
    def from_lines(cls, lines: List[str]):
        lines = [
            line
            for line
            in lines
            if len(line) > 0
        ]
        key_value_pairs = [
            line.split('=')
            for line
            in lines
            if not line.startswith('[T =')
        ]
        key_value_pairs = [
            (camel_to_snake(k.strip()), v.strip())
            for k, v
            in key_value_pairs
        ]
        data = {k: v for k, v in key_value_pairs}
        return cls(**data)
