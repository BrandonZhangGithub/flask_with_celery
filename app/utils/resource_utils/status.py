class TaskWorkflowRequestStatus:
    NEXT = 0  # 审核通过
    BACK = -1  # 退回任务
    COMPLETE = 1  # 任务完成