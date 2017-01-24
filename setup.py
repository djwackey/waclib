#-*- coding: utf-8 -*-

import os
from distutils.core import setup

from waclib import utils

LIB_NAME = "waclib"
CUR_DIR = os.getcwd()
DIRS = utils.list_dirs(CUR_DIR +"/"+ LIB_NAME)

def get_packages(lib_name, main_dirs):
    packages = [lib_name]
    for child_dir in main_dirs:
        packages.append(lib_name +"."+ child_dir)

    return packages

PACKAGES = get_packages(LIB_NAME, DIRS)
AUTHOR = "wackey"
EMAIL = "worcy_kiddy@126.com"
URL = "blog.csdn.net/worcy_kiddy"
VERSION = "1.0.0"
DESCRIPTION = "wackey's lib"

setup(name=LIB_NAME,
      version=VERSION,
      description=DESCRIPTION,
      author=AUTHOR,
      author_email=EMAIL,
      url=URL,
      packages=PACKAGES,
     )
