from pathlib import Path, PureWindowsPath
from tempfile import NamedTemporaryFile

from mdocfile.data_models import MdocGlobalData, MdocSectionData, Mdoc

GLOBAL_DATA_EXAMPLE = r"""PixelSpacing = 5.4
ImageFile = TS_01.mrc
ImageSize = 924 958
DataMode = 1
"""


def test_global_data_from_lines():
    lines = GLOBAL_DATA_EXAMPLE.split('\n')
    data = MdocGlobalData.from_lines(lines)
    assert isinstance(data, MdocGlobalData)
    assert data.PixelSpacing == 5.4
    assert data.ImageFile == Path('TS_01.mrc')
    assert data.DataMode == 1


SECTION_DATA_EXAMPLE = r"""[ZValue = 0]
TiltAngle = 0.000999877
StagePosition = 20.7936 155.287
StageZ = 163.803
Magnification = 105000
Intensity = 0.00900259
ExposureDose = 0
PixelSpacing = 5.4
SpotSize = 8
Defocus = 2.68083
ImageShift = -0.0108126 -0.121079
RotationAngle = 175.3
ExposureTime = 0.8
Binning = 0.5
CameraIndex = 2
DividedBy2 = 1
MagIndex = 31
MinMaxMean = 5 1403 623.699
TargetDefocus = -4
SubFramePath = D:\DATA\Flo\HGK149_20151130\frames\TS_01_000_0.0.mrc
NumSubFrames = 8
DateTime = 30-Nov-15  15:21:38
"""


def test_section_data_from_lines():
    lines = SECTION_DATA_EXAMPLE.split('\n')
    data = MdocSectionData.from_lines(lines)
    assert isinstance(data, MdocSectionData)
    assert data.TiltAngle == 0.000999877
    assert data.StagePosition == (20.7936, 155.287)
    assert data.StageZ == 163.803
    assert data.Magnification == 105000
    assert data.Intensity == 0.009002590
    assert data.ExposureDose == 0
    assert data.PixelSpacing == 5.4
    assert data.SpotSize == 8
    assert data.Defocus == 2.68083
    assert data.ImageShift == (-0.0108126, -0.121079)
    assert data.RotationAngle == 175.3
    assert data.ExposureTime == 0.8
    assert data.Binning == 0.5
    assert data.CameraIndex == 2
    assert data.DividedBy2 is True
    assert data.MagIndex == 31
    assert data.MinMaxMean == (5, 1403, 623.699)
    assert data.TargetDefocus == -4
    assert data.SubFramePath == PureWindowsPath(r'D:\DATA\Flo\HGK149_20151130\frames\TS_01_000_0.0.mrc')
    assert data.NumSubFrames == 8
    assert data.DateTime == '30-Nov-15  15:21:38'


def test_mdoc_from_tilt_series_mdoc_file(tilt_series_mdoc_file):
    mdoc = Mdoc.from_file(tilt_series_mdoc_file)
    assert isinstance(mdoc, Mdoc)
    assert len(mdoc.titles) == 2
    assert mdoc.global_data.PixelSpacing == 5.4
    assert len(mdoc.section_data) == 41


def test_to_string_is_valid_mdoc(tilt_series_mdoc_file):
    mdoc = Mdoc.from_file(tilt_series_mdoc_file)
    with NamedTemporaryFile() as tmp:
        tmp.write(mdoc.to_string().encode())
        tmp.flush()
        mdoc2 = Mdoc.from_file(tmp.name)
    mdoc_dict = mdoc.section_data[0].model_dump()
    mdoc2_dict = mdoc2.section_data[0].model_dump()
    for (k1, v1), (k2, v2) in zip(mdoc_dict.items(), mdoc2_dict.items()):
        assert v1 == v2
        assert k1 == k2

def test_section_data_from_path():
    some_path = Path('bla.tif')
    section = MdocSectionData(SubFramePath=some_path)
    assert section.SubFramePath == some_path
    assert f'SubFramePath = {some_path}' in section.to_string()

def test_fieldname_alias_mapping():
    """Test that aliased field names are mapped to canonical names."""
    lines = """[ZValue = 0]
TiltAngle = 5.0
FrameDosesAndNumber = 2.5 10 3.0 20
""".split('\n')

    section = MdocSectionData.from_lines(lines)

    # Should be accessible via canonical name
    assert section.FrameDosesAndNumbers is not None
    assert section.FrameDosesAndNumbers == [(2.5, 10), (3.0, 20)]

    # to_string should output the alias FrameDosesAndNumber due to serialize_by_alias
    assert 'FrameDosesAndNumber = 2.5 10 3.0 20' in section.to_string()

    # Keeps orig
    section = MdocSectionData.from_lines("""[ZValue = 0]
TiltAngle = 5.0
FrameDosesAndNumbers = 2.5 10 3.0 20
""".split('\n'))
    # to_string should output the alias FrameDosesAndNumber due to serialize_by_alias
    assert 'FrameDosesAndNumbers = 2.5 10 3.0 20' in section.to_string()


def test_extra_fields_round_trip():
    """Test that unknown fields are preserved through full Mdoc round-trip."""
    mdoc_str = """DataMode = 1
ImageFile = test.mrc

[ZValue = 0]
TiltAngle = 5.0
CountsPerElectron = 42.0
UnknownCustomField = some_value
"""

    mdoc = Mdoc.from_string(mdoc_str)

    # Extra fields stored in model_extra
    assert mdoc.section_data[0].model_extra['CountsPerElectron'] == '42.0'
    assert mdoc.section_data[0].model_extra['UnknownCustomField'] == 'some_value'

    # Round-trip preserves extra fields
    mdoc2 = Mdoc.from_string(mdoc.to_string())
    assert mdoc2.section_data[0].model_extra['CountsPerElectron'] == '42.0'
    assert mdoc2.section_data[0].model_extra['UnknownCustomField'] == 'some_value'


def test_dataframe_alias_mapping():
    """Test that aliased field names work through dataframe round-trip."""
    mdoc_str = """DataMode = 1
ImageFile = test.mrc

[ZValue = 0]
TiltAngle = 5.0
FrameDosesAndNumber = 2.5 10 3.0 20
"""

    mdoc = Mdoc.from_string(mdoc_str)
    df = mdoc.to_dataframe()

    # Dataframe should have the alias it came as
    assert 'FrameDosesAndNumber' in df.columns

    # Round-trip through dataframe
    assert Mdoc.from_dataframe(df).section_data[0].FrameDosesAndNumbers == [(2.5, 10), (3.0, 20)]


def test_dataframe_extra_fields_round_trip():
    """Test that extra fields survive dataframe round-trip."""
    mdoc_str = """DataMode = 1
ImageFile = test.mrc

[ZValue = 0]
TiltAngle = 5.0
CountsPerElectron = 42.0
UnknownCustomField = some_value
"""

    mdoc = Mdoc.from_string(mdoc_str)
    df = mdoc.to_dataframe()

    # Extra fields should be columns in dataframe
    assert 'CountsPerElectron' in df.columns
    assert 'UnknownCustomField' in df.columns
    assert df['CountsPerElectron'].iloc[0] == '42.0'
    assert df['UnknownCustomField'].iloc[0] == 'some_value'

    # Round-trip through dataframe preserves extra fields
    mdoc2 = Mdoc.from_dataframe(df)
    assert mdoc2.section_data[0].model_extra['CountsPerElectron'] == '42.0'
    assert mdoc2.section_data[0].model_extra['UnknownCustomField'] == 'some_value'