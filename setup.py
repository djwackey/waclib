#-*- coding: utf-8 -*-

import os
from waclib import utils
from distutils.core import setup

lib_name = "waclib"
cur_dir = os.getcwd()
dirs = utils.list_dirs(cur_dir +"/"+ lib_name)

def _get_packages(lib_name, dirs):
    packages = []
    for dir in dirs:
        packages.append(lib_name +"."+ dir)

    # add myself.
    packages.append(lib_name)
    return packages

packages = _get_packages(lib_name, dirs)
version = "1.0.0"

setup(name=lib_name,
      version=version,
      description="wackey's lib",
      author='wackey',
      author_email='worcy_kiddy@126.com',
      url='blog.csdn.net/worcy_kiddy',
      packages=packages,
     )
