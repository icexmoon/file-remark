import getopt
import sys
from .main import Main
from .config import Config
def getOptionVal(options, key, key2):
    for optKey, optVal in options:
        if optKey == key or optKey == key2:
            return optVal
    return None

def main():
    pass
    try:
        opts, args=getopt.gnu_getopt(sys.argv[1:],
                            'ahf:r:lo',
                            ['help','add','file=','remark=','remark_first','remark_last','only_remark'])
    except getopt.GetoptError as e:
        print("获取参数信息出错，错误提示：", e.msg)
        return
    main_process = Main()
    # if not opts:
    #     main_process.list_remarks()
    for opt in opts:
        argKey = opt[0]
        argVal = opt[1]
        if argKey == '-a' or argKey == '--add':
            file_path = getOptionVal(opts, '-f', '--file')
            if file_path is None:
                print('必须指定文件才能添加备注！')
                return
            remark = getOptionVal(opts, '-r', '--remark')
            if remark is None:
                print('缺少备注信息！')
                return
            main_process.add_remark(file_path, remark)
        elif argKey == '-h' or argKey == '--help':
            main_process.print_help()
            return
        elif argKey == '--remark_first':
            main_process.set_print_mode(Config.PRINT_REMARK_FIRST)
        elif argKey == '--remark_last' or argKey=='-l':
            main_process.set_print_mode(Config.PRINT_REMARK_LAST)
        elif argKey == '--only_remark' or argKey=='-o':
            main_process.set_print_mode(Config.PRINT_ONLY_REMARK)
    main_process.list_remarks()

main()
exit()