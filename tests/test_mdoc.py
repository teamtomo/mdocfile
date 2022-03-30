from mdocfile.mdoc import Mdoc
from tempfile import NamedTemporaryFile


def test_mdoc_from_tilt_series_mdoc_file(tilt_series_mdoc_file):
    mdoc = Mdoc.from_file(tilt_series_mdoc_file)
    assert isinstance(mdoc, Mdoc)
    assert len(mdoc.titles) == 2
    assert mdoc.global_data.PixelSpacing == 5.4
    assert len(mdoc.section_data) == 41


def test_to_string_is_valid_mdoc(tilt_series_mdoc_file):
    mdoc = Mdoc.from_file(tilt_series_mdoc_file)
    with NamedTemporaryFile() as tmp:
        tmp.write(mdoc.to_string().encode())
        mdoc2 = Mdoc.from_file(tmp.name)
    for (k1, v1), (k2, v2) in zip(mdoc.section_data[0].dict().items(), mdoc2.section_data[0].dict().items()):
        assert(v1 == v2), k1
