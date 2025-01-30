import shutil
import os

import pandas as pd

from mdocfile import read, write
from mdocfile.data_models import Mdoc


def test_read_tilt_series_mdoc(tilt_series_mdoc_file):
    df = read(tilt_series_mdoc_file)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (41, 26)
    assert 'TiltAngle' in df.columns

def test_read_tilt_series_mdoc_string(tilt_series_mdoc_string):
    df = Mdoc.from_string(tilt_series_mdoc_string).to_dataframe()
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


def test_write_tilt_series_mdoc(tilt_series_mdoc_file):
    tmp_path = "tests/test_data/tmpdir/"
    os.makedirs(tmp_path, exist_ok=True)

    df = read(tilt_series_mdoc_file)
    write(df, f"{tmp_path}/test.mdoc")
    df2 = read(f"{tmp_path}/test.mdoc")
    
    shutil.rmtree(tmp_path)
    assert df.equals(df2)


def test_write_tilt_series_mdoc_string(tilt_series_mdoc_string):
    tmp_path = "tests/test_data/tmpdir/"
    os.makedirs(tmp_path, exist_ok=True)

    df = Mdoc.from_string(tilt_series_mdoc_string).to_dataframe()
    write(df, f"{tmp_path}/test.mdoc")
    df2 = read(f"{tmp_path}/test.mdoc")

    shutil.rmtree(tmp_path)

    assert df.equals(df2)
