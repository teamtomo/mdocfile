from mdocfile.global_data import MdocGlobalData
from pathlib import Path

GLOBAL_DATA_EXAMPLE = r"""PixelSpacing = 5.4
ImageFile = TS_01.mrc
ImageSize = 924 958
DataMode = 1
"""


def test_global_data_from_filepart():
    data = MdocGlobalData.from_filepart(GLOBAL_DATA_EXAMPLE)
    assert isinstance(data, MdocGlobalData)
    assert data.pixel_spacing == 5.4
    assert data.image_file == Path('TS_01.mrc')
    assert data.data_mode == 1
