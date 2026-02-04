import logging
import pandas as pd
from pydantic import field_validator, BaseModel, ConfigDict, Field, PrivateAttr
from pathlib import Path, PureWindowsPath
from typing import List, Optional, Set, Tuple, Union, Sequence

from mdocfile.utils import find_section_entries, find_title_entries

log = logging.getLogger('mdocfile')


class MdocGlobalData(BaseModel):
    """Data model for global data in a SerialEM mdoc file.

    https://bio3d.colorado.edu/SerialEM/hlp/html/about_formats.htm
    """
    model_config = ConfigDict(extra='allow')

    DataMode: Optional[int] = None
    ImageSize: Optional[Tuple[int, int]] = None
    Montage: Optional[bool] = None
    ImageSeries: Optional[int] = None
    ImageFile: Optional[Path] = None
    PixelSpacing: Optional[float] = None
    Voltage: Optional[float] = None
    Version: Optional[str] = None

    @field_validator('ImageSize', mode="before")
    @classmethod
    def multi_number_string_to_tuple(cls, value: str):
        if isinstance(value, str):
            value = tuple(value.split())
        return value

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
    
    @classmethod
    def from_dataframe(cls, df: pd.DataFrame):
        data = {}
        for k in cls.model_fields.keys():
            if k in df.columns:
                data[k] = df[k].iloc[0]
        return cls(**data)

    def to_string(self):
        lines = []
        for k, v in self.model_dump().items():
            if v is None:
                continue
            if isinstance(v, tuple):
                v = ' '.join(str(el) for el in v)
            if v == 'nan':
                v = 'NaN'
            lines.append(f'{k} = {v}')
        return '\n'.join(lines)


class MdocSectionData(BaseModel):
    """Data model for section data in a SerialEM mdoc file.

    https://bio3d.colorado.edu/SerialEM/hlp/html/about_formats.htm
    """
    model_config = ConfigDict(extra='allow', validate_by_name=True)
    _used_aliases: dict = PrivateAttr(default_factory=dict)  # field_name -> alias

    # headers
    ZValue: Optional[int] = None
    MontSection: Optional[int] = None
    FrameSet: Optional[int] = None

    # section data
    TiltAngle: Optional[float] = None
    PieceCoordinates: Optional[Tuple[float, float, int]] = None
    StagePosition: Optional[Tuple[float, float]] = None
    StageZ: Optional[float] = None
    Magnification: Optional[float] = None
    CameraLength: Optional[float] = None
    MagIndex: Optional[int] = None
    Intensity: Optional[float] = None
    SuperMontCoords: Optional[Tuple[float, float]] = None
    PixelSpacing: Optional[float] = None
    ExposureDose: Optional[float] = None
    DoseRate: Optional[float] = None
    SpotSize: Optional[float] = None
    Defocus: Optional[float] = None
    TargetDefocus: Optional[float] = None
    ImageShift: Optional[Tuple[float, float]] = None
    RotationAngle: Optional[float] = None
    ExposureTime: Optional[float] = None
    Binning: Optional[float] = None
    UsingCDS: Optional[bool] = None
    CameraIndex: Optional[int] = None
    DividedBy2: Optional[bool] = None
    RotationAndFlip: Optional[int] = None
    LowDoseConSet: Optional[int] = None
    MinMaxMean: Optional[Tuple[float, float, float]] = None
    PriorRecordDose: Optional[float] = None
    XedgeDxy: Optional[Union[Tuple[float, float], Tuple[float, float, float]]] = None
    YedgeDxy: Optional[Union[Tuple[float, float], Tuple[float, float, float]]] = None
    XedgeDxyVS: Optional[Union[Tuple[float, float], Tuple[float, float, float]]] = None
    YedgeDxyVS: Optional[Union[Tuple[float, float], Tuple[float, float, float]]] = None
    StageOffsets: Optional[Tuple[float, float]] = None
    AlignedPieceCoords: Optional[Union[Tuple[float, float], Tuple[float, float, float]]] = None
    AlignedPieceCoordsVS: Optional[
        Union[Tuple[float, float], Tuple[float, float, float]]] = None
    SubFramePath: Optional[Union[PureWindowsPath, Path]] = None
    NumSubFrames: Optional[int] = None
    FrameDosesAndNumbers: Optional[Sequence[Tuple[float, int]]] = Field(
        default=None, validation_alias='FrameDosesAndNumber'
    )
    DateTime: Optional[str] = None
    NavigatorLabel: Optional[str] = None
    FilterSlitAndLoss: Optional[Tuple[float, float]] = None
    ChannelName: Optional[str] = None
    MultiShotHoleAndPosition: Optional[Union[Tuple[int, int], Tuple[int, int, int]]] = None
    CameraPixelSize: Optional[float] = None
    Voltage: Optional[float] = None

    @field_validator(
        'PieceCoordinates',
        'SuperMontCoords',
        'ImageShift',
        'MinMaxMean',
        'StagePosition',
        'XedgeDxy',
        'YedgeDxy',
        'XedgeDxyVS',
        'YedgeDxyVS',
        'StageOffsets',
        'AlignedPieceCoords',
        'AlignedPieceCoordsVS',
        'FilterSlitAndLoss',
        'MultiShotHoleAndPosition',
        mode="before")
    @classmethod
    def multi_number_string_to_tuple(cls, value: str):
        if isinstance(value, str):
            value = tuple(value.split())
        return value

    @field_validator('FrameDosesAndNumbers', mode="before")
    @classmethod
    def parse_frame_doses_and_numbers(cls, value: str):
        """Parse 'dose1 num1 dose2 num2 ...' into [(dose1, num1), ...]"""
        if isinstance(value, str):
            parts = value.split()
            return [(float(parts[i]), int(parts[i+1])) for i in range(0, len(parts)-1, 2)]
        return value

    @classmethod
    def from_lines(cls, lines: List[str]):
        data = {}
        for line in lines:
            line = line.strip().strip('[]')
            if not line or '=' not in line:
                continue
            k, v = line.split('=', 1)
            data[k.strip()] = v.strip()

        # Rename aliased fields and track which were used
        used_aliases = {}
        for field_name, field_info in cls.model_fields.items():
            alias = field_info.validation_alias
            if alias and alias in data:
                data[field_name] = data.pop(alias)
                used_aliases[field_name] = alias
                log.warning(f"'{alias}' mapped to '{field_name}'")

        inst = cls(**data)
        inst._used_aliases = used_aliases
        return inst
    
    @classmethod
    def from_dataframe(cls, series: pd.Series):
        skip = set(MdocGlobalData.model_fields.keys()) | {'titles'}
        data = {k: series[k] for k in series.index if k not in skip}
        return cls(**data)

    def to_string(self):
        data = self.model_dump()
        z_value = data.pop('ZValue')
        lines = [f'[ZValue = {z_value}]']
        for k, v in data.items():
            if v is None:
                continue

            # Use original fieldname if something was aliased
            output_key = self._used_aliases.get(k, k)

            if k == 'FrameDosesAndNumbers' and isinstance(v, list):
                v = ' '.join(f'{d} {n}' for d, n in v)
            elif isinstance(v, tuple):
                v = ' '.join(str(el) for el in v)
            elif v == 'nan':
                v = 'NaN'
            lines.append(f'{output_key} = {v}')
        return '\n'.join(lines)


class Mdoc(BaseModel):
    titles: List[str]
    global_data: MdocGlobalData
    section_data: List[MdocSectionData]

    @classmethod
    def from_file(cls, filename: str):
        with open(filename) as file:
            return cls.from_lines(file.readlines())
    
    @classmethod
    def from_string(cls, string: str):
        lines = string.split('\n')

        return cls.from_lines(lines)
    
    @classmethod
    def from_lines(cls, file_lines: List[str]) -> 'Mdoc':
        lines = [line.strip() for line in file_lines]
        split_idxs = find_section_entries(lines)
        split_idxs.append(len(lines))

        header_lines = lines[0:split_idxs[0]]
        title_idxs = find_title_entries(header_lines)

        titles = [header_lines[idx] for idx in title_idxs]
        global_data = MdocGlobalData.from_lines(header_lines)
        section_data = [
            MdocSectionData.from_lines(lines[start_idx:end_idx])
            for start_idx, end_idx
            in zip(split_idxs, split_idxs[1:])
        ]

        # Warn about extra fields
        extra_fields = set(global_data.model_extra.keys())
        for s in section_data:
            extra_fields.update(s.model_extra.keys())
        if extra_fields:
            log.warning(f"Unknown fields will be preserved: {extra_fields}")

        return cls(titles=titles, global_data=global_data, section_data=section_data)
    
    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert an Mdoc object to a pandas DataFrame
        """
        # Collect used aliases across all sections
        used_aliases = {}
        for section in self.section_data:
            used_aliases.update(section._used_aliases)

        df = pd.DataFrame([
            {used_aliases.get(k, k): v for k, v in section.model_dump().items()}
            for section in self.section_data
        ])

        # add duplicate copies of global data and mdoc file titles to each row of
        # the dataframe - tidy data is easier to analyse
        for k, v in self.global_data.model_dump().items():
            df[k] = [v] * len(df)
        df['titles'] = [self.titles] * len(df)
        df = df.dropna(axis='columns', how='all')
        return df
    
    @classmethod
    def from_dataframe(cls, df: pd.DataFrame):
        """
        Convert a suitable pandas dataframe, e.g. as generated by the Mdoc.to_dataframe() method, to an Mdoc object
        """
        global_data = MdocGlobalData.from_dataframe(df)
        section_data = [MdocSectionData.from_dataframe(row) for idx, row in df.iterrows()]
        titles = df['titles'].iloc[0]
        return cls(titles=titles, global_data=global_data, section_data=section_data)

    def to_string(self):
        """
        Generate the string representation of the Mdoc data
        """
        return '\n\n'.join([
            self.global_data.to_string(),
            '\n\n'.join(self.titles),
            '\n\n'.join(section.to_string() for section in self.section_data),
        ])
