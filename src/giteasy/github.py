"""

    """

from pathlib import Path

from github import Github

from .funcs import get_token
from .repo import Repo


def ret_usr_repo_from_repo_url(repo_url) :
    """ Return the user/repo name from a GitHub repository URL. """
    rp = Repo(repo_url)
    return rp.user_repo


def ret_pygithub_repo_obj(usr_repo , tok = None) :
    """ Return a PyGitHub repo object. """
    if not tok :
        tok = get_token()
    g = Github(tok)
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

    with open(fp , 'rb') as f :
        cnt = f.read()

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
    fps = list(Path(dirpath).glob(f'*.{file_suf}'))
    print(f'{file_suf} files count in {dirpath}:  {len(fps)}')

    rp = pygithub_repo_obj
    getf = _get_all_fps_in_repo
    ofns = getf(rp)
    print(f'all files count in {rp.full_name}:  {len(ofns)}')

    ofns = [Path(x.path) for x in ofns]
    ofns = [x.name for x in ofns if x.suffix == f'.{file_suf}']
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
        fps = list(_dir.glob(f'*.{file_suf}'))
        _ = [fu(x , rp) for x in fps]
    else :
        fu1 = _find_new_files_fr_dir_not_in_repo_by_suf
        fns = fu1(dirpath , file_suf , rp)
        fps = [_dir / x for x in fns]
        _ = [fu(x , rp) for x in fps]


def ret_fps_pygithub_repo_inst_for_multiprocess(dirpath ,
                                                file_suf ,
                                                repo_url ,
                                                overwrite = False) :
    ur = ret_usr_repo_from_repo_url(repo_url)
    rp = ret_pygithub_repo_obj(ur)

    _dir = Path(dirpath)

    if overwrite :
        fps = list(_dir.glob(f'*.{file_suf}'))
    else :
        fu1 = _find_new_files_fr_dir_not_in_repo_by_suf
        fns = fu1(dirpath , file_suf , rp)
        fps = [_dir / x for x in fns]

    return {
            'fps'           : fps ,
            'pygithub.repo' : rp
            }
