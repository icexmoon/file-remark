import sys

sys.path.insert(-2, "d:\\workspace\\python\\file-remark\\src")
# sys.path.insert(0, "/home/icexmoon/workspace/python/file-remark/src")
import os
from file_remark.main import Main
from file_remark.config import Config
from file_remark.user_exception import UserException
try:
    main = Main()
    # path = os.path.abspath(os.getcwd()+os.sep+'./aa.txt')
    # path = './e.txt'
    # main.add_remark(path, 'file cc.txt comment')
    # main.set_print_mode(Config.PRINT_REMARK_LAST)
    # main.print_help()
    main.print_version()
    # main.init_process()
    # main.modify_remark('./aa.txt','new file comment')
    # main.remove_remark('./aa.txt')
    main.remove_all()
    # main.list_remarks()
    # main.print_version()
    # main.list_all()
except UserException as e:
    UserException.dealUserException(e)