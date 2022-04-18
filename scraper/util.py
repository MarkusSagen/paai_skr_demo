import os
from pathlib import Path
from sys import platform

import requests


def is_local_download_link(url):
    return url[0] == "/"


def _config_requests():
    # DEAL with issues then parsing the docs
    # https://stackoverflow.com/questions/10667960/python-requests-throwing-sslerror
    if platform == "linux" or platform == "linux2":
        # debian
        os.environ["REQUESTS_CA_BUNDLE"] = os.path.join(
            "/etc/ssl/certs/", "ca-certificates.crt"
        )

    # https://stackoverflow.com/questions/38015537/python-requests-exceptions-sslerror-dh-key-too-small
    requests.packages.urllib3.disable_warnings()
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "ALL:@SECLEVEL=1"
    try:
        requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += (
            ":HIGH:!DH:!aNULL"
        )
    except AttributeError:
        # no pyopenssl support used / needed / available
        pass
