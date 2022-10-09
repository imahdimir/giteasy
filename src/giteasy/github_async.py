"""

    """

import asyncio
import base64
from functools import partial
from pathlib import Path

import aiohttp
import nest_asyncio
import pandas as pd
import ujson
from gidgethub.aiohttp import GitHubAPI

from .funcs import get_token
from .githubb import _get_all_fps_in_repo
from .githubb import ret_pygithub_repo_obj
from .githubb import ret_usr_repo_from_repo_url


nest_asyncio.apply()


def make_header(tok) :
    return {
            "Accept"        : "application/vnd.github.v3+json" ,
            "Authorization" : f"token {tok}" ,
            }


def make_data_json(cont , branch , sha , fn) :
    dta = {
            "content" : cont ,
            "branch"  : branch ,
            }
    if sha :
        dta["sha"] = sha
        dta["message"] = f"{fn} overwritted"
    else :
        dta["message"] = f"{fn} overwritted"
    return dta


async def ret_file_cont_as_base64_encoded_async(fp) :
    with open(fp , 'rb') as f :
        cnt = f.read()
    cnt = base64.b64encode(cnt)
    cnt = cnt.decode('utf-8')
    return cnt


async def add_overwrite_a_file_2_repo_async(fp ,
                                            fn ,
                                            sha ,
                                            usr_repo ,
                                            branch ,
                                            headers) :
    bs64_cnt = await ret_file_cont_as_base64_encoded_async(fp)
    dta = make_data_json(bs64_cnt , branch , sha , fn)
    async with aiohttp.ClientSession(json_serialize = ujson.dumps) as ses :
        url = f"https://api.github.com/repos/{usr_repo}/contents/{fn}"
        async with ses.put(url , headers = headers , json = dta) as r :
            print(await r.text())


async def add_overwrite_files_2_repo_async(fps , repo_url , branch) :
    tok = get_token()

    hdr = make_header(tok)

    ur = ret_usr_repo_from_repo_url(repo_url)

    df = find_sha_of_files(fps , ur , tok)

    fu = partial(add_overwrite_a_file_2_repo_async ,
                 usr_repo = ur ,
                 branch = branch ,
                 headers = hdr)

    co_tsks = []
    for _ , row in df.iterrows() :
        tsk = fu(fp = row['fp'] , fn = row['fn'] , sha = row['sha'])
        co_tsks.append(tsk)

    await asyncio.gather(*co_tsks)


def find_sha_of_files(fps , usr_repo , tok) :
    fps = [Path(fp) for fp in fps]

    data = {
            'fp' : list(fps)
            }
    df = pd.DataFrame(data)

    df['fn'] = df['fp'].apply(lambda x : x.name)

    rp = ret_pygithub_repo_obj(usr_repo , tok)
    ofs = _get_all_fps_in_repo(rp)

    _df = pd.DataFrame(ofs)
    _df['sha'] = _df[0].apply(lambda x : x.sha)
    _df['fn'] = _df[0].apply(lambda x : x.path)

    _df = _df.set_index('fn')
    df['sha'] = df['fn'].map(_df['sha'])
    return df


async def get_rare_limit(requester = 'imahdimir') :
    async with aiohttp.ClientSession() as session :
        gh = GitHubAPI(session , requester , oauth_token = get_token())
        data = await gh.getitem("/rate_limit")
        print(data)
