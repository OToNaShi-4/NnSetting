import os
from enum import Enum
from typing import Dict, Type, Tuple, Generic, TypeVar, Any

from NnSetting.Source import Source

_Settings: Dict[str, Type['DefaultSettings']] = {}


@property
def currentSetting() -> Type['DefaultSettings']:
    pass


class Property:

    def __init__(self, value, editable: bool = False):
        self.value = value
        self.editable = editable

    def __set_name__(self, owner, name):
        if not isinstance(owner, _Setting):
            raise RuntimeError("本类只能在DefaultSetting中或者其子类中被实例化")
        self.name = name

    def __get__(self, instance, owner):
        return self.value

    def __set__(self, instance, value):
        if not self.editable:
            raise RuntimeError(f"属性{self.name}不可更改")
        self.value = value


class _Setting(type):

    def __new__(cls, name, bases: tuple, attrs: dict):
        Class = type.__new__(cls, name, bases, attrs)
        global _Settings
        _Settings[_Setting.get_lower_case_name(name)] = Class
        return Class

    @staticmethod
    def get_lower_case_name(name: str):
        text = name.replace('Settings', '').replace('Setting', '')
        lst = []
        for index, char in enumerate(text):
            if char.isupper() and index != 0:
                lst.append("_")
            lst.append(char)
        return "".join(lst).lower()


class responseType(Enum):
    stateInBody = 1
    stateInHeader = 2


class DefaultSettings(metaclass=_Setting):
    # RedisSettings
    redis_address: str = Property('localhost')
    redis_port: str = Property(6379)
    redis_pool_size_max: int = Property(16)
    redis_pool_size_min: int = Property(8)
    redis_password: str = Property('')

    # MysqlSettings
    mysql_host: str = Property('localhost')
    mysql_port: str = Property(3306)
    mysql_db: str = Property('')
    mysql_max_size: int = Property(20)
    mysql_min_size: int = Property(5)
    mysql_user: str = Property('root')
    mysql_password: str = Property('')

    @classmethod
    def getMysqlSettings(cls) -> Dict:
        return {
            'host'    : cls.mysql_host,
            'port'    : cls.mysql_port,
            'db'      : cls.mysql_db,
            'user'    : cls.mysql_user,
            'password': cls.mysql_password,
            'minsize' : cls.mysql_min_size,
            'maxsize' : cls.mysql_max_size
        }

    @classmethod
    def getRedisSettings(cls) -> Dict:
        data = {
            'address': (cls.redis_address, cls.redis_port),
            'minsize': cls.redis_pool_size_min,  # 连接池最小数量
            'maxsize': cls.redis_pool_size_max  # 连接池最大数量
        }
        if cls.redis_password:
            data['password'] = cls.redis_password
        return data

    @classmethod
    def getTornadoSettings(cls) -> Dict:
        return {
            'current_path' : cls.current_path,
            'static_path'  : cls.static_path,
            'cookie_secret': cls.cookie_secret,
            'xsrf_cookies' : cls.xsrf_cookies,
            'debug'        : cls.debug,
            'autoreload'   : cls.autoreload,
            'xheaders'     : cls.xheaders
        }


T = TypeVar('T', bound=Type[DefaultSettings])


class NnSetting(Generic[T]):
    """
    调用此类则会返回当前设置类
    """

    env_name: str = 'py_setting'
    source: Source

    def __init__(self, source: Source = Source):
        self.source = source

    def __getitem__(self, item) -> T:
        return _Settings[item]

    def __getattr__(self, item) -> Any:
        return object.__getattribute__(self[self.source.name], item)

    @property
    def cur(self) -> T:
        return self[self.source.name]

