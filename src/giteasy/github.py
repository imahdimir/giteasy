"""

    """

import asyncio
import nest_asyncio
from pathlib import Path

from github import Github
from functools import partial

from .repo import get_github_token_json_fp
from .repo import get_usr_tok_fr_json_file
from .repo import Repo


nest_asyncio.apply()

def ret_pygithub_github_obj(github_user_repo_name) :
    """ Return a PyGitHub Github object. """
    rp = Repo(github_user_repo_name)
    rpn = rp.user_repo

    fp = get_github_token_json_fp()
    if fp :
        _ , tok = get_usr_tok_fr_json_file(fp)
    else :
        tok = input('enter github access token:')

    g = Github(tok)
    repo = g.get_repo(rpn)

    return repo

def _get_all_fps_in_github_repo(pygithub_github_obj ,
                                sha = None ,
                                recursive = False) :
    """ Get all files sha & pathes in a GitHub repository. """
    rp = pygithub_github_obj
    if not sha :
        br = rp.default_branch
        sha = rp.get_branch(br).commit.sha
    return rp.get_git_tree(sha = sha , recursive = recursive).tree

def get_all_fps_in_github_repo(github_user_repo_name ,
                               sha = None ,
                               recursive = False) :
    """ Get all files sha & pathes in a GitHub repository. """
    rp = ret_pygithub_github_obj(github_user_repo_name)
    return _get_all_fps_in_github_repo(rp , sha , recursive)

def find_sha_of_a_file_in_github_repo(github_repo , fn) :
    """ Find the sha of a file in a GitHub repository. """
    rp = ret_pygithub_github_obj(github_repo)
    return _find_sha_of_a_file_in_github_repo(rp , fn)

def _find_sha_of_a_file_in_github_repo(pygithub_github_obj , fn) :
    """ Find the sha of a file in a GitHub repository. """
    rp = pygithub_github_obj
    fns = _get_all_fps_in_github_repo(rp)
    for _fn in fns :
        if _fn.path == fn :
            return _fn.sha

def _add_xor_overwrite_a_txt_based_file_2_github_repo(fp ,
                                                      pygithub_repo_obj ,
                                                      msg = None ,
                                                      branch = 'main') :
    """ Add a text based file to a GitHub repository. If the file already exists, it will be overwritten. """
    rp = pygithub_repo_obj
    fn = Path(fp).name

    with open(fp , 'r' , encoding = 'utf-8') as fi :
        cnt = fi.read()

    sha = _find_sha_of_a_file_in_github_repo(rp , fn)

    if sha :
        _ms = f'{fn} overwritted'
        if not msg :
            msg = _ms

        rp.update_file(path = fn ,
                       message = msg ,
                       content = cnt ,
                       sha = sha ,
                       branch = branch)

        print(_ms , f' in  {rp.full_name}')

    else :
        _ms = f'{fn} added'
        if not msg :
            msg = _ms

        rp.create_file(path = fn ,
                       message = msg ,
                       content = cnt ,
                       branch = branch)

        print(_ms , f' 2  {rp.full_name}')

def add_xor_overwrite_a_txt_based_file_2_github_repo(fp ,
                                                     github_user_repo_name ,
                                                     msg = None ,
                                                     branch = 'main') :
    """ Add a text based file to a GitHub repository. If the file already exists, it will be overwritten. """
    repo = ret_pygithub_github_obj(github_user_repo_name)
    fu = _add_xor_overwrite_a_txt_based_file_2_github_repo
    fu(fp , repo , msg , branch)

async def _add_xor_overwrite_a_txt_based_file_2_github_repo_async(fp ,
                                                                  pygithub_github_obj ,
                                                                  branch = 'main') :
    fu = _add_xor_overwrite_a_txt_based_file_2_github_repo
    fu(fp , pygithub_github_obj , None , branch)

async def add_xor_overwrite_txt_based_files_2_github_repo_async(fps ,
                                                                github_user_repo_name ,
                                                                branch = 'main') :
    """ Add text based files to a GitHub repository. If the files already exist, they will be overwritten. """
    rp = ret_pygithub_github_obj(github_user_repo_name)
    fu = partial(_add_xor_overwrite_a_txt_based_file_2_github_repo_async ,
                 pygithub_github_obj = rp ,
                 branch = branch)
    co_tsks = [fu(x) for x in fps]
    await asyncio.gather(*co_tsks)

def _find_stems_fr_dir_not_in_repo(dir_ , file_suf , pygithub_github_obj) :
    fps = list(Path(dir_).glob(f'*.{file_suf}'))
    print(f'{file_suf} files count in {dir_}:  {len(fps)}')

    rp = pygithub_github_obj
    getf = _get_all_fps_in_github_repo
    ofps = getf(rp)
    print(f'all files count in {rp.full_name}:  {len(ofps)}')

    ofps = [Path(x.path) for x in ofps]
    ofps = [x.stem for x in ofps if x.suffix == f'.{file_suf}']
    print(f'{file_suf} files count in {rp.full_name}:  {len(ofps)}')

    stms = [x.stem for x in fps]
    nstms = set(stms) - set(ofps)
    print(f'new files count:  {len(nstms)}')

    return nstms

def find_stems_fr_dir_not_in_repo(dir_ , file_suf , github_user_repo_name) :
    rp = ret_pygithub_github_obj(github_user_repo_name)
    return _find_stems_fr_dir_not_in_repo(dir_ , file_suf , rp)

async def add_txt_based_files_fr_dir_to_github_repo_async(dir_ ,
                                                          file_suf ,
                                                          github_user_repo_name ,
                                                          overwrite = False) :
    fu = add_xor_overwrite_txt_based_files_2_github_repo_async
    if overwrite :
        fps = list(Path(dir_).glob(f'*.{file_suf}'))
        await fu(fps , github_user_repo_name)
    else :
        fu1 = find_stems_fr_dir_not_in_repo
        stms = fu1(dir_ , file_suf , github_user_repo_name)
        fps = [Path(dir_) / (f'{x}.{file_suf}') for x in stms]
        await fu(fps , github_user_repo_name)
