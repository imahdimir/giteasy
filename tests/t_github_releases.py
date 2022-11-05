from pathlib import Path

import requests

from src.giteasy.github_releases import get_filename_fr_github_resp
from src.giteasy.github_releases import \
    get_tar_url_of_latest_release_of_a_public_github_repo


##
rp = 'https://github.com/imahdimir/make-day-plan-in-Todoist-fr-notion'
url = get_tar_url_of_latest_release_of_a_public_github_repo(rp)
url

##
r = requests.get(url)
r.headers
##
r.headers
import re


##
get_filename_fr_github_resp(r)

##


##


##
from mirutil.codal import find_fn_and_suf_fr_codal_get_resp


find_fn_and_suf_fr_codal_get_resp(r.headers)

##
with open('t.tar.gz' , 'wb') as f :
    f.write(r.content)

##
def find_filename_fr_resp_header(resp) :
    hdr = resp.headers
    cd = hdr['content-disposition']
    pat = 'filename=(.+)\.(\w+)'
    rf = re.findall(pat , cd)
    if len(rf) == 0 :
        return RFindFn(None , None)
