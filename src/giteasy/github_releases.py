"""

    """

import requests

from .github_repo import GitHubRepo


def get_tar_url_of_latest_release_of_a_public_github_repo(repo_url) :
    ghr = GitHubRepo(repo_url)
    url = f'https://api.github.com/repos/{ghr.usr_repo}/releases/latest'
    r = requests.get(url)
    dct = r.json()

    return dct['tarball_url']
