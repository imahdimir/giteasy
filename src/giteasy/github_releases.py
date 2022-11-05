"""

    """

import re
from pathlib import Path
import tarfile

import requests
from mirutil.files import write_to_file
from mirutil.files import untar_to

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

def download_latest_release_tarball_of_a_public_github_repo(repo_url ,
                                                            local_path = None) :
    url = get_tar_url_of_latest_release_of_a_public_github_repo(repo_url)

    r = requests.get(url)
    if r.status_code != 200 :
        return

    fn = get_filename_fr_github_resp(r)
    if local_path is None :
        local_path = Path.cwd()
    fp = Path(local_path) / fn

    write_to_file(r.content , fp , 'wb')

    return fp

def get_dirname_fr_github_tarball(fp) :
    with tarfile.open(fp) as tar :
        return tar.getnames()[0]

def download_latest_release_of_public_github_repo(repo_url ,
                                                  local_path = None) :
    tar_fp = download_latest_release_tarball_of_a_public_github_repo(repo_url ,
                                                                     local_path)
    untar_to(tar_fp , tar_fp.parent)
    dirp = tar_fp.parent / get_dirname_fr_github_tarball(tar_fp)
    tar_fp.unlink()
    return dirp
