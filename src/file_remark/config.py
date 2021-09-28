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
            self.db_config:dict[str] = dict() # 数据库配置
            Config.inited = True

    def set_db_config(self, name:str, value: str)->None:
        '''设置数据库配置
        name 配置名称
        value 配置内容
        '''
        self.db_config[name] = value


    def get_home(self):
        '''获取应用的主目录'''
        return os.path.dirname(__file__)

    def get_path_split(self) -> str:
        return os.path.sep

    def get_data_dir(self)->str:
        '''获取数据目录'''
        return self.__get_dir('data')

    def get_help_file(self)->str:
        '''获取帮助文件路径'''
        return self.get_data_dir()+self.get_path_split()+'help.info'

    def get_sql_dir(self)->str:
        '''获取sql目录'''
        return self.__get_dir('sql')

    def __get_dir(self, dir_name:str)->str:
        '''获取应用的二级目录,如果不存在，会创建
        dir_name 二级目录名称
        return 二级目录路径
        '''
        data_dir = self.get_home()+self.get_path_split()+dir_name
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
        return data_dir

