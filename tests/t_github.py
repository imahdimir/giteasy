"""

  """

from src.giteasy.githubb import *


##
rp = 'https://github.com/imahdimir/td-u-d0-FirmTicker-MonthlySales'
ob = ret_pygithub_repo_obj(rp)
fp = Path('/Users/mahdi/Downloads/forest-doc.pdf')

with open(fp , 'rb') as f :
    content = f.read()

ob.create_file(fp.name , 'test commit' , content)

##
rp = 'https://github.com/imahdimir/td-u-d0-FirmTicker-MonthlySales'
fp = Path('/Users/mahdi/Downloads/forest-doc.pdf')
add_overwrite_a_file_2_repo(fp , rp)

##

rp = 'https://github.com/imahdimir/td-u-d0-FirmTicker-MonthlySales'
dp = '/Users/mahdi/Dropbox/1-git-dirs/PyCharm/u-d0-FirmTicker-MonthlySales/link-htmls'
diir = Path(dp)
sf = 'html'
fu = ret_fps_and_pygithub_repo_obj
fu(diir , sf , rp)

##
get_github_rate_limit(github_usr = 'imahdimir')

##
