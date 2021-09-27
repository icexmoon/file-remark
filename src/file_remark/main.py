import os
import time
from file_remark.config import Config
from file_remark.module.m_files import MFiles
from file_remark.my_db import MyDB
from file_remark.tools import Tools


class Main:
    def set_print_mode(self, new_print_mode: int):
        '''设置打印模式'''
        config: Config = Config()
        config.print_mode = new_print_mode
        # print(config.print_mode)
        # print(id(config))

    def print_help(self):
        config: Config = Config()
        help_file = config.get_help_file()
        with open(file=help_file, mode='r', encoding='UTF-8') as fopen:
            for line in fopen:
                print(line, end='')
        print()

    def list_remarks(self):
        '''展示当前工作目录下设置了备注的文件'''
        # 获取当前工作目录下的所有文件和目录
        config: Config = Config()
        # print(id(config))
        # print(config.print_mode)
        names = os.listdir(os.getcwd())
        paths = []
        for name in names:
            path = os.getcwd()+config.get_path_split()+name
            # if os.path.isfile(path):
            paths.append(path)
        # 匹配数据库中添加了备注的文件
        m_files = MFiles()
        file_remarks = m_files.search_path(paths)
        # 按照选项进行打印
        if config.print_mode == Config.PRINT_ONLY_REMARK:
            self.__print_remarks(file_remarks)
        elif config.print_mode == Config.PRINT_REMARK_FIRST:
            self.__print_remarks(file_remarks)
            self.__print_others(names, file_remarks, m_files)
        elif config.print_mode == Config.PRINT_REMARK_LAST:
            self.__print_others(names, file_remarks, m_files)
            self.__print_remarks(file_remarks)
        else:
            pass

    def __print_remarks(self, file_remarks):
        # file_remarks = m_files.search_path(paths)
        for file_remark in file_remarks:
            print("{} [{}]".format(file_remark['name'], file_remark['remark']))

    def __print_others(self, names, file_remarks, m_files):
        config = Config()
        for name in names:
            path = os.getcwd()+config.get_path_split()+name
            if not m_files.is_in_file_remarks(path, file_remarks):
                print(name)

    def list_all(self):
        '''展示所有设置了备注的文件'''

    def add_remark(self, file_path: str, remark: str):
        '''给文件添加备注'''
        file_path = Tools.get_abs_path(file_path)
        if not os.path.exists(file_path):
            print('文件{}不存在，不能添加备注！'.format(file_path))
            return
        m_files = MFiles()
        file_remark = m_files.get_file_remark(file_path)
        if not file_remark:
            m_files.add_remark(file_path, remark)
        else:
            print('文件{}的备注已经存在，不能重复添加！'.format(os.path.basename(file_path)))

    def remove_remark(self, file_path):
        '''删除文件备注'''

    def modify_remark(self, file_path, remark):
        '''修改文件备注'''

    def remove_all(self):
        '''删除全部备注信息'''
