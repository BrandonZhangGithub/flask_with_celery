PROJECT_NAME = 'xyzq'
JWT_SECRET_KEY = "cuAihCz53DZRjZwbsGcZJ2Ai6At+T142uphtJMsk7iQ="
CURRENT_ENV = 'XYZQ_TEST'  # XYZQ_TEST 、 XYZQ_PRODUCT

# celery
BROKER = 'redis://czt-redis:6379/2'
BACKEND = 'redis://czt-redis:6379/3'

# ~~~~~研报系统相关
# 服务器IP+PORT
CZT_IP_PORT = 'http://10.86.0.65:15494'
# 研报主页
HOME_PAGE = '/#/research-report/record/audit?page=1'
# web_api
API_HOST_IP = 'http://czt-web-api:10001'
# 登录
API_LOGIN =  '/user/login'
# 上传文件
API_UPLOAD_FILE = '/research_report_audit/file/upload'
# 创建任务
CREATE_TASK = '/research_report_audit/task'
# 更新任务文件
UPDATE_TASK = '/research_report_audit/task/update'
# 查看卡片信息
SHOW_CARDS = '/research_report_audit/audit/text/basic'
# 任务流->撤回任务
FOR_CALL_BACK = '/research_report_audit/task/workflow'
# 查看任务详情
QUERY_TASK_NAME = '/research_report_audit/task/edit?task_id={}'
# 修改任务详情
EDIT_TASK_NAME = '/research_report_audit/task/edit'


# dg_oauth
DG_OAUTH_HOST = 'http://czt-dg-oauth:8080'
DG_SECRET_KEY = '64923f50a698486bb2b9644ff916eb6d'  # 内部请求dg_oauth的密钥
CREATE_USER = '/internal/user/create_all'  # 创建用户信息(访问dg_oauth)
GET_USER_BY_USERNAME = '/internal/user/list_by_name'
UPDATE_USER = '/user/item/'
SecretKey = "jkl;POIU1234++==" # AES
TIME_RE = '(\d{4})[^0-9]*(\d{,2})[^0-9]*(\d{,2})' # 匹配时间
UPDATE_DAYS = 7 # 定时任务更新投研平台用户回溯时间

# ~~~投研平台相关
# 投研平台测试环境
TYPT_HOST_PORT = 'http://192.20.103.97:8080'
# 投研平台域名
TYPT_DOMAIN_NAME = 'http://192.20.103.97:8080'
#home_page
TYPT_HOST_PAGE = '/anaplatform/#my.AffairsMgr'
# token有效时间判断
TYPT_TOKEN_EXPIRED_MINUTES = 100
# 静态文件夹路径
STATIC_DIR = '/czt_web_api/app/upload'
# 获取投研平台任务详情接口 post
TASK_DETAIL = '/mobileDoc.do?detail'
# 自审开启工作流
START_PROCESS = '/mobileDaguan.do?startProcess'
# 审核通过
APPROVE_PROCESS = '/mobileDoc.do?approval'
# 撤回
WITHDRAW_PROCESS = '/mobileDoc.do?withdrawn'
# 公司类隔离墙检测
COMPANY_SEPARATION_WALL = '/mobileCheck.do?separationWall'
# 非公司类隔离墙检测
NO_COMPANY_SEPARATION_WALL = '/mobileCheck.do?noCompanySeparationWall'
# 敏感词检测
SENSITIVE_WORDS = '/mobileCheck.do?sensitiveWords'
# 获取审核进度
REVIEW_DETAILS = '/mobileDaguan.do?getDocReviewDetails'
# 股票检测
CHECK_STOCK = '/mobileStock.do?search'
# 用户同步
SYNC_USERS = '/mobileDaguan.do?userSync'
# 导出水印文件
EXPORT_WATER_MARK = '/anaplatform/docType.do?action=watermarkReport&attachId={}&userId={}'
# 管理员id
ADMIN_EMPLOYEE_ID = '1111'

# 文档等级映射
DOC_LEVEL_MAPPER = {
    0: "无星级",
    1: "☆",
    2: "☆☆",
    3: "☆☆☆",
    4: "☆☆☆☆",
    5: "☆☆☆☆☆",
}
DOC_LEVEL_MAPPER_REVERSED = {
    "无星级": '0',
    "☆": '1',
    "☆☆": '2',
    "☆☆☆": '3',
    "☆☆☆☆": '4',
    "☆☆☆☆☆": '5',
}
# 文档密级映射
DOC_SECRET_LEVEL_MAPPER = {
    1: "非商密",
    2: "普通商密",
    3: "中级商密",
    4: "内部",
    5: "高级商密",
}
DOC_SECRET_LEVEL_MAPPER_REVERSED = {
    "非商密":1,
    "普通商密":2,
    "中级商密":3,
    "内部":4,
    "高级商密":5,
}
# 隔离墙检测公司类状态 mapper
COMPANY_SEPARATION_MAPPER = {
    "通过": "0",
    "不通过": "1",
    "可疑": "2",
    "检测中": "3",
    "后台错误": "-1"
}
# 需要打分的阶段/可以看分的阶段
NEED_POINTS = ['预审核', '合规终审核', '质量终审核']
# 领导审批阶段
LEADER_STAGE = '领导审核'
# 报告编写阶段
WRITING_STAGE = '报告编写'