"""

    """

from pathlib import Path

from github import Github

from .repo import get_github_token_json_fp
from .repo import get_usr_tok_fr_json_file
from .repo import Repo


def ret_pygithub_github_obj(usr_repo_name) :
    """ Return a PyGitHub Github object. """
    rp = Repo(usr_repo_name)
    rpn = rp.user_repo

    fp = get_github_token_json_fp()
    if fp :
        _ , tok = get_usr_tok_fr_json_file(fp)
    else :
        tok = input('enter github access token:')

    g = Github(tok)
    repo = g.get_repo(rpn)

    return repo

def _get_all_fps_in_repo(pygithub_github_obj , sha = None , recursive = False) :
    """ Get all files sha & pathes in a GitHub repository. """
    rp = pygithub_github_obj
    if not sha :
        br = rp.default_branch
        sha = rp.get_branch(br).commit.sha
    return rp.get_git_tree(sha = sha , recursive = recursive).tree

def get_all_fps_in_repo(usr_repo_name , sha = None , recursive = False) :
    """ Get all files sha & pathes in a GitHub repository. """
    rp = ret_pygithub_github_obj(usr_repo_name)
    return _get_all_fps_in_repo(rp , sha , recursive)

def find_file_sha(usr_repo_name , fn) :
    """ Find the sha of a file in a GitHub repository. by its name. """
    rp = ret_pygithub_github_obj(usr_repo_name)
    return _find_file_sha(rp , fn)

def _find_file_sha(pygithub_github_obj , fn) :
    """ Find the sha of a file in a GitHub repository. """
    rp = pygithub_github_obj
    fns = _get_all_fps_in_repo(rp)
    for _fn in fns :
        if _fn.path == fn :
            return _fn.sha

def _add_overwrite_a_file_2_repo(fp ,
                                 pygithub_repo_obj ,
                                 msg = None ,
                                 branch = 'main') :
    """ Add a text based file to a GitHub repository. If the file already exists, it will be overwritten. """
    rp = pygithub_repo_obj
    fn = Path(fp).name

    with open(fp , 'rb') as fi :
        cnt = fi.read()

    sha = _find_file_sha(rp , fn)

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

def add_overwrite_a_file_2_repo(fp ,
                                usr_repo_name ,
                                msg = None ,
                                branch = 'main') :
    """ Add a text based file to a GitHub repository. If the file already exists, it will be overwritten. """
    repo = ret_pygithub_github_obj(usr_repo_name)
    fu = _add_overwrite_a_file_2_repo
    fu(fp , repo , msg , branch)

def _find_stems_fr_dir_not_in_repo(dirpath , file_suf , pygithub_github_obj) :
    fps = list(Path(dirpath).glob(f'*.{file_suf}'))
    print(f'{file_suf} files count in {dirpath}:  {len(fps)}')

    rp = pygithub_github_obj
    getf = _get_all_fps_in_repo
    ofps = getf(rp)
    print(f'all files count in {rp.full_name}:  {len(ofps)}')

    ofps = [Path(x.path) for x in ofps]
    ofps = [x.stem for x in ofps if x.suffix == f'.{file_suf}']
    print(f'{file_suf} files count in {rp.full_name}:  {len(ofps)}')

    stms = [x.stem for x in fps]
    nstms = set(stms) - set(ofps)
    print(f'new files count:  {len(nstms)}')

    return nstms

def find_stems_fr_dir_not_in_repo(dirpath , file_suf , usr_repo_name) :
    rp = ret_pygithub_github_obj(usr_repo_name)
    return _find_stems_fr_dir_not_in_repo(dirpath , file_suf , rp)

def add_overwrite_by_suf_fr_dir_2_repo(dirpath ,
                                       file_suf ,
                                       usr_repo_name ,
                                       overwrite = False) :
    fu = _add_overwrite_a_file_2_repo
    rp = ret_pygithub_github_obj(usr_repo_name)
    if overwrite :
        fps = list(Path(dirpath).glob(f'*.{file_suf}'))
        _ = [fu(x , rp) for x in fps]
    else :
        fu1 = find_stems_fr_dir_not_in_repo
        stms = fu1(dirpath , file_suf , usr_repo_name)
        fps = [Path(dirpath) / f'{x}.{file_suf}' for x in stms]
        _ = [fu(x , rp) for x in fps]
