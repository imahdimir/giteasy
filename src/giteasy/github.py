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

def get_all_files_in_github_repo(github_repo) :
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

    return repo.get_git_tree(recursive = True).tree
