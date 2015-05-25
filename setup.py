#-*- coding: utf-8 -*-

import os
from waclib import utils
from distutils.core import setup

lib_name = "waclib"
cur_dir = os.getcwd()
dirs = utils.list_dirs(cur_dir +"/"+ lib_name)

def get_packages(lib_name, dirs):
    packages = []
    for dir in dirs:
        packages.append(lib_name +"."+ dir)

    # add myself.
    packages.append(lib_name)
    return packages

packages = get_packages(lib_name, dirs)
author = "wackey"
email = "worcy_kiddy@126.com"
url = "blog.csdn.net/worcy_kiddy"
version = "1.0.0"
description = "wackey's lib"

setup(name=lib_name,
      version=version,
      description=description,
      author=author,
      author_email=email,
      url=url,
      packages=packages,
     )
