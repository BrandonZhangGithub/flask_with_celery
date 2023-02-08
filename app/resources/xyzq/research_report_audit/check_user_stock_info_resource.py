# coding=utf-8
from configs.base import *
from utils.response import RF
from .. import xyzq
from flask.views import MethodView
from schemas.ideas_schema import TextBasicSchema
from utils.resource_utils.utils import InterfaceForwardServices
from models.research_report_time_model import research_report_time_model
from models.check_user_stock_info_model import check_user_stock_info_model
from utils.resource_utils.utils import ConnectTypt, ConnectInner, ConnectDgauth

class CheckUserStockInfo(MethodView):

    @xyzq.arguments(TextBasicSchema, as_kwargs=True, location="query")
    def get(self, file_id):
        response_json = InterfaceForwardServices().forward(API_HOST_IP+ SHOW_CARDS)
        if response_json['status'] == 200:
            for item in response_json['data']['items']:
                if item['second_result_type'] == 1: # 股票
                    item = self.check_stock(item)
                elif item['second_result_type'] == 2: # 分析师
                    item = self.check_user(item)
                elif item['second_result_type'] == 3: # 时间
                    item = self.get_date(file_id, item)

            response_json['data']['items'].sort(key=lambda x:x.get('has_cross', 0), reverse=True)
        return response_json

    def check_stock(self, stock_item):
        searched_stock_name = ''
        if 'stock_code' in stock_item and stock_item['stock_code']['value']:
            stock_code = stock_item['stock_code']['value']
            searched_stock_name = ConnectTypt().check_stock(stock_code)
            if searched_stock_name:
                pass
            else:
                stock_item['stock_code']['cross'] = 1
                stock_item['has_cross'] = 1
        if 'stock_name' in stock_item and stock_item['stock_name']['value']:
            stock_name = stock_item['stock_name']['value']
            if searched_stock_name:
                if searched_stock_name == stock_item['stock_name']['value']:
                    pass
                else:
                    stock_item['stock_name']['cross'] = 1
                    stock_item['has_cross'] = 1
            else:
                searched_stock_code = ConnectTypt().check_stock(stock_name)
                if searched_stock_code:
                    pass
                else:
                    stock_item['stock_name']['cross'] = 1
                    stock_item['has_cross'] = 1
        return stock_item

    # 验证姓名、证书、邮箱
    def check_user(self, user_item):
        searched_user_by_email = None
        searched_user_by_license = None
        if 'email' in user_item and user_item['email']['value']:
            email = user_item['email']['value']
            user_by_email = check_user_stock_info_model.query_by_email(email)
            if user_by_email:
                searched_user_by_email = user_by_email
            else:
                user_item['email']['cross'] = 1
                user_item['has_cross'] = 1
        if 'cn_license' in user_item and user_item['cn_license']['value']:
            cn_license = user_item['cn_license']['value']
            if searched_user_by_email:
                if cn_license == searched_user_by_email.certificate:
                    pass
                else:
                    user_item['cn_license']['cross'] = 1
                    user_item['has_cross'] = 1
            else:
                user_by_license = check_user_stock_info_model.query_by_cn_license(cn_license)
                if user_by_license:
                    searched_user_by_license = user_by_license
                else:
                    user_item['cn_license']['cross'] = 1
                    user_item['has_cross'] = 1

        last_user = searched_user_by_email or searched_user_by_license
        if 'name' in user_item and user_item['name']['value']:
            name =  user_item['name']['value']
            if last_user:
                if name == last_user.nickname:
                    pass
                else:
                    user_item['name']['cross'] = 1
                    user_item['has_cross'] = 1
            else:
                user_by_name = check_user_stock_info_model.query_by_name(name)
                if user_by_name:
                    pass
                else:
                    user_item['name']['cross'] = 1
                    user_item['has_cross'] = 1
        return user_item

    def get_date(self, file_id, item):
        date = research_report_time_model.get_remark_date(file_id)
        item['report_date']['post_process_value'] = date if date else ''
        return item