"""

    """

import json
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

def get_usr_tok_fr_json_file(jsp) :
    with open(jsp , 'r') as fi :
        js = json.load(fi)
    return js['usr'] , js['tok']

def get_github_token_json_fp() :
    rsp = requests.get(cte.tr)
    js = rsp.json()
    for fp in js.values() :
        if Path(fp).exists() :
            return fp

def get_token() :
    fp = get_github_token_json_fp()
    if fp :
        _ , tok = get_usr_tok_fr_json_file(fp)
    else :
        tok = input('enter github access token:')
    return tok
