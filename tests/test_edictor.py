import pathlib

from collabutils.edictor import get_url, fetch


def test_get_url():
    u = get_url(path='x', v=['a', 'b'])
    assert '/x' in u
    assert '?' in u


def test_fetch(mocker, tmp_path):
    mocker.patch(
        'collabutils.edictor.urlretrieve',
        lambda u, p: pathlib.Path(p).write_text('test', encoding='utf8'))
    fetch('ds', outdir=tmp_path)
    assert tmp_path.joinpath('ds.sqlite').exists()
