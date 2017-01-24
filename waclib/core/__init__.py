#-*- coding: utf-8 -*-

import sys
import json

from waclib.utils.importlib import import_by_name

class Application(object):
    """ 应用程序
        cfg_inst_dict - 配置实例词典
            1.storage_cfg_file - 存储层配置
                [存储配置数据, 存储引擎回调函数]
            2.model_cfg_file - 模型层配置
                [模型配置数据, 模型引擎回调函数]
            3.cache_cfg_file - 缓存层配置
            4.logic_cfg_file - 逻辑层配置
    """

    def __init__(self):
        super(Application, self).__init__()
        self.enable_storage_context = False
        self.storage_engines = {}
        self.model_default = {}

        self.cfg_inst_dict = {"storage_cfg_file": [None,
                                                   self._init_storage_engine],
                              "model_cfg_file":   [None,
                                                   self._init_model_engine],
                              "cache_cfg_file":   [None,
                                                   self._init_cache_engine],
                              "logic_cfg_file":   [None,
                                                   self._init_logic_engine],
                              }
        self.debug = False

    def init(self, **kwargs):
        for cfg_file in self.cfg_inst_dict:
            if kwargs.has_key(cfg_file):
                cfg_obj = Config()
                cfg_obj.Read(kwargs[cfg_file])

            self._init_inst_config(cfg_file, cfg_obj)
            self._init_engine_config(cfg_file)

    def _init_inst_config(self, cfg_file, cfg_obj):
        """ 初始化实例配置 """
        self.cfg_inst_dict[cfg_file][0] = cfg_obj

    def _init_engine_config(self, cfg_file):
        """ 初始化引擎配置 """
        cfg_engine_obj, cfg_engine_func = self.cfg_inst_dict[cfg_file]
        cfg_engine_func(cfg_engine_obj)

    def reset_storage_engines(self):
        """ 重置存储相关状态（比如关闭数据库链接，关闭memcached链接）"""
        for engine_name, storage_engine in self.storage_engines.iteritems():
            storage_engine.reset()

    @property
    def enabled_storage_context(self):
        """ enabled storage_context """
        return self.enable_storage_context

    def init_models(self, model_cls):
        m_name = model_cls.__name__
        if m_name == "Serializer" or m_name == "BaseModel":
            return

        for attr in self.model_default:
            setattr(model_cls, attr, self.model_default[attr])

        model_config = self.cfg_inst_dict["model_cfg_file"][0]

        if model_config.models.has_key(m_name):
            for attr in model_config.models[m_name]:
                setattr(model_cls, attr, model_config.models[m_name][attr])

    def _init_storage_engine(self, cfg_engine_obj):
        """ init storage engine """
        if not hasattr(cfg_engine_obj, "storage_engines"):
            sys.exit("Can't find 'storage_engines' in config file.")

        if hasattr(cfg_engine_obj, "enable_storage_context"):
            self.enable_storage_context = cfg_engine_obj.enable_storage_context

        for engine in cfg_engine_obj.storage_engines:
            cls = import_by_name(engine.get("class"))
            engine_obj = cls()
            engine_obj.configure(engine.get("config"))
            self.storage_engines[engine.get("sname")] = engine_obj

    def _init_model_engine(self, cfg_engine_obj):
        """ init default model engine """
        if hasattr(cfg_engine_obj, "model_default"):
            self.model_default = getattr(cfg_engine_obj, "model_default")

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
