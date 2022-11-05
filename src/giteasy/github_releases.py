"""

    """

import re

import requests

from .github_repo import GitHubRepo


def get_tar_url_of_latest_release_of_a_public_github_repo(repo_url) :
    ghr = GitHubRepo(repo_url)
    url = f'https://api.github.com/repos/{ghr.usr_repo}/releases/latest'
    r = requests.get(url)
    dct = r.json()
    return dct['tarball_url']

def get_filename_fr_github_resp(r) :
    hdr = r.headers
    cd = hdr['content-disposition']
    pat = 'attachment; filename=(.+)'
    mat = re.findall(pat , cd)
    return mat[0]
