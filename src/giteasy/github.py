"""

    """

from pathlib import Path

from github import Github

from .repo import get_github_token_json_fp
from .repo import get_usr_tok_fr_json_file
from .repo import Repo


def add_txt_based_file_to_github_repo(file_path ,
                                      github_repo ,
                                      path_in_repo = None ,
                                      msg = None ,
                                      branch = 'main') :
    """ Add a text based file to a GitHub repository. If the file already exists, it will be overwritten. """
    rp = Repo(github_repo)
    rpn = rp.user_repo

    fp = get_github_token_json_fp()
    if fp :
        _ , tok = get_usr_tok_fr_json_file(fp)
    else :
        tok = input('enter github access token:')

    g = Github(tok)
    repo = g.get_repo(rpn)

    if path_in_repo is None :
        path_in_repo = Path(file_path).name
    if msg is None :
        msg = f'added {path_in_repo}'

    with open(file_path , 'r' , encoding = 'utf-8') as fi :
        cont = fi.read()
        repo.create_file(path_in_repo , msg , cont , branch = branch)

    print(f'file {path_in_repo} added to {rpn}')

def get_all_files_in_github_repo(github_repo , sha = None , recursive = True) :
    """ Get all files in a GitHub repository. """
    rp = Repo(github_repo)
    rpn = rp.user_repo

    fp = get_github_token_json_fp()
    if fp :
        _ , tok = get_usr_tok_fr_json_file(fp)
    else :
        tok = input('enter github access token:')

    g = Github(tok)
    repo = g.get_repo(rpn)

    if not sha :
        br = repo.default_branch
        sha = repo.get_branch(br).commit.sha

    return repo.get_git_tree(sha = sha , recursive = recursive).tree

def add_new_txt_based_files_fr_dir_to_github_repo(dir , file_suf , repo_name) :
    fps = list(Path(dir).glob('*'))
    fps = [fp for fp in fps if fp.suffix == file_suf]
    print(len(fps))

    getf = get_all_files_in_github_repo
    ofps = getf(repo_name)
    print(len(ofps))

    ofps = [Path(x.path) for x in ofps]
    ofps = [x.stem for x in ofps if x.suffix == file_suf]
    print(len(ofps))

    stms = [x.stem for x in fps]
    nstms = set(stms) - set(ofps)
    print(len(nstms))

    addf = add_txt_based_file_to_github_repo
    for st in nstms :
        fp = Path(dir) / f'{st}.html'
        addf(fp , repo_name)
