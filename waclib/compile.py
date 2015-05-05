#-*- coding: utf-8 -*-

import os
import utils	# from waclib #
import compileall

"""
* py_compile *
This module allows you to explicitly compile Python modules 
to bytecode. It behaves like Python’s import statement, 
but takes a file name, not a module name.
"""
"""
* compileall *
This module contains functions to compile all Python scripts 
in a given directory (or along the Python path) to bytecode. 
It can also be used as a script (on Unix platforms, it’s 
automatically run when Python is installed).
"""

def exec_compile(package_list):
    for package in package_list:
        compileall.compile_dir(package, force=1)

# list all packages
cur_dir = os.getcwd()
package_list = utils.list_dirs(cur_dir)

# compile all
print "This may take a while!"
exec_compile(package_list)
