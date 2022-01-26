from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple, Union, Sequence, List

from pydantic import BaseModel, validator

from .utils import camel_to_snake


class MdocSectionData(BaseModel):
    """
    https://bio3d.colorado.edu/SerialEM/hlp/html/about_formats.htm
    """
    z_value: Optional[int]
    tilt_angle: Optional[float]
    piece_coordinates: Optional[Tuple[float, float, int]]
    stage_position: Tuple[float, float]
    stage_z: Optional[float]
    magnification: Optional[float]
    camera_length: Optional[float]
    mag_index: Optional[int]
    intensity: Optional[float]
    super_mont_coords: Optional[Tuple[float, float]]
    pixel_spacing: Optional[float]
    exposure_dose: Optional[float]
    dose_rate: Optional[float]
    spot_size: Optional[float]
    defocus: Optional[float]
    target_defocus: Optional[float]
    image_shift: Optional[Tuple[float, float]]
    rotation_angle: Optional[float]
    exposure_time: Optional[float]
    binning: Optional[int]
    using_cds: Optional[bool]
    camera_index: Optional[int]
    divided_by2: Optional[bool]
    low_dose_con_set: Optional[int]
    min_max_mean: Optional[Tuple[float, float, float]]
    prior_record_dose: Optional[float]
    x_edge_dxy: Optional[Tuple[float, float]]
    y_edge_dxy: Optional[Tuple[float, float]]
    x_edge_dxy_vs: Optional[Tuple[float, float]]
    y_edge_dxy_vs: Optional[Tuple[float, float]]
    stage_offsets: Optional[Tuple[float, float]]
    aligned_piece_coordinates: Optional[Tuple[float, float]]
    aligned_piece_coordinates_vs: Optional[Tuple[float, float]]
    sub_frame_path: Optional[Path]
    num_sub_frames: Optional[int]
    frame_doses_and_numbers: Optional[Sequence[Tuple[float, int]]]
    date_time: Optional[datetime]
    navigator_label: Optional[str]
    filter_slit_and_loss: Optional[Tuple[float, float]]
    channel_name: Optional[str]
    multi_shot_hole_and_position: Optional[Union[Tuple[int, int], Tuple[int, int, int]]]
    camera_pixel_size: Optional[float]
    voltage: Optional[float]

    @property
    def stage_position_x(self):
        return self.stage_position[0]

    @property
    def stage_position_y(self):
        return self.stage_position[1]

    @property
    def image_shift_x(self):
        return self.image_shift[0]

    @property
    def image_shift_y(self):
        return self.image_shift[1]

    @property
    def min(self):
        return self.min_max_mean[0]

    @property
    def max(self):
        return self.min_max_mean[1]

    @property
    def mean(self):
        return self.min_max_mean[2]

    @validator(
        'piece_coordinates',
        'super_mont_coords',
        'image_shift',
        'min_max_mean',
        'stage_position',
        'x_edge_dxy',
        'y_edge_dxy',
        'x_edge_dxy_vs',
        'y_edge_dxy_vs',
        'stage_offsets',
        'aligned_piece_coordinates',
        'aligned_piece_coordinates_vs',
        'frame_doses_and_numbers',
        'filter_slit_and_loss',
        'multi_shot_hole_and_position',
        pre=True)
    def multi_number_string_to_tuple(cls, value: str):
        return tuple(value.split())

    @validator('date_time', pre=True)
    def mdoc_datetime_to_datetime(cls, value: str):
        return datetime.strptime(value, '%d-%b-%y  %H:%M:%S', )

    @classmethod
    def from_lines(cls, lines: List[str]):
        lines = [line.strip('[]')
                 for line
                 in lines
                 if len(line) > 0]
        key_value_pairs = [line.split('=') for line in lines]
        key_value_pairs = [
            (camel_to_snake(k.strip()), v.strip())
            for k, v
            in key_value_pairs
        ]
        lines = {k: v for k, v in key_value_pairs}
        return cls(**lines)
