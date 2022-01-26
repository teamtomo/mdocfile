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


def test_section_data_from_lines():
    lines = SECTION_DATA_EXAMPLE.split('\n')
    data = MdocSectionData.from_lines(lines)
    assert isinstance(data, MdocSectionData)
    assert data.tilt_angle == 0.000999877
    assert data.stage_position == (20.7936, 155.287)
    assert data.stage_z == 163.803
    assert data.magnification == 105000
    assert data.intensity == 0.009002590
    assert data.exposure_dose == 0
    assert data.pixel_spacing == 5.4
    assert data.spot_size == 8
    assert data.defocus == 2.68083
    assert data.image_shift == (-0.0108126, -0.121079)
    assert data.rotation_angle == 175.3
    assert data.exposure_time == 0.8
    assert data.binning == 4
    assert data.camera_index == 2
    assert data.divided_by2 is True
    assert data.mag_index == 31
    assert data.min_max_mean == (5, 1403, 623.699)
    assert data.target_defocus == -4
    assert data.sub_frame_path == Path(r'D:\DATA\Flo\HGK149_20151130\frames\TS_01_000_0.0.mrc')
    assert data.num_sub_frames == 8
    assert data.date_time == MdocSectionData.mdoc_datetime_to_datetime('30-Nov-15  15:21:38')




