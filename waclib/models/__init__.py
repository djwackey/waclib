#-*- coding: utf-8 -*-

import sys
import cPickle as pickle
from threading import local

from waclib.core import app

enable_storage_context = app.enabled_storage_context()


class SerializerMetaClass(type):

    def __init__(self, name, bases, attrs):
        super(SerializerMetaClass, self).__init__(name, bases, attrs)
        # 用config.conf中的配置信息设置类属性
        app.init_models(self)
        if hasattr(self, "seq_attrs") or hasattr(self, "adv_seq_attrs"):
            print >> sys.stderr, 'Warning: "seq_attrs" and \
                "adv_seq_attrs were deprecated, please use "def_attrs".', self
        self._get_def_attrs(bases)

    def _get_def_attrs(self, bases):
        if hasattr(self, "def_attrs"):
            def_attrs = dict(getattr(self, "def_attrs"))
            for attr, v in def_attrs.items():
                if v != "adv" and v != "simple":
                    if not hasattr(self, v+"_loads") or \
                        not hasattr(self, v+"_dumps"):
                        raise ValueError("Invalid field define. \
                        Model:%s field:%s value:%s" % (self.__name__, attr, v))
        else:
            def_attrs = {}

        # def_attrs is empty dict
        if not def_attrs:
            seq_attrs = getattr(self, "seq_attrs", [])
            adv_seq_attrs = getattr(self, "adv_seq_attrs", [])
            for attr in seq_attrs:
                if attr in adv_seq_attrs and not def_attrs.has_key(attr):
                    def_attrs[attr] = "adv"
                else:
                    def_attrs[attr] = "simple"

        for base in bases:
            if hasattr(base, "all_def_attrs"):
                base_def_attrs = getattr(base, "all_def_attrs")
                for k, v in base_def_attrs.items():
                    if not def_attrs.has_key(k):
                        def_attrs[k] = v
        setattr(self, "all_def_attrs", def_attrs)


class Serializer(object):
    __metaclass__ = SerializerMetaClass

    def __init__(self):
        super(Serializer, self).__init__()

    @classmethod
    def loads(cls, data):
        """ 将一个dict转换成model对象实例
            data: dict对象
        """
        def_attrs = cls.all_def_attrs

        obj = cls()
        for attr in def_attrs:
            if attr in data:
                if def_attrs[attr] == "simple":
                    setattr(obj, attr, data[attr])
                elif def_attrs[attr] == "adv":
                    if data[attr]:
                        setattr(obj, attr, pickle.loads(str(data[attr])))
                    else:
                        setattr(obj, attr, None)
                else:
                    loads_func = getattr(obj, def_attrs[attr]+"_loads")
                    setattr(obj, attr, loads_func(data[attr]))
        return obj

    def dumps(self, attrs=None, shallow=False):
        def_attrs = self.all_def_attrs
        if attrs is not None:
            seq_attrs = attrs
        else:
            seq_attrs = def_attrs.keys()

        data = {}
        for attr in seq_attrs:
            val = getattr(self, attr)
            if def_attrs[attr] == "simple":
                if app.debug:
                    vtype = type(val)
                    if vtype == dict or vtype == list or vtype == tuple:
                        raise RuntimeError("dumps error! Model:%s Field:%s" % \
                                           (self.__class__.__name__, attr))
                data[attr] = val
            elif def_attrs[attr] == "adv":
                data[attr] = val if shallow else \
                            pickle.dumps(val, pickle.HIGHEST_PROTOCOL)
            else:
                dumps_func = getattr(self, def_attrs[attr]+"_dumps")
                data[attr] = dumps_func(val)
        return data


class StorageContext(local):

    def __init__(self):
        self._keys = set()
        self._storage = {}

    def clear(self):
        """ 清除所有缓存的数据，未保存的数据会丢失
        """
        if enable_storage_context:
            self._keys.clear()
            self._storage.clear()

        # 重置存储相关状态（比如关闭数据库链接，关闭memcached链接）
        app.reset_storage_engines()

    def put(self, key, obj, need_save=True):
        """ 缓存对象实例
            key:  缓存用的key
            obj:  需要缓存的对象实例
            need_save: 是否需要真实保存。
                True: 调用save()方法时会进行将数据存储到持久层
                False:  只是缓存数据
        """
        if enable_storage_context:
            self._storage[key] = obj
            if need_save:
                self._keys.add(key)

    def get(self, key):
        if enable_storage_context:
            return self._storage.get(key, None)

    def save(self):
        if enable_storage_context:
            for key in self._keys:
                obj = self._storage.get(key)
                if obj is not None:
                    obj.do_put()
            self.clear()

        # 重置存储相关状态（比如关闭数据库链接，关闭memcached链接）
        app.reset_storage_engines()

    def delete(self, key):
        try:
            del self._storage[key]
        except:
            pass
        try:
            self._keys.remove(key)
        except:
            pass


class BaseModel(Serializer):
    storage_context = StorageContext()
    cache_prefix = ""

    def __init__(self):
        pass

    @classmethod
    def get(cls, pkey):
        cache_key = cls.make_cache_key(pkey)

        if enable_storage_context:
            obj = cls.storage_context.get(cache_key)
            if obj is not None:
                return obj

        obj = cls.do_get(cache_key, pkey)

        if enable_storage_context:
            if  obj is not None:
                cls.storage_context.put(cache_key, obj, False)

        return obj

    @classmethod
    def do_get(cls, cache_key, pkey):
        pass

    @classmethod
    def make_cache_key(cls, pkey):
        return "%s|%s.%s|%s" % (cls.cache_prefix, cls.__module__, cls.__name__,
                                pkey)
