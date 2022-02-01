from pathlib import Path
from typing import Optional, Tuple, List

from pydantic import BaseModel, validator


class MdocGlobalData(BaseModel):
    """Data model for global data in a SerialEM mdoc file.

    https://bio3d.colorado.edu/SerialEM/hlp/html/about_formats.htm
    """
    DataMode: Optional[int]
    ImageSize: Optional[Tuple[int, int]]
    Montage: Optional[bool]
    ImageSeries: Optional[int]
    ImageFile: Optional[Path]
    PixelSpacing: Optional[float]

    @validator('ImageSize', pre=True)
    def multi_number_string_to_tuple(cls, value: str):
        return tuple(value.split())

    @classmethod
    def from_lines(cls, lines: List[str]):
        lines = [
            line for line in lines
            if len(line) > 0
        ]
        key_value_pairs = [
            line.split('=') for line in lines
            if not line.startswith('[T =')
        ]
        key_value_pairs = [
            (k.strip(), v.strip()) for k, v in key_value_pairs
        ]
        data = {k: v for k, v in key_value_pairs}
        return cls(**data)
