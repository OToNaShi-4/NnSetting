import os


class Source:
    """
    Source class
    最基础的设置源class，只能采用默认的设置

    其他源请继承此类，并根据需求重写 name property

    """

    @property
    def name(self) -> str:
        return "default"


class StaticSource(Source):

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name


class EnvSource(Source):
    """
    EnvSource class
    获取环境变量源，可以采用环境变量指定的设置
    可在运行时动态修改指定的设置
    """
    env_name: str

    def __init__(self, env_name: str = "nn_setting"):
        self.env_name = env_name

    @property
    def name(self) -> str:
        return os.getenv(self.env_name, "default")


class EnvFastSource(EnvSource):
    """
    EnvFastSource class
    功能跟EnvSource一样
    但不会每次都在环境变量中查找，而是在第一次调用时就获取并缓存
    执行速度更快 一丢丢
    """
    _name: str = None

    @property
    def name(self) -> str:
        if not self._name:
            self._name = os.getenv(self.env_name, "default")
        return self._name
