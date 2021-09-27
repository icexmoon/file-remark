import os
import time
from file_remark.my_db import MyDB
class MFiles:
    '''files表module'''
    def add_remark(self, file_path: str, remark: str):
        '''给文件添加备注'''
        db = MyDB()
        file_name = os.path.basename(file_path)
        now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        sql = '''
        INSERT INTO files('name','path','remark','add_time','modify_time') 
        VALUES('{}','{}','{}','{}','{}')
        '''.format(file_name, file_path, remark, now_time, now_time)
        db.execute(sql)

    def search_path(self, paths:list[str])->list:
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

    def is_in_file_remarks(self, path:str, file_remarks:list):
        '''指定的路径是否在file_remarks数据集中'''
        for file_remark in file_remarks:
            if path == file_remark['path']:
                return True
        return False



    