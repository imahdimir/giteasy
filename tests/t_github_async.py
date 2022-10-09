"""

    """

import asyncio
from pathlib import Path

from src.giteasy.funcs import get_token
from src.giteasy.github import ret_usr_repo_from_repo_url
from src.giteasy.github_async import add_overwrite_a_file_2_repo_async
from src.giteasy.github_async import add_overwrite_files_2_repo_async
from src.giteasy.github_async import get_rare_limit
from src.giteasy.github_async import make_header


##
fu = get_rare_limit()
asyncio.run(fu)

##
fp = Path('/Users/mahdi/Downloads/Stata_to_LaTeX.pdf')
url = 'https://github.com/imahdimir/td-u-d0-FirmTicker-MonthlySales'

tok = get_token()
hdrs = make_header(tok)
ur = ret_usr_repo_from_repo_url(url)

fu = add_overwrite_a_file_2_repo_async(fp ,
                                       '14.pdf' ,
                                       None ,
                                       ur ,
                                       'main' ,
                                       hdrs)

##
asyncio.run(fu)
##
fu1 = add_overwrite_a_file_2_repo_async(fp ,
                                        '15.pdf' ,
                                        None ,
                                        ur ,
                                        'main' ,
                                        hdrs)

##
_fu = asyncio.gather(*[await fu , await fu1])
asyncio.run(_fu)

##
url = 'https://github.com/imahdimir/td-u-d0-FirmTicker-MonthlySales'

pth = '/Users/mahdi/Dropbox/1-git-dirs/PyCharm/u-d0-FirmTicker-MonthlySales/link-htmls'
diir = Path(pth)

fps = diir.glob('*.html')
fps = list(fps)
fps = fps[:5]

fu = add_overwrite_files_2_repo_async(fps , url , 'main')

asyncio.run(fu)

##
