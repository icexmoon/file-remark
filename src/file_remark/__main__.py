import getopt
from os import path
import sys
from .main import Main
from .config import Config
from .my_db import MyDB
from .user_exception import UserException
def getOptionVal(options, key, key2):
    for optKey, optVal in options:
        if optKey == key or optKey == key2:
            return optVal
    return None

def main():
    pass
    try:
        opts, args=getopt.gnu_getopt(sys.argv[1:],
                            'ahf:r:lovmd',
                            ['help','add','modify','delete','delete_all','file=','remark=','remark_first','remark_last','only_remark','version','init_process','all'])
    except getopt.GetoptError as e:
        print("获取参数信息出错，错误提示：", e.msg)
        return
    main_process = Main()
    file_path = getOptionVal(opts, '-f', '--file')
    remark = getOptionVal(opts, '-r', '--remark')
    for opt in opts:
        argKey = opt[0]
        argVal = opt[1]
        if argKey == '-a' or argKey == '--add':
            main_process.add_remark(file_path, remark)
            return
        elif argKey == '-h' or argKey == '--help':
            main_process.print_help()
            return
        elif argKey == '--remark_first':
            main_process.set_print_mode(Config.PRINT_REMARK_FIRST)
        elif argKey == '--remark_last' or argKey=='-l':
            main_process.set_print_mode(Config.PRINT_REMARK_LAST)
        elif argKey == '--only_remark' or argKey=='-o':
            main_process.set_print_mode(Config.PRINT_ONLY_REMARK)
        elif argKey == '--version' or argKey == '-v':
            main_process.print_version()
            return
        elif argKey == '--init_process':
            main_process.init_process()
            return
        elif argKey == '--all':
            main_process.list_all()
            return
        elif argKey == '--modify' or argKey == '-m':
            main_process.modify_remark(file_path, remark)
            return
        elif argKey == '--delete' or argKey == '-d':
            main_process.remove_remark(file_path)
            return
        elif argKey == '--delete_all':
            main_process.remove_all()
            return
        else:
            pass
    main_process.list_remarks()
try:
    main()
except UserException as e:
    UserException.dealUserException(e)
exit()