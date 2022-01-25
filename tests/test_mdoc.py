from mdocfile.mdoc import MdocSectionData, MdocGlobalData, MdocData

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
Binning = 4
CameraIndex = 2
DividedBy2 = 1
MagIndex = 31
MinMaxMean = 5 1403 623.699
TargetDefocus = -4
SubFramePath = D:\DATA\Flo\HGK149_20151130\frames\TS_01_000_0.0.mrc
NumSubFrames = 8
DateTime = 30-Nov-15  15:21:38
"""


def test_instantiation():
    entry = MdocSectionData.from_filepart(SECTION_DATA_EXAMPLE)
    assert isinstance(entry, MdocSectionData)