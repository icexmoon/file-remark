class UserException (Exception):
    CODE_NO_PATH = 1  # 文件或目录不存在
    CODE_DB = 2  # 数据库错误
    CODE_NO_REMARK = 3 # 备注信息不存在
    CODE_NO_PARAM = 4 # 缺少参数

    def __init__(self, errorCode: int, errorMsg: str = ""):
        super().__init__()
        self.errorCode = errorCode
        self.errorMsg = errorMsg

    def getErrorCode(self):
        return self.errorCode

    def getErrorMsg(self):
        return self.errorMsg

    @classmethod
    def dealUserException(cls, exp: 'UserException') -> None:
        print('程序错误，错误码[{}]，错误信息：{}'.format(
            exp.getErrorCode(), exp.getErrorMsg()))
