#-*- coding: utf-8 -*-
import cPickle as pickle

from waclib.models.engine import StorageEngine
from waclib.client.mcache import MemcacheClient

class MemcacheEngine(StorageEngine):
    
    def configure(self, cfg_value):
        StorageEngine.configure(self, cfg_value)
        self.servers = cfg_value.get("servers")
        self.default_timeout = cfg_value.get("default_timeout", 0)
        self.client = MemcacheClient(self.servers, self.default_timeout)
    
    def get_data(self, model_cls, pkey):
        """
        model_cls:  model类对象
        pkey:       model对象主键
        """
        cache_key = model_cls.generate_cache_key(pkey)
        val = self.client.get(cache_key)
        if val is None:
            return None
        return pickle.loads(val)
    
    def put_data(self, model_cls, pkey, data, create_new):
        cache_key = model_cls.generate_cache_key(pkey)
        val = pickle.dumps(data, pickle.HIGHEST_PROTOCOL)
        if create_new:
            flag = self.client.add(cache_key, val, self.default_timeout)
            if not flag:
                raise Exception('memcache client add failure, cache key: %s' % cache_key)
        else:
            flag = self.client.set(cache_key, val, self.default_timeout)
            if not flag:
                raise Exception('memcache client set failure, cache key: %s' % cache_key)
    
    def reset(self):
        self.client.close()
        
    def delete_data(self, model_cls, pkey):
        cache_key = model_cls.generate_cache_key(pkey)
        flag = self.client.delete(cache_key)
        if flag == 0:
            raise Exception('memcache client delete failure, cache key: %s' % cache_key)
        
