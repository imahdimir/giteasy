"""

  """

import importlib

import src.giteasy as sgi


importlib.reload(sgi)

from src.giteasy.repo import get_github_tok_fp
from src.giteasy.repo import Repo
from src.giteasy.githubb import ret_pygithub_repo_obj , get_all_fps_in_repo


## test get_github_token_pathes()
fp = get_github_tok_fp()
print(fp)

## clone a public repo
u = 'https://github.com/imahdimir/d-TSETMC_ID-2-FirmTicker'
repo = Repo(u)
repo.overwriting_clone()

##
repo.rmdir()

## clone a private repo
ur = 'https://github.com/imahdimir/test-private'
rp = Repo(ur)
rp.overwriting_clone()

##
rp.commit_and_push('test commit')

##
rp.rmdir()

##
rp = 'https://github.com/imahdimir/Codal-monthly-sales-htmls'
ob = ret_pygithub_repo_obj(rp)
x = get_all_fps_in_repo(rp)
print(x)
print(len(x))

##
rp = 'https://github.com/imahdimir/td-u-d0-FirmTicker-MonthlySales'
ob = ret_pygithub_repo_obj(rp)
find_sha_of_a_file_in_github_repo(rp , 'a.prq')

##
rp = 'https://github.com/imahdimir/td-u-d0-FirmTicker-MonthlySales'
fp0 = '/Users/mahdi/Dropbox/1-git-dirs/PyCharm/u-d0-FirmTicker-MonthlySales/link-htmls/302345.html'
fp1 = '/Users/mahdi/Dropbox/1-git-dirs/PyCharm/u-d0-FirmTicker-MonthlySales/link-htmls/302229.html'
fps = [fp0 , fp1]
asyncio.run(add_xor_overwrite_txt_based_files_2_github_repo_async(fps , rp))

##
rp = 'https://github.com/imahdimir/td-u-d0-FirmTicker-MonthlySales'
di = '/Users/mahdi/Dropbox/1-git-dirs/PyCharm/u-d0-FirmTicker-MonthlySales/link-htmls'
fu = add_txt_based_files_fr_dir_to_github_repo_async
asyncio.run(fu(di , 'html' , rp))

##
rp = 'https://github.com/imahdimir/td-u-d0-FirmTicker-MonthlySales'
ob = ret_pygithub_repo_obj(rp)
fp = '/Users/mahdi/Downloads/pr.py'
with open(fp , 'rb') as f :
    content = f.read()
ob.create_file('1.py' , 'test commit' , content)

##
