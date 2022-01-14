from pathlib import Path

from pydantic import BaseModel
from typing import Tuple
import datetime


class MdocImage(BaseModel):
    z_value: int
    tilt_angle: float
    stage_position: Tuple[float, float]
    stage_z: float
    magnification: float
    intensity: float
    exposure_dose: float
    pixel_spacing: float
    spot_size: float
    defocus: float
    image_shift: Tuple[float, float]
    rotation_angle: float
    exposure_time: float
    binning: int
    camera_index: int
    divided_by_2: bool
    mag_index: int
    min_max_mean: tuple[float, float, float]
    target_defocus: float
    subframe_path: Path
    num_subframes: int
    datetime: datetime.datetime

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
