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
    num_rows, num_cols = df.shape
    assert num_rows == 63
    assert num_cols >= 37  # extra fields preserved
    assert 'TiltAngle' in df.columns


def test_read_montage_section_multiple_mdoc(montage_section_multiple_mdoc_file):
    df = read(montage_section_multiple_mdoc_file)
    assert isinstance(df, pd.DataFrame)
    num_rows, num_cols = df.shape
    assert num_rows == 100
    assert num_cols >= 36  # extra fields preserved


def test_read_frame_set_single_mdoc(frame_set_single_mdoc_file):
    df = read(frame_set_single_mdoc_file)
    assert isinstance(df, pd.DataFrame)
    num_rows, num_cols = df.shape
    assert num_rows == 1
    assert num_cols >= 26  # extra fields preserved


def test_read_frame_set_multiple_mdoc(frame_set_multiple_mdoc_file):
    df = read(frame_set_multiple_mdoc_file)
    assert isinstance(df, pd.DataFrame)
    num_rows, num_cols = df.shape
    assert num_row == 21
    assert num_cols >= 28  # (extra fields preserved)


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
