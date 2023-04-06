import pytest
from pathlib import Path


@pytest.fixture
def tilt_series_mdoc_file():
    return Path(__file__).parent / 'test_data' / 'tilt_series.mdoc'


@pytest.fixture
def montage_section_mdoc_file():
    return Path(__file__).parent / 'test_data' / 'montage_section.mdoc'
