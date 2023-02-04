#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from twisted.web.client import downloadPage
PY3 = sys.version_info.major >= 3
print("Update.py")


def upd_done():
    print("In upd_done")
    xfile = 'http://patbuweb.com/tvSettings/tvsettings.tar'
    if PY3:
        xfile = b"http://patbuweb.com/tvSettings/tvsettings.tar"
        print("Update.py in PY3")
    import requests
    response = requests.head(xfile)
    if response.status_code == 200:
        # print(response.headers['content-length'])
        print("Code 200 upd_done xfile =", xfile)
        fdest = "/tmp/tvsettings.tar"
        downloadPage(xfile, fdest).addCallback(upd_last)
    elif response.status_code == 404:
        print("Error 404")
    else:
        return


def upd_last(fplug):
    import time
    import os
    time.sleep(5)
    fdest = "/tmp/tvsettings.tar"
    if os.path.isfile(fdest) and os.stat(fdest).st_size > 10000:
        cmd = "tar -xvf /tmp/tvsettings.tar -C /"
        print("cmd A =", cmd)
        os.system(cmd)
        os.remove('/tmp/tvsettings.tar')
    return
