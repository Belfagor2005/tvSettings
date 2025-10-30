#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
PY3 = sys.version_info.major >= 3
print("Update.py")


def upd_done():
    from os import popen, system
    cmd01="wget -q --no-check-certificate https://raw.githubusercontent.com/Belfagor2005/tvSettings/main/installer.sh -O - | /bin/sh"
    popen(cmd01)
    return
