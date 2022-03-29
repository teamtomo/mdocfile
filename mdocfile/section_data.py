from pathlib import Path
from typing import Optional, Tuple, Union, Sequence, List

from pydantic import BaseModel, validator


class MdocSectionData(BaseModel):
    """Data model for section data in a SerialEM mdoc file.

    https://bio3d.colorado.edu/SerialEM/hlp/html/about_formats.htm
    """
    ZValue: Optional[int]
    TiltAngle: Optional[float]
    PieceCoordinates: Optional[Tuple[float, float, int]]
    StagePosition: Tuple[float, float]
    StageZ: Optional[float]
    Magnification: Optional[float]
    CameraLength: Optional[float]
    MagIndex: Optional[int]
    Intensity: Optional[float]
    SuperMontCoords: Optional[Tuple[float, float]]
    PixelSpacing: Optional[float]
    ExposureDose: Optional[float]
    DoseRate: Optional[float]
    SpotSize: Optional[float]
    Defocus: Optional[float]
    TargetDefocus: Optional[float]
    ImageShift: Optional[Tuple[float, float]]
    RotationAngle: Optional[float]
    ExposureTime: Optional[float]
    Binning: Optional[float]
    UsingCDS: Optional[bool]
    CameraIndex: Optional[int]
    DividedBy2: Optional[bool]
    LowDoseConSet: Optional[int]
    MinMaxMean: Optional[Tuple[float, float, float]]
    PriorRecordDose: Optional[float]
    XedgeDxy: Optional[Tuple[float, float]]
    YedgeDxy: Optional[Tuple[float, float]]
    XedgeDxyVS: Optional[Tuple[float, float]]
    YedgeDxyVS: Optional[Tuple[float, float]]
    StageOffsets: Optional[Tuple[float, float]]
    AlignedPieceCoords: Optional[Tuple[float, float]]
    AlignedPieceCoordsVS: Optional[Tuple[float, float]]
    SubFramePath: Optional[Path]
    NumSubFrames: Optional[int]
    FrameDosesAndNumbers: Optional[Sequence[Tuple[float, int]]]
    DateTime: Optional[str]
    NavigatorLabel: Optional[str]
    FilterSlitAndLoss: Optional[Tuple[float, float]]
    ChannelName: Optional[str]
    MultiShotHoleAndPosition: Optional[Union[Tuple[int, int], Tuple[int, int, int]]]
    CameraPixelSize: Optional[float]
    Voltage: Optional[float]

    @validator(
        'PieceCoordinates',
        'SuperMontCoords',
        'ImageShift',
        'MinMaxMean',
        'StagePosition',
        'XedgeDxy',
        'YedgeDxy',
        'XedgeDxyVS',
        'XedgeDxyVS',
        'StageOffsets',
        'AlignedPieceCoords',
        'AlignedPieceCoordsVS',
        'FrameDosesAndNumbers',
        'FilterSlitAndLoss',
        'MultiShotHoleAndPosition',
        pre=True)
    def multi_number_string_to_tuple(cls, value: str):
        return tuple(value.split())

    @classmethod
    def from_lines(cls, lines: List[str]):
        lines = [line.strip('[]')
                 for line
                 in lines
                 if len(line) > 0]
        key_value_pairs = [line.split('=') for line in lines]
        key_value_pairs = [
            (k.strip(), v.strip())
            for k, v
            in key_value_pairs
        ]
        lines = {k: v for k, v in key_value_pairs}
        return cls(**lines)

    def to_string(self):
        data = self.dict()
        z_value = data.pop('ZValue')
        lines = [f'[ZValue = {z_value}]']
        for k, v in data.items():
            if v is None:
                continue
            elif isinstance(v, tuple):
                v = ' '.join(str(el) for el in v)
            elif v == 'nan':
                v = 'NaN'
            lines.append(f'{k} = {v}')
        return '\n'.join(lines)
