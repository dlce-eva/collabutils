import logging

import pytest

from collabutils.zotero import *


@pytest.fixture
def bibentry():
    return """@article{key,
keywords = {id:x:local},
note = {:bibtex:type: book:xetbib: :bibtex:field:author: The Author:xetbib: :bibtex:field:note: unpublished:xetbib:},
editor = {Editor, The},
title = {the title}
}"""


@pytest.fixture
def bib(tmp_path, bibentry):
    bibpath = tmp_path / 'test.bib'
    bibpath.write_text(bibentry, encoding='utf8')
    return bibpath


@pytest.fixture
def ZoteroAPI(mocker, bibentry):
    class API:
        def __init__(self, *args):
            pass
        def items(self, *args, **kw):
            if kw.get('limit') == 1:
                return []
            if kw.get('content') == 'bibtex':
                return [bibentry]
            return [
                {'data': {'tags': [{'tag': 'id:x'}, {'tag': 'id:y'}]}},
                {'data': {'tags': [{'tag': 'id:x'}]}},
            ]
        def delete_item(self, *args, **kw):
            pass
        def everything(self, q, *args, **kw):
            return q
        def item_template(self, *args, **kw):
            return {'tags': [], 'title': ''}
        def create_items(self, *args, **kw):
            return {'success': {'0': 1}}
    mocker.patch('collabutils.zotero.API', API)


def test_Zotero_upload_bib(bib, ZoteroAPI):
    z = Zotero(None, None)
    res = z.upload_bib('x', bib)
    assert res['key']


def test_Zotero_download_bib(ZoteroAPI):
    z = Zotero(None, None)
    bib = z.download_bib('x', remove=['keywords'])
    assert '@book{local,' in bib
    assert 'Author' in bib


def test_Zotero_delete_bib(ZoteroAPI, caplog):
    z = Zotero(None, None)
    z.delete_bib('x', log=logging.getLogger(__name__))
    assert caplog.records
