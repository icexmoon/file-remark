import os
import time


class Tools:
    @classmethod
    def get_abs_path(cls, path: str) -> str:
        '''获取一个绝对路径
        path 相对路径或绝对路径
        '''
        abs_path = os.path.abspath(path)
        return abs_path

    @classmethod
    def get_now_time_str(cls)->str:
        '''获取当前时间字符串'''
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
