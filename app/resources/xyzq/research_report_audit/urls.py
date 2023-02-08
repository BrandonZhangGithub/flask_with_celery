from .. import xyzq
from .task_transfer_resource import TaskTransfer
from .task_detail_transfer_resource import TaskDetailTransfer
from .task_workflow_transfer_resource import TaskWorkflowTransfer
from .task_one_transfer_resource import TaskOneTransfer
from .task_workflow_info_resource import TaskWorkflowInfo
from .task_comment_info_resource import TaskCommentInfo
from .task_time_info_resource import TaskTimetInfo
from .export_research_report_resource import ExportResearchReport
from .delete_research_report_resource import DeleteResearchReport
from .redirect_task_detail_resource import RedirectTaskDetailResource
from .check_user_stock_info_resource import CheckUserStockInfo
from .research_report_time_resource import ResearchReportTime

xyzq.add_resource(TaskWorkflowTransfer, "/research_report_audit/task/workflow") # 添加审核任务获取时间到research_report_audit_task表-审核退回等转发
xyzq.add_resource(TaskTransfer, "/research_report_audit/task") # 查看用户的审核任务获取时间-转发
xyzq.add_resource(TaskDetailTransfer, "/research_report_audit/task/detail") # 文件列表页 主要增加task_info（jump_url、jump_token）-转发
xyzq.add_resource(TaskOneTransfer, "/research_report_audit/task/one") # 单个任务详情-增加审核任务基本信息（关键词等）-转发
xyzq.add_resource(TaskWorkflowInfo, "/task_workflow_info") # 查看审核进度-定制化
xyzq.add_resource(TaskCommentInfo, "/task_comment_info") # 查看该任务当前操作人应有的评论信息+following_operator_ids-定制化
xyzq.add_resource(CheckUserStockInfo, "/research_report_audit/audit/text/basic") # 转发请求，校验卡片结果
xyzq.add_resource(TaskTimetInfo, "/task_time_info") # 最后的时间校验-定制化
xyzq.add_resource(ExportResearchReport, "/export_research_report") # 导出研报
xyzq.add_resource(DeleteResearchReport, "/deleteResearchReport") # 删除研报任务
xyzq.add_resource(RedirectTaskDetailResource, "/redirectTaskDetail") # 重定向到任务详情页
xyzq.add_resource(ResearchReportTime, "/research_report_audit/research_report_time")  #对于研报后处理结果的增删改
