from financial_beans.enum.research_report_audit.research_report_audit_task_status import ResearchReportAuditTaskStatus

# 研报任务状态
class XYZQTaskWorkflowRequestStatus(ResearchReportAuditTaskStatus):
    # 已撤回
    CALL_BACK = 10

XYZQ_TaskWorkflowRequestStatus = XYZQTaskWorkflowRequestStatus()

class TyptResponseStatusEnum():
    SUCCESS = 1

# 9,已经取消文档 5 撤回文档；1 已通过文档；2 未审批文档；3 已删除文档；0 流转中文档，工作流已开启;4合规接口未通过 6:文档特权删除 7:草稿箱  8:邮件接收有相同的报告
class TyptTaskStatusEnum():
    IN_FLOW = 0
    CALL_BACK = 5
    IN_BOX = 7
