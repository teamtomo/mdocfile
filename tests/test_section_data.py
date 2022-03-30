from pathlib import Path

from mdocfile.section_data import MdocSectionData

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
    assert data.SubFramePath == Path(r'D:\DATA\Flo\HGK149_20151130\frames\TS_01_000_0.0.mrc')
    assert data.NumSubFrames == 8
    assert data.DateTime == '30-Nov-15  15:21:38'
