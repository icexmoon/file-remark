class UserException (Exception):
    CODE_NO_PATH = 1  # 文件或目录不存在

    def __init__(self, errorCode: int, errorMsg: str = ""):
        super().__init__()
        self.errorCode = errorCode
        self.errorMsg = errorMsg

    def getErrorCode(self):
        return self.errorCode

    def getErrorMsg(self):
        return self.errorMsg
