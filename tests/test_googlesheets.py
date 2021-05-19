from csvw.dsv import reader

from collabutils.googlesheets import *


def test_Spreadsheet(mocker, tmp_path):
    class Sheet:
        title = 'the title'
        def get_all_values(self):
            return [['col1', 'col2'], ['val1', 'val2']]

    class Workbook:
        def worksheets(self):
            return [Sheet()]

    class Service:
        def open_by_url(self, *args):
            return Workbook()
        def open_by_key(self, *args):
            return Workbook()

    mocker.patch(
        'collabutils.googlesheets.gspread', mocker.Mock(service_account=lambda **kw: Service()))
    d = Spreadsheet('key', auth=tmp_path)
    assert 'the title' in d.sheets
    d = Spreadsheet('http://example.org/key', auth=tmp_path)
    d.fetch_sheets({'the title': 'test.tsv'}, outdir=tmp_path, delimiter='\t')
    rows = list(reader(tmp_path / 'test.tsv', delimiter='\t', dicts=True))
    assert rows[0]['col2'] == 'val2'
