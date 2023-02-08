import random

import requests, json, time
from initialization.redis_process import redis_cli
from initialization.logger_process import logger
from configs.base import *
from flask import request
from utils.resource_utils.exceptions import InterfaceForwardException
import jwt
from utils.resource_utils.aes_encrypt import aes_encryption

# 投研平台连接
class ConnectTypt():
    def __init__(self, user_id=None):
        self.user_id = user_id if user_id else jwt.decode(
                request.headers.environ.get('HTTP_AUTHORIZATION').split(' ')[-1], verify=False, algorithms="HS256"
            )['username']

    def get_user_token(self):
        # token_time_cache = redis_cli.get(self.user_id)
        # if token_time_cache:
        #     token_cache, time_cache = token_time_cache.decode().split('&')
        #     if (time.time() - int(time_cache))//60 > TYPT_TOKEN_EXPIRED_MINUTES:
        #         token, timestamp = self.request_user_token()
        #         redis_cli.set(self.user_id, token+'&'+timestamp)
        #         return token
        #     else:
        #         return token_cache
        # else:
            token, timestamp = self.request_user_token()
            # redis_cli.set(self.user_id, token+'&'+timestamp)
            return token

    def request_user_token(self):
        if CURRENT_ENV == 'SAAS':
            return 'D19E1B006D882754C902D51E1D9979F3AB5B7CB2EE53171BE442B447A1964663203318ECCD0CCBD38AF7294A4883831E', str(int(time.time()))
        else:
            token_url = TYPT_HOST_PORT + '/token.do'
            payload = json.dumps({
                "body" : {
                "userId" : self.user_id,
                "deviceNo": "datagrand"
            }}
            )
            headers = {
                'Content-Type' : 'application/json'
            }
            logger.info('获取投研平台token url：{},payload:{}'.format(token_url, payload))
            response = requests.request("POST", token_url, headers=headers, data=payload)
            logger.info('获取投研平台token response：{}'.format(json.dumps(response.json(), ensure_ascii=False)))
            token = response.json().get('json', {}).get('token', '')
            timestamp = str(response.json().get('json', {}).get('timestamp', ''))
            return token, timestamp

    def query_work_flow_info(self, docId):
        url = TYPT_HOST_PORT + REVIEW_DETAILS
        payload = json.dumps({
            "token": self.get_user_token(),
            "body": {
                "docId": docId,
                "userId": self.user_id
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=CA2285775CB3F4E3D5904724E8144A0C'
        }
        logger.info('获取投研平台commentsList url：{},payload:{}'.format(url, payload))
        response = requests.request("POST", url, headers=headers, data=payload)
        logger.info('获取投研平台commentsList response：{}'.format(json.dumps(response.json(), ensure_ascii=False)))
        return response.json().get('json', {}).get('commentsList', {})

    def query_task_comment_info(self, doc_id):
        result = {
            'compliance_review': [],
            'quality_review': [],
            'error_review': [],
            'stage_info': {
                'following_operator_name': [],
                'following_operator_ids': [],
                'following_stage': '',
                'current_stage': ''
            },
            'leader_stage_info': {
                'leader_operator_name': [],
                'leader_operator_ids': [],
                'leader_following_stage': ''
            },
            'opinion_review': 'default',
            'send_message': 'default'
        }
        task_detail = self.get_task_detail(doc_id)


        ### stage_info
        submitUser = task_detail.get('submitUser', [])

        #  查看是否为领导审批
        LEADER_APPROVE = False
        for user in submitUser:
            if user['nextTransName'] == LEADER_STAGE:
                LEADER_APPROVE = True

        if LEADER_APPROVE:
            leader_stage_info = {
                'leader_operator_name': [user['name'] for user in submitUser],
                'leader_operator_ids': [ConnectDgauth().get_user_by_username(user['employeeId']).get('userId') for user in submitUser],
                'leader_following_stage': LEADER_STAGE
            }
            result['leader_stage_info'] = leader_stage_info
            result['stage_info']['current_stage'] = task_detail.get('currentStage', '') # 设置当前审批阶段
        else:
            following_operator_name = [user['name'] for user in submitUser]
            following_operator_ids = [ConnectDgauth().get_user_by_username(user['employeeId']).get('userId') for user in submitUser]
            if submitUser:
                following_stage = [user['nextTransName'] for user in submitUser][0]
            else:
                following_stage = ""
            stage_info = {
                'following_operator_name': following_operator_name,
                'following_operator_ids': following_operator_ids,
                'following_stage': following_stage,
                'current_stage': task_detail.get('currentStage', '') # 设置当前审批阶段
            }
            result['stage_info'] = stage_info

        ### compliance_review 与 quality_review
        if task_detail.get('currentStage') != WRITING_STAGE:
            if task_detail.get('isCompliance', 0) == 0:
                reportQualityOptions = task_detail.get('reportQualityOptions', [])
                result['quality_review'] = [{"name": reportQualityOption.get("content"), "id": reportQualityOption.get("id")} for reportQualityOption in reportQualityOptions]
            else:
                complianceRecordInfos = task_detail.get('complianceRecordInfos', [])
                result['compliance_review'] = [{"name": complianceRecordInfo.get("content"), "id": complianceRecordInfo.get("id")} for complianceRecordInfo in complianceRecordInfos]

        ###  error_review
        if task_detail.get('currentStage') in NEED_POINTS:
            result["error_review"]= {
                "oneErr": 0,
                "twoErr": 0,
                "otherErr": 0,
                "totalErr": 0
            }
        # opinion_review

        # 自审阶段不展示评论
        if task_detail.get('currentStage') == WRITING_STAGE:
            result["opinion_review"] = ''
        else:
            result["opinion_review"] = 'default'
        # send_message
        result["send_message"] = 'default'
        return result

    def get_task_detail(self, docId):
        url = TYPT_HOST_PORT + TASK_DETAIL
        payload = json.dumps({
            "token": self.get_user_token(),
            "body": {
                "docId": docId,
                "userId": self.user_id,
                "isRelation": 0
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=A72B5E2BD6AADB9CFC0DF7E2A182D59D'
        }
        logger.info('获取投研平台task_detail url：{},payload:{}'.format(url, payload))
        response = requests.request("POST", url, headers=headers, data=payload)
        logger.info('获取投研平台task_detail response：{}'.format(json.dumps(response.json(), ensure_ascii=False)))
        return response.json().get('json', {}).get('document', {})

    def send_start_process_request(self, docId, customized):
        task_detail = self.get_task_detail(docId)
        if task_detail.get('dyStockcode'): # 查看是否为公司类报告，映射chack_stock
            customized['check_stock'] = COMPANY_SEPARATION_MAPPER.get(customized['check_stock'])

        url = TYPT_HOST_PORT + START_PROCESS
        payload = json.dumps({
            "token": self.get_user_token(),
            "body": {
                "docId": docId,
                "employeeId": self.user_id,
                "processInstanceId": self.get_task_detail(docId).get('processInstanceId'),
                "separationWallstock": customized.get('check_stock'),
                "comment": "无问题"
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=A72B5E2BD6AADB9CFC0DF7E2A182D59D'
        }
        logger.info('开启流程，url: {},payload: {}'.format(url, payload))
        response = requests.request("POST", url, headers=headers, data=payload)
        logger.info('开启流程response:{}'.format(json.dumps(response.json(), ensure_ascii=False)))
        return response.json()

    def send_next_process_request(self, docId, customized):

        task_detail = self.get_task_detail(docId)

        if task_detail.get('dyStockcode'): # 查看是否为公司类报告，映射chack_stock
            customized['check_stock'] = COMPANY_SEPARATION_MAPPER.get(customized['check_stock'])

        url = TYPT_HOST_PORT + APPROVE_PROCESS

        if 'error_review' in customized:  # 判断是否有error评论
            payload = json.dumps({
                "token": self.get_user_token(),
                "body": {
                    "docId": docId,
                    "opinion": customized.get('opinion_review', ''),
                    "status": customized.get('status'),
                    "SMSReminders": customized.get('send_message', 1),
                    "processInstanceId": task_detail.get('processInstanceId'),
                    "taskInstanceId": task_detail.get('taskInstanceId'),
                    "userId": self.user_id,
                    "docLevel": DOC_LEVEL_MAPPER_REVERSED.get(customized.get('doc_level')),
                    "docSecretLevel": DOC_SECRET_LEVEL_MAPPER_REVERSED.get(customized.get('doc_secret_level')),
                    "qualityApprove": customized.get('quality_review', []),
                    "complianceRecord": customized.get('complianceRecord', []),
                    "checkStock": customized.get('check_stock', ""),
                    'oneErr': customized.get('error_review', {}).get('oneErr', 0),
                    'twoErr': customized.get('error_review', {}).get('twoErr', 0),
                    'otherErr': customized.get('error_review', {}).get('otherErr', 0),
                }
            })
        else:
            payload = json.dumps({
                "token": self.get_user_token(),
                "body": {
                    "docId": docId,
                    "opinion": customized.get('opinion_review', ''),
                    "status": customized.get('status'),
                    "SMSReminders": customized.get('send_message', 1),
                    "processInstanceId": task_detail.get('processInstanceId'),
                    "taskInstanceId": task_detail.get('taskInstanceId'),
                    "userId": self.user_id,
                    "docLevel": DOC_LEVEL_MAPPER_REVERSED.get(customized.get('doc_level')),
                    "docSecretLevel": DOC_SECRET_LEVEL_MAPPER_REVERSED.get(customized.get('doc_secret_level')),
                    "qualityApprove": customized.get('quality_review', []),
                    "complianceRecord": customized.get('complianceRecord', []),
                    "checkStock": customized.get('check_stock', ""),
                }
            })

        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=EDC40CDFECA7FB7732533BC47D681925'
        }
        logger.info('审核通过，url: {},payload: {}'.format(url, payload))
        response = requests.request("POST", url, headers=headers, data=payload)
        logger.info('审核通过response:{}'.format(json.dumps(response.json(), ensure_ascii=False)))
        return response.json()

    def send_back_process_request(self, docId):
        task_detail = self.get_task_detail(docId)

        url = TYPT_HOST_PORT + WITHDRAW_PROCESS
        payload = json.dumps({
            "token": self.get_user_token(),
            "body": {
                "processInstanceId": task_detail.get('processInstanceId'),
                "userId": self.user_id,
                "docId": docId
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=EDC40CDFECA7FB7732533BC47D681925'
        }
        logger.info('撤回 url: {},payload: {}'.format(url, payload))
        response = requests.request("POST", url, headers=headers, data=payload)
        logger.info('撤回 response:{}'.format(json.dumps(response.json(), ensure_ascii=False)))
        return response.json()

    # 敏感词检测
    def send_sensitive_check(self, docId):
        url = TYPT_HOST_PORT + SENSITIVE_WORDS

        payload = json.dumps({
            "token": self.get_user_token(),
            "body": {
                "docId": docId
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=1E4E99C817F6332051D0E88E5FC3FF81'
        }
        logger.info('敏感词 url: {},payload: {}'.format(url, payload))
        response = requests.request("POST", url, headers=headers, data=payload)
        logger.info('敏感词 response:{}'.format(json.dumps(response.json(), ensure_ascii=False)))
        return response.json().get('json', {})

    # 隔离墙检测
    def send_sepatation_check(self, docId):
        task_detail = self.get_task_detail(docId)

        # 根据是否有股票代码判断是否是公司类报告
        if task_detail.get('dyStockcode'):
            url = TYPT_HOST_PORT + COMPANY_SEPARATION_WALL
        else:
            url = TYPT_HOST_PORT + NO_COMPANY_SEPARATION_WALL

        payload = json.dumps({
            "token": self.get_user_token(),
            "body": {
                "docId": docId
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=1E4E99C817F6332051D0E88E5FC3FF81'
        }
        logger.info('隔离墙 url: {},payload: {}'.format(url, payload))
        response = requests.request("POST", url, headers=headers, data=payload)
        logger.info('隔离墙 response:{}'.format(json.dumps(response.json(), ensure_ascii=False)))
        return response.json().get('json', {})

    # 检测股票接口
    def check_stock(self, stock_name_or_id, GET_NAME=True):
        url = TYPT_HOST_PORT + CHECK_STOCK
        payload = json.dumps({
            "token": self.get_user_token(),
            "body": {
                "stock": stock_name_or_id,
                "pageSize": "1",
                "pageNo": "0"
            }
        })
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=334DA9D2D3D35F32659FA7541A368E72'
        }
        logger.info('检测股票 url: {},payload: {}'.format(url, payload))
        response = requests.request("POST", url, headers=headers, data=payload)
        logger.info('检测股票 response:{}'.format(json.dumps(response.json(), ensure_ascii=False)))
        search = response.json().get('json', {}).get('search', [])
        if search:
            if GET_NAME:
                return search[0]['stockName']
            else:
                return search[0]['stockCode']
        else:
            return False

    def get_one_task_info(self, docId):
        """
        title 标题
        keyWords 关键字
        author 作者
        emailAuthor 分析师
        operator 操作者
        dyCompany 股票名称
        dyStockcode 股票代码
        extractionMainPoints 是否提取要点 true->是
        summary 摘要
        investSuggestion 投资评级
        investSuggestionChange 投资评级改动
        industryId 内部行业
        docSecretLevel 文档密级 1,非商密、2,普通商密、3,中级商密、4,内部 、5,高级商密
        docLevel 文档等级 【0，1,2,3,4,5】 --> [无等级，☆，☆☆，☆☆☆，☆☆☆☆，☆☆☆☆☆]
        myStockList 预测分析
        isInStockpool 是否绿色金融 是、否
        industry 内部行业
        myStockList  EPS预测分析
        """

        task_detail = self.get_task_detail(docId)
        result = []
        if task_detail.get('title'):
            result.append({"标题": task_detail.get('title')})
        if task_detail.get('keyWords'):
            result.append({"关键字": task_detail.get('keyWords')})
        if task_detail.get('author'):
            result.append({"作者": task_detail.get('author')})
        if task_detail.get('emailAuthor'):
            result.append({"分析师": task_detail.get('emailAuthor')})
        if task_detail.get('operator'):
            result.append({"操作者": task_detail.get('operator')})
        result.append({"文档等级": DOC_LEVEL_MAPPER.get(task_detail.get('docLevel'), "")})
        if task_detail.get('docSecretLevel'):
            result.append({"文档密级": task_detail.get('docSecretLevel')})
        if task_detail.get('summary'):
            result.append({"摘要": task_detail.get('summary')})
        if task_detail.get('dyCompany'):
            result.append({"股票名称": task_detail.get('dyCompany')})
        if task_detail.get('dyStockcode'):
            result.append({"股票代码": task_detail.get('dyStockcode')})
        if task_detail.get('extractionMainPoints'):
            result.append({"是否提取要点": "是" if task_detail.get('extractionMainPoints') == 'true' else "否"})
        if task_detail.get('isInStockpool'):
            result.append({"是否绿色金融": task_detail.get('isInStockpool')})
        if task_detail.get('industry'):
            result.append({"内部行业": task_detail.get('industry')})
        if task_detail.get('myStockList'):
            myStockList_result = ''
            myStockList = task_detail.get('myStockList')
            myStockList.sort(key=lambda x:x['year'])
            for myStock in myStockList:
                myStock["eps"] = str(myStock['eps']) + '元'
                myStock["year"] = str(myStock['year']) + '年'
            myStockList_result = ';'.join([item['year'] + ':' + item['eps'] for item in myStockList])
            result.append({"预测分析": myStockList_result})
        return result

# 财报内部链接 username=employee_id
class ConnectInner():
    def __init__(self, user_id=None):
        self.user_id = user_id if user_id else jwt.decode(
            request.headers.environ.get('HTTP_AUTHORIZATION').split(' ')[-1], verify=False, algorithms="HS256"
        )['username']

    def get_user_token(self):
        # token_time_cache = redis_cli.get(self.user_id)
        # if token_time_cache:
        #     token_cache, time_cache = token_time_cache.decode().split('&')
        #     if (time.time() - int(time_cache))//60 > TYPT_TOKEN_EXPIRED_MINUTES:
        #         token, timestamp = self.request_user_token()
        #         redis_cli.set(self.user_id, token+'&'+timestamp)
        #         return token
        #     else:
        #         return token_cache
        # else:
        #     token, timestamp = self.request_user_token()
        #     redis_cli.set(self.user_id, token+'&'+timestamp)
        #     return token
        return self.request_user_token()

    def request_user_token(self):
        token_url = DG_OAUTH_HOST + API_LOGIN

        if self.user_id == 1:
            username = 'admin'
            password = '2Jt6@jKk'
        else:
            username = str(self.user_id)
            password = '2wsx!QAZ'

        payload = json.dumps({
            "username": aes_encryption(username),
            "password": aes_encryption(password),
            "code": "default"
        })
        headers = {
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=D2A08BABC01930778407C66C69796E3C'
        }
        logger.info('获取达观内部token url: {},payload: {}, username:{}'.format(token_url, payload, username))
        response = requests.request("POST", token_url, headers=headers, data=payload)
        logger.info('获取达观内部token response:{}'.format(json.dumps(response.json(), ensure_ascii=False)))
        return response.json().get('data').get('accessToken')

    def get_edit_user_ids(self, task_id):
        url = API_HOST_IP + QUERY_TASK_NAME.format(task_id)

        payload = {}
        headers = {
            'Authorization': 'Bearer {}'.format(self.get_user_token()),
            'Cookie': 'JSESSIONID=1BC8A4E4A2424F2DD6174A974C1F36D1'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        return [item['user_id'] for item in response.json().get('data', [])]

    def post_edit_task_name(self, task_id, file_name, user_ids):
        url = API_HOST_IP + EDIT_TASK_NAME

        payload = json.dumps({
            "task_id": str(task_id),
            "remark": "-",
            "user_ids": user_ids,
            "task_name": file_name
        })
        headers = {
            'Authorization': 'Bearer {}'.format(self.get_user_token()),
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()

# DG_OAUTH链接
class ConnectDgauth():
    def __init__(self, user_id=None):
        pass

    def get_user_by_username(self, username: str):
        """
        通过username从dg_oauth获取用户信息
        @param username:
        @return:
        """
        url = f'{DG_OAUTH_HOST}{GET_USER_BY_USERNAME}?username={username}'
        headers = dict(secret=DG_SECRET_KEY)
        response = requests.get(url, headers=headers, timeout=10)
        return response.json().get('data')

    def create_user(self, users: list):
        url = f'{DG_OAUTH_HOST}{CREATE_USER}'
        headers = dict(secret=DG_SECRET_KEY)
        response = requests.post(url, headers=headers, json=users, timeout=10)

    def update_user(self, users: list):
        user_id = users[0]['userId']
        url = DG_OAUTH_HOST + UPDATE_USER + str(user_id)

        headers = {
            'Authorization': 'Bearer {}'.format(ConnectInner(1).get_user_token()),
            'Content-Type': 'application/json',
            'Cookie': 'JSESSIONID=05E08E411B803F0FB1155F7B309222B2'
        }
        response = requests.post(url, headers=headers, json=users[0], timeout=10)

    def get_all_menu(self, appId):
        url = DG_OAUTH_HOST + '/frontend/menu?appId={}'.format(appId)
        payload = {}
        headers = {'Authorization': 'Bearer {}'.format(ConnectInner(1).get_user_token()),
                   'Cookie': 'JSESSIONID=974681ABB0BE9B904C50AB7C6E9171BE'}
        response = requests.request("GET", url, headers=headers, data=payload)
        return response.json()


# 转发
class InterfaceForwardServices:
    def forward(self, target_uri):
        try:
            data = request.form if request.form else json.dumps(request.json)

            # 任务完成 单独修改
            WORK_FLOW_URL = API_HOST_IP + '/research_report_audit/task/workflow'
            if target_uri == WORK_FLOW_URL and 'forward_to_user_ids' in request.json and not request.json['forward_to_user_ids']:
                    tmp_dict = request.json
                    tmp_dict['flow_status'] = 1
                    del tmp_dict['forward_to_user_ids']
                    data = json.dumps(tmp_dict)

            logger.info("开始进行接口转发，method: {} target_uri: {}".format(request.method, target_uri))
            headers = {"Authorization": request.headers.environ.get('HTTP_AUTHORIZATION'), "Content-Type": request.headers.environ.get('CONTENT_TYPE')}
            response = requests.request(request.method, target_uri, data=data, params=request.args,
                                        files=self.get_file_list(), headers=headers)
            return response.json()
        except Exception as e:
            logger.error("接口转发失败: {}".format(str(e)))
            raise InterfaceForwardException("转发目标服务器不可达！")

    def get_file_list(self, file_name='file'):
        """
        获取多个文件
        :return:
        """
        file_list = request.files.getlist(f'{file_name}')
        _list = []
        for file_obj in file_list:
            # 不知是否为bug,多文件上传时 总有那么一个文件名结尾添加了 " ,所以去掉
            origin_file_name = file_obj.filename
            if origin_file_name.endswith('"'):
                origin_file_name = origin_file_name[:-1]
            _list.append((file_name, (origin_file_name, file_obj.read(), file_obj.content_type)))
        return _list

