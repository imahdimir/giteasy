"""

  """

from src.giteasy.main import get_github_token_pathes
from src.giteasy.main import Repo


## test get_github_token_pathes()
fp = get_github_token_pathes()
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
