"""

    """

from dataclasses import dataclass
from functools import partial
from multiprocessing import Pool
from pathlib import Path

from github import Github
from github.GithubException import GithubException
from mirutil.files import read_file as rf
from mirutil.tok import get_token as gt

from .github_repo import GitHubRepo


def ret_usr_repo_from_repo_url(repo_url) :
    """ Return the user/repo name from a GitHub repository URL. """
    rp = GitHubRepo(repo_url)
    return rp.usr_repo

def ret_pygithub_github_obj(tok = None , github_usr = None) :
    """ Return a PyGitHub GitHub object. """
    if tok is None :
        tok = gt(key = github_usr)
    g = Github(tok)
    return g

def ret_pygithub_repo_obj(usr_repo , tok = None , github_usr = None) :
    """ Return a PyGitHub repo object. """
    g = ret_pygithub_github_obj(tok , github_usr)
    return g.get_repo(usr_repo)

def _get_all_fps_in_repo(pygithub_repo_obj , sha = None , recursive = False) :
    """ Get all files sha & pathes in a GitHub repository. """
    rp = pygithub_repo_obj
    if not sha :
        br = rp.default_branch
        sha = rp.get_branch(br).commit.sha
    return rp.get_git_tree(sha = sha , recursive = recursive).tree

def get_all_fps_in_repo(repo_url , sha = None , recursive = False) :
    """ Get all files sha & pathes in a GitHub repository. """
    ur = ret_usr_repo_from_repo_url(repo_url)
    rp = ret_pygithub_repo_obj(ur)
    return _get_all_fps_in_repo(rp , sha , recursive)

def find_file_sha(repo_url , fn) :
    """ Find the sha of a file in a GitHub repository. by its name. """
    ur = ret_usr_repo_from_repo_url(repo_url)
    rp = ret_pygithub_repo_obj(ur)
    return _find_file_sha(rp , fn)

def _find_file_sha(pygithub_repo_obj , fn) :
    """ Find the sha of a file in a GitHub repository. """
    rp = pygithub_repo_obj
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

    cnt = rf(fp , mode = 'rb')

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

def add_overwrite_a_file_2_repo(fp , repo_url , msg = None , branch = 'main') :
    """ Add a text based file to a GitHub repository. If the file already exists, it will be overwritten. """
    ur = ret_usr_repo_from_repo_url(repo_url)
    rp = ret_pygithub_repo_obj(ur)
    fu = _add_overwrite_a_file_2_repo
    fu(fp , rp , msg , branch)

def _find_new_files_fr_dir_not_in_repo_by_suf(dirpath ,
                                              file_suf ,
                                              pygithub_repo_obj) :
    pth_ptrn = f'*{file_suf}'

    fps = list(Path(dirpath).glob(pth_ptrn))
    print(f'{file_suf} files count in {dirpath}:  {len(fps)}')

    rp = pygithub_repo_obj
    getf = _get_all_fps_in_repo
    ofns = getf(rp)
    print(f'all files count in {rp.full_name}:  {len(ofns)}')

    ofns = [Path(x.path) for x in ofns]
    ofns = [x.name for x in ofns if x.match(pth_ptrn)]
    print(f'{file_suf} files count in {rp.full_name}:  {len(ofns)}')

    fns = [x.name for x in fps]
    nfns = set(fns) - set(ofns)
    print(f'new files count:  {len(nfns)}')

    return nfns

def find_stems_fr_dir_not_in_repo(dirpath , file_suf , repo_url) :
    ur = ret_usr_repo_from_repo_url(repo_url)
    rp = ret_pygithub_repo_obj(ur)
    return _find_new_files_fr_dir_not_in_repo_by_suf(dirpath , file_suf , rp)

def add_overwrite_files_by_suf_fr_dir_2_repo(dirpath ,
                                             file_suf ,
                                             repo_url ,
                                             overwrite = False) :
    ur = ret_usr_repo_from_repo_url(repo_url)
    rp = ret_pygithub_repo_obj(ur)

    _dir = Path(dirpath)

    fu = _add_overwrite_a_file_2_repo

    if overwrite :
        fps = list(_dir.glob(f'*{file_suf}'))
        _ = [fu(x , rp) for x in fps]
    else :
        fu1 = _find_new_files_fr_dir_not_in_repo_by_suf
        fns = fu1(dirpath , file_suf , rp)
        fps = [_dir / x for x in fns]
        _ = [fu(x , rp) for x in fps]

@dataclass
class RRetFpsPyGithubRepoObj :
    fps: list
    pygithub_repo_obj: object

def ret_fps_and_pygithub_repo_obj(dirpath ,
                                  file_suf ,
                                  repo_url ,
                                  github_usr = None ,
                                  overwrite = False) :
    ur = ret_usr_repo_from_repo_url(repo_url)
    rp = ret_pygithub_repo_obj(ur , github_usr = github_usr)

    _dir = Path(dirpath)

    if overwrite :
        fps = list(_dir.glob(f'*{file_suf}'))
    else :
        fu1 = _find_new_files_fr_dir_not_in_repo_by_suf
        fns = fu1(dirpath , file_suf , rp)
        fps = [_dir / x for x in fns]

    ro = RRetFpsPyGithubRepoObj
    return ro(fps = fps , pygithub_repo_obj = rp)

def upload_files_by_suf_from_dir_2_repo_mp(dirpath ,
                                           file_suf ,
                                           repo_url ,
                                           github_usr = None ,
                                           overwrite = False ,
                                           n_jobs = 50) :
    fu = ret_fps_and_pygithub_repo_obj
    ou = fu(dirpath = dirpath ,
            file_suf = file_suf ,
            repo_url = repo_url ,
            github_usr = github_usr ,
            overwrite = overwrite)

    fps = ou.fps
    print(fps)

    rp = ou.pygithub_repo_obj
    print(rp)

    pool = Pool(n_jobs)

    fu = partial(_add_overwrite_a_file_2_repo , pygithub_repo_obj = rp)

    pool.map(fu , fps)

    return len(fps)

def persistently_upload_files_from_dir_2_repo_mp(dirpath ,
                                                 file_suf ,
                                                 repo_url ,
                                                 github_usr = None ,
                                                 overwrite = False ,
                                                 n_jobs = 50) :
    fu = upload_files_by_suf_from_dir_2_repo_mp
    while True :

        try :
            n = fu(dirpath = dirpath ,
                   file_suf = file_suf ,
                   repo_url = repo_url ,
                   github_usr = github_usr ,
                   overwrite = overwrite ,
                   n_jobs = n_jobs)
            if n == 0 :
                break

        except GithubException as e :
            print(e)
            pass

        except KeyboardInterrupt :
            break

def get_github_rate_limit(tok = None , github_usr = None) :
    """ Get the GitHub API rate limit. """
    gh = ret_pygithub_github_obj(tok = tok , github_usr = github_usr)
    return gh.get_rate_limit()

def ret_fps_with_suf_in_github_repo(repo_name , file_suffix) :
    """ returns a list of files havig file_suffix in the GitHub repo """
    fps = get_all_fps_in_repo(repo_name)
    fps = [Path(x.path) for x in fps]
    fps_wt_suf = [x for x in fps if x.suffix == file_suffix]
    return fps_wt_suf
