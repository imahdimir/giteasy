"""

  """

from pathlib import Path

from src.giteasy.github import add_overwrite_a_file_2_repo
from src.giteasy.github import ret_pygithub_repo_obj


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
