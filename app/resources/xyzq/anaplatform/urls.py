from .. import xyzq
from .create_task_resource import CreateTask
from .jump_datgrand_home_resource import JumpDatagrandHome
from .sync_users_first_resource import SyncUsersFirst
from .sync_call_back_resource import SyncCallBack
from .init_customized_tables_resource import InitCustomizedTables

xyzq.add_resource(CreateTask, "/create_task")   # 创建任务
xyzq.add_resource(JumpDatagrandHome, "/jump_datagrand_home") # 跳转到达观智能审核主页
xyzq.add_resource(SyncCallBack, "/sync_call_back")  # 同步达观智能审核的撤回
xyzq.add_resource(SyncUsersFirst, "/sync_users_first") # 首次同步用户
xyzq.add_resource(InitCustomizedTables, "/init_customized_tables") # 首次同步用户
