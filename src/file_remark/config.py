from typing import Any
import os


class Config:
    '''配置类'''
    PRINT_ONLY_REMARK = 1
    PRINT_REMARK_FIRST = 2
    PRINT_REMARK_LAST = 3
    inited = False

    def __new__(cls) -> Any:
        if not hasattr(cls, "__instance"):
            setattr(cls, "__instance", super().__new__(cls))
        return getattr(cls, "__instance")

    def __init__(self) -> None:
        if not Config.inited:
            self.print_mode = Config.PRINT_REMARK_FIRST
            Config.inited = True

    def get_home(self):
        '''获取应用的主目录'''
        return os.path.dirname(__file__)

    def get_path_split(self) -> str:
        return os.path.sep

    def get_data_dir(self):
        '''获取数据目录'''
        data_dir = self.get_home()+self.get_path_split()+'data'
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        return data_dir

    def get_help_file(self):
        '''获取帮助文件路径'''
        return self.get_data_dir()+self.get_path_split()+'help.info'
