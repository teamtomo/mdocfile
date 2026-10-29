import logging
import math
from collections.abc import Sequence
from itertools import pairwise
from os import PathLike
from pathlib import Path, PureWindowsPath
from typing import Any

import pandas as pd
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, field_validator

from mdocfile.utils import find_section_entries, find_title_entries

log = logging.getLogger("mdocfile")


def _format_value(value: Any) -> str:
    """Consistent formatting of SerialEM mdoc values."""
    # NOTE: booleans written as 0/1
    if isinstance(value, bool):
        return str(int(value))

    # NOTE: NaN values written as 'NaN' (not 'nan' or 'None')
    if isinstance(value, float) and math.isnan(value):
        return "NaN"

    # NOTE: tuples/lists written as space-separated values
    if isinstance(value, tuple | list):
        return " ".join(_format_value(el) for el in value)

    return str(value)


class MdocGlobalData(BaseModel):
    """Data model for global data in a SerialEM mdoc file.

    https://bio3d.colorado.edu/SerialEM/hlp/html/about_formats.htm
    """

    model_config = ConfigDict(extra="allow")

    DataMode: int | None = None
    ImageSize: tuple[int, int] | None = None
    Montage: bool | None = None
    ImageSeries: int | None = None
    ImageFile: Path | None = None
    PixelSpacing: float | None = None
    Voltage: float | None = None
    Version: str | None = None

    @field_validator("ImageSize", mode="before")
    @classmethod
    def multi_number_string_to_tuple(cls, value: Any) -> Any:
        """Split a space-separated string into a tuple of strings."""
        if isinstance(value, str):
            value = tuple(value.split())
        return value

    @classmethod
    def from_lines(cls, lines: list[str]) -> "MdocGlobalData":
        """Create global data from the header lines of an mdoc file."""
        lines = [line for line in lines if len(line) > 0]
        key_value_pairs = [
            line.split("=") for line in lines if not line.startswith("[T =")
        ]
        data: dict[str, Any] = {k.strip(): v.strip() for k, v in key_value_pairs}
        return cls(**data)

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> "MdocGlobalData":
        """Create global data from the first row of an mdoc dataframe."""
        data = {}
        for k in cls.model_fields.keys():
            if k in df.columns:
                data[k] = df[k].iloc[0]
        return cls(**data)

    def to_string(self) -> str:
        """Generate the string representation of the global data."""
        lines = []
        for k, v in self.model_dump().items():
            if v is None:
                continue
            lines.append(f"{k} = {_format_value(v)}")
        return "\n".join(lines)


class MdocSectionData(BaseModel):
    """Data model for section data in a SerialEM mdoc file.

    https://bio3d.colorado.edu/SerialEM/hlp/html/about_formats.htm
    """

    model_config = ConfigDict(extra="allow", validate_by_name=True)
    _used_aliases: dict = PrivateAttr(default_factory=dict)  # field_name -> alias

    # headers
    ZValue: int | None = None
    MontSection: int | None = None
    FrameSet: int | None = None

    # section data
    TiltAngle: float | None = None
    PieceCoordinates: tuple[int, int, int] | None = None
    StagePosition: tuple[float, float] | None = None
    StageZ: float | None = None
    Magnification: int | None = None
    CameraLength: float | None = None
    MagIndex: int | None = None
    Intensity: float | None = None
    SuperMontCoords: tuple[float, float] | None = None
    PixelSpacing: float | None = None
    ExposureDose: float | None = None
    DoseRate: float | None = None
    SpotSize: int | None = None
    Defocus: float | None = None
    TargetDefocus: float | None = None
    ImageShift: tuple[float, float] | None = None
    RotationAngle: float | None = None
    ExposureTime: float | None = None
    Binning: float | None = None
    UsingCDS: bool | None = None
    CameraIndex: int | None = None
    DividedBy2: bool | None = None
    RotationAndFlip: int | None = None
    LowDoseConSet: int | None = None
    MinMaxMean: tuple[float, float, float] | None = None
    PriorRecordDose: float | None = None
    XedgeDxy: tuple[float, float] | tuple[float, float, float] | None = None
    YedgeDxy: tuple[float, float] | tuple[float, float, float] | None = None
    XedgeDxyVS: tuple[float, float] | tuple[float, float, float] | None = None
    YedgeDxyVS: tuple[float, float] | tuple[float, float, float] | None = None
    StageOffsets: tuple[float, float] | None = None
    AlignedPieceCoords: tuple[float, float] | tuple[float, float, float] | None = None
    AlignedPieceCoordsVS: tuple[float, float] | tuple[float, float, float] | None = None
    SubFramePath: PureWindowsPath | Path | None = None
    NumSubFrames: int | None = None
    FrameDosesAndNumbers: Sequence[tuple[float, int]] | None = Field(
        default=None, validation_alias="FrameDosesAndNumber"
    )
    DateTime: str | None = None
    NavigatorLabel: str | None = None
    FilterSlitAndLoss: tuple[float, float] | None = None
    ChannelName: str | None = None
    MultiShotHoleAndPosition: tuple[int, int] | tuple[int, int, int] | None = None
    CameraPixelSize: float | None = None
    Voltage: float | None = None

    @field_validator(
        "PieceCoordinates",
        "SuperMontCoords",
        "ImageShift",
        "MinMaxMean",
        "StagePosition",
        "XedgeDxy",
        "YedgeDxy",
        "XedgeDxyVS",
        "YedgeDxyVS",
        "StageOffsets",
        "AlignedPieceCoords",
        "AlignedPieceCoordsVS",
        "FilterSlitAndLoss",
        "MultiShotHoleAndPosition",
        mode="before",
    )
    @classmethod
    def multi_number_string_to_tuple(cls, value: Any) -> Any:
        """Split a space-separated string into a tuple of strings."""
        if isinstance(value, str):
            value = tuple(value.split())
        return value

    @field_validator("SubFramePath", mode="before")
    @classmethod
    def empty_path_to_none(cls, value: Any) -> Any:
        """Convert an empty 'SubFramePath =' to None, not the directory '.'."""
        if isinstance(value, str) and value.strip() == "":
            return None
        return value

    @field_validator("FrameDosesAndNumbers", mode="before")
    @classmethod
    def parse_frame_doses_and_numbers(cls, value: Any) -> Any:
        """Parse 'dose1 num1 dose2 num2 ...' into [(dose1, num1), ...]."""
        if isinstance(value, str):
            parts = value.split()
            return [
                (float(parts[i]), int(parts[i + 1]))
                for i in range(0, len(parts) - 1, 2)
            ]
        return value

    @classmethod
    def from_lines(cls, lines: list[str]) -> "MdocSectionData":
        """Create section data from the lines of one mdoc section."""
        data: dict[str, Any] = {}
        for line in lines:
            line = line.strip().strip("[]")
            if not line or "=" not in line:
                continue
            k, v = line.split("=", 1)
            data[k.strip()] = v.strip()

        # Rename aliased fields and track which were used
        used_aliases = {}
        for field_name, field_info in cls.model_fields.items():
            alias = field_info.validation_alias
            if isinstance(alias, str) and alias in data:
                data[field_name] = data.pop(alias)
                used_aliases[field_name] = alias
                log.warning(f"'{alias}' mapped to '{field_name}'")

        inst = cls(**data)
        inst._used_aliases = used_aliases
        return inst

    @classmethod
    def from_dataframe(cls, series: pd.Series) -> "MdocSectionData":
        """Create section data from one row of an mdoc dataframe."""
        skip = set(MdocGlobalData.model_fields.keys()) | {"titles"}
        data = {k: series[k] for k in series.index if k not in skip}
        return cls(**data)

    def to_string(self) -> str:
        """Generate the string representation of the section data."""
        data = self.model_dump()
        # A section is headed by whichever of ZValue, MontSection or FrameSet
        # it was read with, e.g. [MontSection = 0] or [FrameSet = 0].
        header_key = "ZValue"
        for key in ("ZValue", "MontSection", "FrameSet"):
            if data[key] is not None:
                header_key = key
                break
        header_value = data.pop(header_key)
        lines = [f"[{header_key} = {header_value}]"]
        for k, v in data.items():
            if v is None:
                continue

            # Use original fieldname if something was aliased
            output_key = self._used_aliases.get(k, k)

            if k == "FrameDosesAndNumbers" and isinstance(v, list):
                v = " ".join(f"{_format_value(d)} {n}" for d, n in v)
            lines.append(f"{output_key} = {_format_value(v)}")
        return "\n".join(lines)


class Mdoc(BaseModel):
    """Data model for a SerialEM mdoc file."""

    titles: list[str]
    global_data: MdocGlobalData
    section_data: list[MdocSectionData]

    @classmethod
    def from_file(cls, filename: str | PathLike) -> "Mdoc":
        """Create an Mdoc from an mdoc file."""
        with open(filename) as file:
            return cls.from_lines(file.readlines())

    @classmethod
    def from_string(cls, string: str) -> "Mdoc":
        """Create an Mdoc from the contents of an mdoc file."""
        lines = string.split("\n")

        return cls.from_lines(lines)

    @classmethod
    def from_lines(cls, file_lines: list[str]) -> "Mdoc":
        """Create an Mdoc from the lines of an mdoc file."""
        lines = [line.strip() for line in file_lines]
        split_idxs = find_section_entries(lines)
        split_idxs.append(len(lines))

        header_lines = lines[0 : split_idxs[0]]
        title_idxs = find_title_entries(header_lines)

        titles = [header_lines[idx] for idx in title_idxs]
        global_data = MdocGlobalData.from_lines(header_lines)
        section_data = [
            MdocSectionData.from_lines(lines[start_idx:end_idx])
            for start_idx, end_idx in pairwise(split_idxs)
        ]

        # Warn about extra fields
        extra_fields = set(global_data.model_extra or {})
        for s in section_data:
            extra_fields.update(s.model_extra or {})
        if extra_fields:
            log.warning(f"Unknown fields will be preserved: {extra_fields}")

        return cls(titles=titles, global_data=global_data, section_data=section_data)

    def to_dataframe(self) -> pd.DataFrame:
        """Convert an Mdoc object to a pandas DataFrame."""
        # Collect used aliases across all sections
        used_aliases = {}
        for section in self.section_data:
            used_aliases.update(section._used_aliases)

        df = pd.DataFrame(
            [
                {used_aliases.get(k, k): v for k, v in section.model_dump().items()}
                for section in self.section_data
            ]
        )

        # add duplicate copies of global data and mdoc file titles to each row of
        # the dataframe - tidy data is easier to analyse
        for k, v in self.global_data.model_dump().items():
            df[k] = [v] * len(df)
        df["titles"] = [self.titles] * len(df)
        df = df.dropna(axis="columns", how="all")
        return df

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame) -> "Mdoc":
        """Convert a suitable pandas dataframe to an Mdoc object.

        The dataframe can be generated by the Mdoc.to_dataframe() method.
        """
        global_data = MdocGlobalData.from_dataframe(df)
        section_data = [
            MdocSectionData.from_dataframe(row) for idx, row in df.iterrows()
        ]
        titles = df["titles"].iloc[0]
        return cls(titles=titles, global_data=global_data, section_data=section_data)

    def to_string(self) -> str:
        """Generate the string representation of the Mdoc data."""
        return "\n\n".join(
            [
                self.global_data.to_string(),
                "\n\n".join(self.titles),
                "\n\n".join(section.to_string() for section in self.section_data),
            ]
        )
