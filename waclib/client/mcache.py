#-*- coding: utf-8 -*-

try:
    import pylibmc as memcache
    _pylibmc = True
except ImportError, e:
    import memcache
    _pylibmc = False

from waclib.utils.encoding import force_str, force_unicode

class MemcacheClient(object):
    def __init__(self, servers, default_timeout=0):
        '''
        servers is a string like "192.168.0.1:9988;192.168.0.1:9989"
        '''
        self._current = memcache.Client(servers.split(';'))
        if _pylibmc:
            self._current.behaviors['distribution'] = 'consistent'
            self._current.behaviors['tcp_nodelay'] = 1
        self.default_timeout = default_timeout

    def add(self, key, value, timeout=0, min_compress=50):
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        return self._current.add(force_str(key), value, timeout or self.default_timeout, min_compress)

    def get(self, key, default=None):
        try:
            val = self._current.get(force_str(key))
        except:
            val = self._current.get(force_str(key))
        if val is None:
            return default
        return val

    def set(self, key, value, timeout=0, min_compress=50):
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        try:
            return self._current.set(force_str(key), value, timeout or self.default_timeout, min_compress)
        except:
            return self._current.set(force_str(key), value, timeout or self.default_timeout, min_compress)

    def delete(self, key):
        try:
            try:
                val = self._current.delete(force_str(key))
            except:
                val = self._current.delete(force_str(key))
            if type(val) == bool:
                val = 1
        except:
            val = 0
        return val

    def get_multi(self, keys):
        return self._current.get_multi(map(force_str, keys))

    def close(self, **kwargs):
        self._current.disconnect_all()

    def incr(self, key, delta=1):
        return self._current.incr(key, delta)

    def decr(self, key, delta=1):
        return self._current.decr(key, delta)

    def current(self):
        return self._current
