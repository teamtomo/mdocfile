import pytest
from pathlib import Path

@pytest.fixture
def tilt_series_mdoc_file():
    return Path(__file__).parent / 'test_data' / 'TS_01.mrc.mdoc'