import pandas as pd
import pytest

from mdocfile.functions import read

@pytest.mark.parametrize(
    'camel_to_snake', [True, False]
)
def test_read(tilt_series_mdoc_file, camel_to_snake: bool):
    df = read(tilt_series_mdoc_file, camel_to_snake=camel_to_snake)
    print(camel_to_snake, len(df.columns))
    print(df.columns)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (41, 26)
    if camel_to_snake:
        assert 'tilt_angle' in df.columns
    else:
        assert 'TiltAngle' in df.columns

