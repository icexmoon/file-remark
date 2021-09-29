import os
import time
from file_remark.my_db import MyDB


class MFiles:
    '''files表module'''
    TYPE_FILE = 1  # 文件
    TYPE_DIR = 2  # 目录
    FIELD_TYPE = 'type'

    def add_remark(self, file_path: str, remark: str):
        '''给文件添加备注'''
        db = MyDB()
        file_name = os.path.basename(file_path)
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        type = self.__get_type_by_path(file_path)
        sql = '''
        INSERT INTO files('name','path','remark','add_time','modify_time','type') 
        VALUES('{}','{}','{}','{}','{}','{}')
        '''.format(file_name, file_path, remark, now_time, now_time, type)
        db.execute(sql)

    def search_path(self, paths: list[str]) -> list:
        '''查询匹配到的path
        paths 需要查询的path列表
        return 匹配到的备注信息
        '''
        files = []
        for path in paths:
            file_info = self.get_file_remark(path)
            if file_info:
                files.append(file_info)
        return files

    def get_file_remark(self, path: str):
        '''获取指定路径的备注信息'''
        db = MyDB()
        sql = '''
        SELECT * FROM files
        WHERE path='{}' LIMIT 1;
        '''.format(path)
        file_info = db.query_one(sql)
        return file_info

    def is_in_file_remarks(self, path: str, file_remarks: list):
        '''指定的路径是否在file_remarks数据集中'''
        for file_remark in file_remarks:
            if path == file_remark['path']:
                return True
        return False

    def __get_type_by_path(self, path: str) -> int:
        '''根据给定路径获取类型
        path 路径
        return 类型
        '''
        if os.path.isfile(path):
            return MFiles.TYPE_FILE
        elif os.path.isdir(path):
            return MFiles.TYPE_DIR
        else:
            return MFiles.TYPE_FILE
