#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, re, sys
from twisted.web.client import downloadPage
PY3 = sys.version_info.major >= 3
print("Update.py")

def upd_done():        
    print( "In upd_done")
    xfile ='http://patbuweb.com/tvSettings/tvsettings.tar'
    if PY3:
        xfile = b"http://patbuweb.com/tvSettings/tvsettings.tar"
        print("Update.py in PY3")
    import requests
    response = requests.head(xfile)
    if response.status_code == 200:
        # print(response.headers['content-length'])
        fdest = "/tmp/tvsettings.tar"
        print("Code 200 upd_done xfile =", xfile)
        downloadPage(xfile, fdest).addCallback(upd_last)
    elif response.status_code == 404:
        print("Error 404")
    else:
        return

def upd_last(fplug):
    import time
    time.sleep(5)        
    if os.path.isfile('/tmp/tvsettings.tar') and os.stat('/tmp/tvsettings.tar').st_size > 10000 : 
        import os
        cmd = "tar -xvf /tmp/tvsettings.tar -C /"
        print( "cmd A =", cmd)
        os.system(cmd)
    return
    
