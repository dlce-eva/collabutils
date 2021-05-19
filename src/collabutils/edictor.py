import pathlib
import urllib.parse
from urllib.request import urlretrieve


def get_url(
        base_url="https://lingulist.de/edictor",
        path=None,
        **params
):
    params = {
        k: '|'.join(v) if isinstance(v, (list, tuple)) else v
        for k, v in params.items() if v is not None}
    url_parts = list(urllib.parse.urlparse(base_url))
    if path:
        if not url_parts[2].endswith('/') and not path.startswith('/'):
            path = '/' + path
        url_parts[2] += path
    query = dict(urllib.parse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urllib.parse.urlencode(query)
    return urllib.parse.urlunparse(url_parts)


def fetch(
        dataset,
        remote_dbase=None,
        concepts=None,
        languages=None,
        columns=None,
        base_url="http://lingulist.de/edictor",
        outdir='.',
):
    remote_dbase = remote_dbase or (dataset + '.sqlite')
    url = get_url(
        base_url=base_url,
        path='/triples/get_data.py',
        file=dataset,
        concepts=concepts,
        doculects=languages,
        columns=columns,
        remote_dbase=remote_dbase,
    )
    return urlretrieve(url, str(pathlib.Path(outdir) / remote_dbase))
