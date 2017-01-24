#-*- coding: utf-8 -*-

import sys
import json

from waclib.utils.importlib import import_by_name

class Application(object):

    def __init__(self):
        super(Application, self).__init__()
        self.storage_engines = {}
        # 配置实例词典
        self.cfg_inst_dict = {"storage_cfg_file": [None, self._init_storage_engine], # 存储层配置
                              "model_cfg_file":   [None, self._init_model_engine],   # 模型层配置
                              "cache_cfg_file":   [None, self._init_cache_engine],   # 缓存层配置
                              "logic_cfg_file":   [None, self._init_logic_engine],   # 逻辑层配置
                              }
        self.debug = False

    def init(self, **kwargs):
        for cfg_file in self.cfg_inst_dict:
            if kwargs.has_key(cfg_file):
                cfg_obj = Config()
                cfg_obj.Read(kwargs[cfg_file])
            # 初始化实例配置
            self._init_inst_config(cfg_file, cfg_obj)
            # 初始化引擎配置
            self._init_engine_config(cfg_file)

    def _init_inst_config(self, cfg_file, cfg_obj):
        """ 初始化实例配置 """
        self.cfg_inst_dict[cfg_file][0] = cfg_obj

    def _init_engine_config(self, cfg_file):
        """ 初始化引擎配置 """
        cfg_engine_obj, cfg_engine_func = self.cfg_inst_dict[cfg_file]
        cfg_engine_func(cfg_engine_obj)

    def _init_storage_engine(self, cfg_engine_obj):
        """ init storage engine """
        if not hasattr(cfg_engine_obj, "storage_engines"):
            sys.exit("Can't find 'storage_engines' in config file.")

        for engine in cfg_engine_obj.storage_engines:
            cls = import_by_name(engine.get("class"))
            engine_obj = cls()
            engine_obj.configure(engine.get("config"))
            self.storage_engines[engine.get("sname")] = engine_obj

    def _init_model_engine(self, cfg_engine_obj):
        """ init model engine """
        pass

    def _init_cache_engine(self, cfg_engine_obj):
        """ init cache engine """
        pass

    def _init_logic_engine(self, cfg_engine_obj):
        """ init logic engine """
        pass

    def get_engine(self, engine_name):
        return self.storage_engines.get(engine_name)


class Config(object):
    def __init__(self):
        super(Config, self).__init__()

    def Read(self, cfg_file):
        cf = open(cfg_file)
        try:
            js = json.load(cf)
            for k in js:
                if k != "__builtins__":
                    setattr(self, k, js[k])
        finally:
            cf.close()

app = Application()
