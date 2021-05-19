import shutil
import pathlib

import pytest

from collabutils.oc import *


@pytest.fixture
def OCClient(mocker):
    class File:
        name = 'f.xlsx'
        path = '/f.xlsx'
        def get_content_type(self):
            return 'text/plain'
    class Client:
        @classmethod
        def from_public_link(cls, *args):
            return cls()
        def list(self, *args):
            return [File()]
        def get_file(self, rp, lp):
            assert rp.startswith('/')
            shutil.copy(pathlib.Path(__file__).parent / 'test.xlsx', lp)
    mocker.patch('collabutils.oc.owncloud', mocker.Mock(Client=Client))


def test_Spreadsheet(OCClient, tmp_path):
    with pytest.raises(ValueError):
        _ = Spreadsheet('x.xlsx', None)
    s = Spreadsheet('f.xlsx', None)
    s.fetch_sheets(outdir=tmp_path)
    assert 'sheet_2.csv' in [p.name for p in tmp_path.glob('*.csv')]
