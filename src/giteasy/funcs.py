"""

    """

import json
from dataclasses import dataclass
from pathlib import Path

import requests

from .consts import Consts


cte = Consts()


def clean_github_url(github_repo_url) :
    inp = github_repo_url

    inp = inp.replace(cte.gi , '')

    spl = inp.split('/' , )
    spl = spl[:2]

    urp = '/'.join(spl)
    urp = urp.split('#')[0]

    url = cte.gi + urp
    return url


def github_url_wt_credentials(user , token , targ_repo) :
    return f'https://{user}:{token}@github.com/{targ_repo}'


def get_github_tok_fp() :
    tr = 'https://raw.github.com/imahdimir/tok/main/github.json'
    rsp = requests.get(tr)
    js = rsp.json()
    for fp in js.values() :
        if Path(fp).exists() :
            return fp


@dataclass
class RGet :
    usr: str
    tok: str


def get_github_usr_tok_fr_js_file(jsp , usr = None) :
    with open(jsp , 'r') as fi :
        js = json.load(fi)

    if usr :
        return RGet(usr = usr , tok = js[usr])

    return RGet(usr = list(js.keys())[0] , tok = list(js.values())[0])
