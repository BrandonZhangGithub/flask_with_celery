from .. import xyzq
from .views import DraftFileName, AllUserInfo

xyzq.add_resource(DraftFileName, "/inner_call/get_filename_by_id")  #  内部调用，查询底稿原文件名
xyzq.add_resource(AllUserInfo, "/inner_call/get_all_user_info")  #  内部调用，查询当前所有生效用户信息