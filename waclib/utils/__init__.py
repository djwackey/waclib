#-*- coding: utf-8 -*-

import os
import hashlib

def list_dirs(path):
    files = os.listdir(path)
    dirs = []
    for f in files:
        if os.path.isdir(path +"/"+ f):
            dirs.append(f)
    return dirs

def make_sign(params):
    key = [(k, v) for k, v in params.iteritems()]
    sorted_data = sorted(key, key=lambda x: x[0], reverse=False)
    list_data = ['%s=%s' % (str(k), str(v)) for k, v in sorted_data]
    sign_str = '&'.join(list_data)
    return hashlib.md5(sign_str).hexdigest()
