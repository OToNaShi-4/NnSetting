# 1. 导入NnSetting 及 相关依赖项
from NnSetting import NnSetting, DefaultSettings, Property
from typing import Type  # python的范型声明库
from NnSetting.Source import EnvSource  # 导入设置源，他负责告诉NnSetting启用那个设置


# 2. 创建一个设置类 ⚠️ ： 每个设置类都需要继承自DefaultSettings
class MySetting(DefaultSettings):
    # 3. 定义设置属性
    # ⚠️ 属性类型可以是任意类型, 但需要使用Property进行声明
    my_setting: int = Property(1)  # 定义一个整数属性
    my_setting_2: str = Property("lalalal")  # 定义一个字符串属性
    my_setting_3: bool = Property(True)  # 定义一个布尔属性
    my_setting_4: float = Property(0.0)  # 定义一个浮点属性

    @classmethod
    def get_source(cls) -> dict:
        return {
            'my_setting': cls.my_setting,

        }


# 创建第二个设置类，并继承第一个类
class LocalSetting(MySetting):
    my_setting_2 = Property('gagaga')  # 重载父类的设置


# 4. 创建一个NnSetting设置实例,并将设置源作为参数传入,他负责管理所有的设置类
# ⚠️ ： NnSetting 支持范型声明， 可以将自己的基类作为 范型参数传入类型声明
setting: NnSetting[Type[MySetting]] = NnSetting(EnvSource('config'))
