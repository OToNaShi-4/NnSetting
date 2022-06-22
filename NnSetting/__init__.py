from enum import Enum
from typing import Dict, Type, Generic, TypeVar, Any

from NnSetting.Source import Source

# 用于存储所有Setting类的缓存， 格式为 类名：设置类
_SETTINGS_CACHE: Dict[str, Type['DefaultSettings']] = dict()

A = TypeVar('A')


class Property(Generic[A]):
    """
    Property基类， 所有设置上的成员尽可能通过本类包裹住

    本类只做基础的常量功能，若有其他需求，请重载此类
    """

    def __init__(self, value: A, editable: bool = False):
        self.value = value
        self.editable = editable

    def __set_name__(self, owner, name):
        """
        本类在Setting类中被实例化时被调用
        :param owner: 本类的所有者
        :param name: 本类所绑定的变量名
        """
        if not isinstance(owner, _Setting):
            raise RuntimeError("本类只能在DefaultSetting中或者其子类中被实例化")
        self.name = name

    def __get__(self, instance, owner) -> A:
        return self.value

    def __set__(self, instance, value: A):
        if not self.editable:
            raise RuntimeError(f"属性{self.name}不可更改")
        self.value = value


class _Setting(type):

    def __new__(cls, name, bases: tuple, attrs: dict):
        """
        重载所有子类的创建过程，并把子类存入缓存中
        :param name: 子类类名
        :param bases: 所有继承的类
        :param attrs: 继承参数
        """
        Class = type.__new__(cls, name, bases, attrs)
        global __SETTINGS_CACHE
        __SETTINGS_CACHE[_Setting.get_lower_case_name(name)] = Class
        return Class

    @staticmethod
    def get_lower_case_name(name: str):
        """
        获取类对应的蛇形命名
        :return:
        """
        text = name.replace('Settings', '').replace('Setting', '')
        lst = []
        for index, char in enumerate(text):
            if char.isupper() and index != 0:
                lst.append("_")
            lst.append(char)
        return "".join(lst).lower()


class DefaultSettings(metaclass=_Setting):
    """
        本类用于隐藏metaclass的存在

        以减少用户在使用本工具过程中导致的一些对与metaclass的疑惑
    """
    ...


T = TypeVar('T', bound=Type[DefaultSettings])


class NnSetting(Generic[T]):
    """
    所有设置的代理

    调用此类则会返回当前设置类
    """

    source: Source

    def __init__(self, source: Source = Source()):
        """
        接受一个source类作为参数
        用于告诉 NnSetting 要使用那个设置
        :param source: 设置源
        """
        self.source = source

    def __getitem__(self, item) -> Type[T]:
        """
        获取指定名称的设置类
        :param item: 设置类的蛇形命名
        :return: 对应设置类
        """
        return _SETTINGS_CACHE[item]

    def __getattr__(self, item) -> Any:
        """
        获取当前设置类下的Property内容
        不推荐使用，建议使用 cur 获取当前设置

        :param item: Property名称
        :return: 当前设置的Property内容
        """
        return object.__getattribute__(self[self.source.name], item)

    @property
    def cur(self) -> Type[T]:
        """
        功能大致同上
        但使用这个入口时ide可以给你预测你设置类中的内容

        :return: 当前设置类
        """
        return self[self.source.name]
