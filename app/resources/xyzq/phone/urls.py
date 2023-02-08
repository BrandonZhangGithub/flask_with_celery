from .. import xyzq
from .views import PhoneNormalApprove, PhoneFinalApprove, PhoneReject

xyzq.add_resource(PhoneNormalApprove, "/PhoneNormalApprove") # 正常审批提交给接下来的人（包含领导审批）
xyzq.add_resource(PhoneFinalApprove, "/PhoneFinalApprove")  # 任务完成接口
xyzq.add_resource(PhoneReject, "/PhoneReject") # 退回任务