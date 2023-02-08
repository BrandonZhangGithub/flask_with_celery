from .. import xyzq
from .views import CheckSensitiveWords, CheckSeparationWall, CheckIfCallBack, FrontendMenu

xyzq.add_resource(FrontendMenu, "/frontend/menu") # 转发获取所有菜单配置
xyzq.add_resource(CheckSensitiveWords, "/check_sensitive_words") # 敏感词检测
xyzq.add_resource(CheckSeparationWall, "/check_separation_wall")  # 隔离墙检测
xyzq.add_resource(CheckIfCallBack, "/check_call_back")  # 判断是否可以撤回
