"""

    """

import shutil
from pathlib import Path

from dulwich import index
from dulwich import porcelain
from dulwich.client import HTTPUnauthorized
from dulwich.repo import Repo as DulwichRepo
from mtok import get_token as gettoken
from purl import URL

gbu = 'https://github.com/'

class GitHubRepo :

    def __init__(self ,
                 repo_url: str ,
                 local_path = None ,
                 containing_dir = Path('GitHubData/') ,
                 committing_usr: (str , None) = None ,
                 token: (str , None) = None
                 ) :

        self.local_path = local_path
        self.containing_dir = containing_dir
        self.committing_usr = committing_usr
        self.token = token

        self.u = resolve_github_url(repo_url)
        self.u = URL.from_string(self.u)

        self.usr = self.u.path_segment(0)
        self.repo_name = self.u.path_segment(1)
        self.usr_repo = self.usr + '/' + self.repo_name

        self.repo: DulwichRepo | None = None

        self.cred_usr = None
        self.cred_tok = None
        self.cred_url = None

        self._resolve_local_path()

    def _resolve_local_path(self) :
        if self.local_path is not None :
            return

        elif self.containing_dir is not None :
            if not self.containing_dir.exists() :
                self.containing_dir.mkdir()

            self.local_path = Path(self.containing_dir) / self.repo_name

        elif self.containing_dir is None :
            self.local_path = Path(self.repo_name)

    def _set_cred_usr_tok(self) :
        cu = self.committing_usr
        tok = self.token
        if (cu is not None) and (tok is not None) :
            self.cred_usr , self.cred_tok = cu , tok
            return
        if cu is not None :
            self.cred_usr , self.cred_tok = cu , gettoken(cu)
            return
        self.cred_usr , self.cred_tok = self.usr , gettoken(self.usr)

    def _set_cred_url(self) :
        self._set_cred_usr_tok()
        self.cred_url = ret_github_url_wt_credentials(self.cred_usr ,
                                                      self.cred_tok ,
                                                      self.usr ,
                                                      self.repo_name)

    def _stage_all_changes(self) :
        idx = self.repo.open_index()
        lp = str(self.local_path) + '/'
        fu = porcelain.get_untracked_paths
        untracked = fu(lp , lp , idx , exclude_ignored = True)
        unstaged = index.get_unstaged_changes(idx , self.local_path)
        all_changes = list(unstaged) + list(untracked)
        self.repo.stage(all_changes)
        return all_changes

    def clone_overwrite(self , depth = 1) :
        """ Every time excecuted, it re-downloads last version of the reposiroty to local_path.

        param depth: None for full depth, default = 1 (last version)
        return: None
        """
        self.rmdir()
        dirr = self.local_path
        try :
            self.repo = porcelain.clone(str(self.u) , dirr , depth = depth)
        except HTTPUnauthorized :
            self._set_cred_url()
            self.repo = porcelain.clone(self.cred_url , dirr , depth = depth)

    def commit_and_push(self , commit_msg , branch = 'main') :
        if self.cred_url is None :
            self._set_cred_url()
        self._stage_all_changes()
        bmsg = commit_msg.encode()
        self.repo.do_commit(bmsg)
        porcelain.push(str(self.local_path) , self.cred_url , branch)
        print(commit_msg)

    def rmdir(self) :
        if (self.local_path.exists()) and (self.local_path != Path.cwd()) :
            shutil.rmtree(self.local_path)

def ret_github_url_wt_credentials(user , token , targ_usr , targ_repo) :
    return f'https://{user}:{token}@github.com/{targ_usr}/{targ_repo}'

def resolve_github_url(url) :
    if url.startswith(gbu) :
        return url
    return gbu + url
