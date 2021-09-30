import os
import time
from file_remark.config import Config
from file_remark.module.m_files import MFiles
from file_remark.my_db import MyDB
from file_remark.tools import Tools
from file_remark.user_exception import UserException


class Main:
    '''程序的入口类'''

    def __init__(self) -> None:
        # 初始化数据库
        db = MyDB()

    def init_process(self):
        '''初始化程序'''
        choice = input('初始化程序将会丢失已添加的文件备注，是否继续（y/n）：')
        if choice != 'y' and choice != 'Y':
            print('终止初始化')
            return
        print('开始程序初始化')
        print('正在重建数据库')
        db: MyDB = MyDB()
        db.reset_db()
        print('初始化结束')

    def set_print_mode(self, new_print_mode: int):
        '''设置打印模式'''
        config: Config = Config()
        config.print_mode = new_print_mode

    def print_version(self):
        '''打印程序版本信息'''
        import pkg_resources
        version = pkg_resources.get_distribution(
            'file-remark-icexmoon').version
        print('当前软件版本：{}'.format(version))
        config: Config = Config()
        print('数据库版本：{}'.format(config.db_config['db_version']))

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
        for file_remark in file_remarks:
            flag = self.__get_flag_by_type(file_remark[MFiles.FIELD_TYPE])
            print("{} {} [{}]".format(
                flag, file_remark['name'], file_remark['remark']))

    def __get_flag_by_type(self, type):
        if type == MFiles.TYPE_DIR:
            return 'd'
        else:
            return '-'

    def __get_flag_by_path(self, path):
        if os.path.isdir(path):
            return 'd'
        else:
            return '-'

    def __print_others(self, names, file_remarks, m_files):
        config = Config()
        for name in names:
            path = os.getcwd()+config.get_path_split()+name
            if not m_files.is_in_file_remarks(path, file_remarks):
                flag = self.__get_flag_by_path(path)
                print('{} {}'.format(flag, name))

    def list_all(self):
        '''展示所有设置了备注的文件'''
        m_files = MFiles()
        file_remarks = m_files.get_all_file_remarks()
        for file_remark in file_remarks:
            flag = self.__get_flag_by_type(file_remark[MFiles.FIELD_TYPE])
            print('{} {} [{}]'.format(
                flag, file_remark[MFiles.FIELD_PATH], file_remark[MFiles.FIELD_REMARK]))
        print('共{}条备注信息'.format(len(file_remarks)))

    def add_remark(self, file_path: str, remark: str):
        '''给文件添加备注'''
        file_path = self.__check_path_exist(file_path)
        m_files = MFiles()
        file_remark = m_files.get_file_remark(file_path)
        if not file_remark:
            m_files.add_remark(file_path, remark)
        else:
            print('文件{}的备注已经存在，不能重复添加！'.format(os.path.basename(file_path)))

    def remove_remark(self, file_path):
        '''删除文件备注'''

    def modify_remark(self, file_path: str, remark: str) -> None:
        '''修改文件备注'''
        file_path = self.__check_path_exist(file_path)
        m_files = MFiles()
        file_remark = m_files.get_file_remark(file_path)
        if file_remark:
            m_files.modify_remark(file_path, remark)
        else:
            raise UserException(UserException.CODE_NO_REMARK,
                                '文件{}的备注信息不存在，不能修改'.format(file_path))

    def remove_all(self):
        '''删除全部备注信息'''

    def __check_path_exist(self, file_path: str) -> str:
        '''检查路径是否存在
        file_path 文件或目录的相对路径或绝对路径
        return 文件或目录的绝对路径
        '''
        file_path = Tools.get_abs_path(file_path)
        if not os.path.exists(file_path):
            error_msg = '文件或目录{}不存在，不能添加备注！'.format(file_path)
            raise UserException(UserException.CODE_NO_PATH, error_msg)
        return file_path
