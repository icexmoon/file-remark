import sqlite3
import os
from sqlite3.dbapi2 import Connection, Cursor
from typing import Any

from file_remark.config import Config
from file_remark.user_exception import UserException


class MyDB:
    '''数据库类（单例）'''
    DB_FILE_NAME = 'my_db.db'
    CURRENT_DB_VERSION = 3
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
            def dict_factory(cursor, row):
                d = {}
                for idx, col in enumerate(cursor.description):
                    d[col[0]] = row[idx]
                return d
            self.conn.row_factory = dict_factory
            # 将数据库中的配置数据写入config对象
            self.__load_config_from_db()
            self.__update_db()
            MyDB.inited = True

    def get_db_file(self) -> str:
        '''获取数据库文件路径
        return 数据库文件路径
        '''
        return MyDB.get_db_file()

    @classmethod
    def get_db_file(cls):
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
            conn = sqlite3.connect(db_file)
            sql = self.__get_sql('files')
            conn.execute(sql)
            sql = self.__get_sql('config')
            conn.execute(sql)
            sql = self.__get_sql('config_data')
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

    def reset_db(self):
        '''初始化数据库'''
        self.conn.close()
        db_file = self.get_db_file()
        os.remove(db_file)
        MyDB.inited=False
        self.__init__()

    def __del__(self):
        '''数据库对象注销时断开连接'''
        self.conn.close()
        super().__del__()

    def __get_sql(self, file_name: str) -> str:
        '''从sql文件获取sql
        file_name: sql文件名
        return sql内容
        '''
        config: Config = Config()
        sql_dir = config.get_sql_dir()
        sql_file = sql_dir+config.get_path_split()+file_name+'.sql'
        if not os.path.exists(sql_file):
            error_msg = "文件或目录{}不存在".format(sql_file)
            raise UserException(UserException.CODE_NO_PATH, error_msg)
        sql_content = ''
        with open(sql_file, 'r', encoding='UTF-8') as fopen:
            sql_content = fopen.read()
        return sql_content

    def __get_multi_sqls(self, file_name: str) -> list[str]:
        '''从sql文件读取多条sql(以;分隔)
        file_name: sql文件名
        return 多条sql
        '''
        sql_content = self.__get_sql(file_name)
        sqls = sql_content.split(';')
        return sqls

    def __load_config_from_db(self) -> None:
        '''从数据库加载配置数据到config对象'''
        config: Config = Config()
        sql = 'SELECT * FROM config;'
        db_configs = self.query(sql)
        for db_config in db_configs:
            config.set_db_config(db_config['name'], db_config['value'])

    def __update_db(self):
        '''更新数据库'''
        config:Config = Config()
        db_version = int(config.db_config['db_version'])
        if db_version == 2:
            sqls = self.__get_multi_sqls('v3')
            for sql in sqls:
                self.execute(sql)
            # 重新加载数据库配置
            self.__load_config_from_db()
        # 验证更新后数据库版本是否已经是当前的版本
        db_version = int(config.db_config['db_version'])
        if db_version != MyDB.CURRENT_DB_VERSION:
            raise UserException(UserException.CODE_DB, "数据库版本是当前最新版本，请尝试重置数据库。")
    
            
