from mdocfile.mdoc import Mdoc


def test_mdoc_from_tilt_series_mdoc_file(tilt_series_mdoc_file):
    mdoc = Mdoc.from_file(tilt_series_mdoc_file)
    assert isinstance(mdoc, Mdoc)
    assert len(mdoc.titles) == 2
    assert mdoc.global_data.PixelSpacing == 5.4
    assert len(mdoc.section_data) == 41
