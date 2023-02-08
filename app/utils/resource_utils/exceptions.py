# 接口转发失败
class InterfaceForwardException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)