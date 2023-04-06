import pandas as pd

from mdocfile import read


def test_read_tilt_series_mdoc(tilt_series_mdoc_file):
    df = read(tilt_series_mdoc_file)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (41, 26)
    assert 'TiltAngle' in df.columns


def test_read_montage_section_mdoc(montage_section_mdoc_file):
    df = read(montage_section_mdoc_file)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (63, 37)
