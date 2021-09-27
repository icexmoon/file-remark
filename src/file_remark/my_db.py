import sqlite3
import os
from sqlite3.dbapi2 import Connection, Cursor
from typing import Any

from file_remark.config import Config


class MyDB:
    '''数据库类（单例）'''
    DB_FILE_NAME = 'my_db.db'
    inited = False

    def __new__(cls) -> Any:
        if not hasattr(cls, "__instance"):
            setattr(cls, "__instance", super().__new__(cls))
        return getattr(cls, "__instance")

    def __init__(self) -> None:
        if not MyDB.inited:
            self.init_db()
            db_file = self.get_db_file()
            self.conn: Connection = sqlite3.connect(db_file)  # 数据库连接
            # self.cursor: Cursor = self.conn.cursor()  # 游标
            def dict_factory(cursor, row):  
                d = {}  
                for idx, col in enumerate(cursor.description):  
                    d[col[0]] = row[idx]  
                return d
            self.conn.row_factory = dict_factory
            MyDB.inited = True

    def get_db_file(self) -> str:
        '''获取数据库文件路径
        return 数据库文件路径
        '''
        config: Config = Config()
        db_file = config.get_path_split().join(
            (config.get_data_dir(), MyDB.DB_FILE_NAME))
        return db_file

    def init_db(self) -> None:
        '''如果数据库文件不存在，初始化数据库文件'''
        db_file = self.get_db_file()
        if not os.path.exists(db_file):
            # open(db_file, 'a').close()
            conn = sqlite3.connect(db_file)
            sql = '''
            CREATE TABLE [files](
            [name] VARCHAR(300) NOT NULL, 
            [path] VARCHAR(2000) NOT NULL UNIQUE, 
            [remark] VARCHAR(255) NOT NULL, 
            [add_time] DATETIME NOT NULL, 
            [modify_time] DATETIME NOT NULL);
            '''
            conn.execute(sql)
            conn.commit()
            conn.close()

    def execute(self, sql: str) -> None:
        self.conn.execute(sql)
        self.conn.commit()

    def query(self, sql: str) -> list:
        cursor: Cursor = self.conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        return result

    def query_one(self, sql: str) -> list:
        '''仅查询一条数据'''
        cursor: Cursor = self.conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        return result

    def __del__(self):
        '''数据库对象注销时断开连接'''
        self.conn.close()
        super().__del__()
