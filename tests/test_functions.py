import pandas as pd

from mdocfile import read, read_string


def test_read_tilt_series_mdoc(tilt_series_mdoc_file):
    df = read(tilt_series_mdoc_file)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (41, 26)
    assert 'TiltAngle' in df.columns

def test_read_tilt_series_mdoc_string(tilt_series_mdoc_string):
    df = read_string(tilt_series_mdoc_string)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (41, 26)
    assert 'TiltAngle' in df.columns

def test_read_montage_section_mdoc(montage_section_mdoc_file):
    df = read(montage_section_mdoc_file)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (63, 37)


def test_read_montage_section_multiple_mdoc(montage_section_multiple_mdoc_file):
    df = read(montage_section_multiple_mdoc_file)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (100, 36)


def test_read_frame_set_single_mdoc(frame_set_single_mdoc_file):
    df = read(frame_set_single_mdoc_file)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (1, 26)


def test_read_frame_set_multiple_mdoc(frame_set_multiple_mdoc_file):
    df = read(frame_set_multiple_mdoc_file)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (21, 28)
