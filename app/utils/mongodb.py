import datetime
import pymongo
from bson import ObjectId


class MongodbException(Exception):
    def __init__(self, msg):
        self.msg = msg


class MongoManager(object):
    def __init__(self, uri, db, client=None):
        if client:
            self.client = client
        else:
            self.client = pymongo.MongoClient(uri, tz_aware=False, retryWrites=True)
        self.db = db

    def get_client(self):
        return self.client

    def check_connection_state(self):
        try:
            info = self.client["admin"].command("ping")
            if info.get("ok") == 1:
                return 1
            else:
                return 0
        except:
            return 0

    def get_collection(self, table):
        return self.client[self.db][table]

    def get_db(self):

        return self.client[self.db]

    def show_collections(self):
        """
        @attention: 获取所有集合名称
        """
        return self.get_db().collection_names()

    # 插入部分
    def single_insert(self, table, document):
        """
        @attention: 新增数据
        """
        con = self.get_collection(table)
        result = con.insert_one(document)
        return str(result.inserted_id)

    def mul_insert(self, table, documents, has_return=False):
        """
        @attention: 批量新增
        @return: 新增数据ID
        """
        if documents:
            con = self.get_collection(table)
            res = con.insert_many(documents)
            if has_return:
                return [str(item) for item in res]
            else:
                return None

    # 修改部分
    def update(self, table, query, update):
        """
        @attention: 修改
        """
        con = self.get_collection(table)
        data = {"$set": update}
        con.update_many(query, data)

    def cover(self, table, query, update):
        """
        @attention: 覆盖
        """
        con = self.get_collection(table)
        con.replace_one(query, update)

    def custom_update(self, table, query, update):
        """
        @attention: 自定义修改
        """
        con = self.get_collection(table)
        con.update_many(query, update)

    # 查询部分
    def get_page_list(self, table, mfilter, mfields=[], msort=[], page=1, page_size=20):
        """
        @attention: 列表查询(用于分页时的查询)，返回列表及总条数
        @warning: 请不要使用该函数进行统计，统计请直接使用底层模块来处理
        """
        con = self.get_collection(table)
        fields = {item: 1 for item in mfields}
        sorts = list(map(lambda x: (x[1:], -1) if "-" in x else (x, 1), msort))
        offset = (page - 1) * page_size
        if fields:
            cursor = con.find(mfilter, fields).skip(offset).limit(page_size)
        else:
            cursor = con.find(mfilter).skip(offset).limit(page_size)

        if sorts:
            cursor = cursor.sort(sorts)

        res = []
        for document in cursor:
            document["_id"] = str(document["_id"])
            res.append(document)
        return res

    def get_page_list_full_key(
        self, table, mfilter, mfields=[], msort=[], page=1, page_size=20
    ):
        """
        @attention: 列表查询(用于分页时的查询)，返回列表,如果查询key不存在,则用空填补
        @warning: 请不要使用该函数进行统计，统计请直接使用底层模块来处理
        """
        con = self.get_collection(table)
        fields = {item: 1 for item in mfields}
        sorts = list(map(lambda x: (x[1:], -1) if "-" in x else (x, 1), msort))
        offset = (page - 1) * page_size
        if fields:
            cursor = con.find(mfilter, fields).skip(offset).limit(page_size)
        else:
            cursor = con.find(mfilter).skip(offset).limit(page_size)

        if sorts:
            cursor = cursor.sort(sorts)

        res = []
        for document in cursor:
            document["_id"] = str(document["_id"])
            temp = {item: "" for item in mfields}
            temp.update(document)
            res.append(temp)
        return res

    def get_find_cursor(self, table, mfilter, mfields=[], msort=[]):
        con = self.get_collection(table)
        fields = {item: 1 for item in mfields}
        sorts = list(map(lambda x: (x[1:], -1) if "-" in x else (x, 1), msort))
        if fields:
            cursor = con.find(mfilter, fields)
        else:
            cursor = con.find(mfilter)

        if sorts:
            cursor = cursor.sort(sorts)

        return cursor

    def get_one_info(self, table, mfilter, mfields=[]):
        """
        @attention: 返回一条数据信息
        """
        con = self.get_collection(table)
        fields = {item: 1 for item in mfields}
        res = con.find_one(mfilter, fields)
        if res is None:
            return None
        else:
            res["_id"] = str(res["_id"])
            return res

    # 删除部分
    def delete_info(self, table, query):
        """
        @attention: 删除信息
        """
        con = self.get_collection(table)
        con.delete_many(query)

    def count(self, table, query, key="", is_distinct=False):
        """
        @attention: 统计次数
        @note: 去重需要传输key和is_distinct=True
        """
        con = self.get_collection(table)
        if is_distinct:
            num = len(con.distinct(key, query))
        else:
            num = con.count(query)
        return num

    def get_field_distinct_list(self, table, query, key):
        """
        @attention: 获取某个字段值去重后的集合
        """
        con = self.get_collection(table)
        info = con.distinct(key, query)
        return info

    def get_distinct_number(self, table, query, key):
        """
        @attention: 获取某个字段值去重后的数量,当数据量大时,可以防止大小超出上限
        """
        pipeline = [
            {"$match": query},
            {"$group": {"_id": "sum", "times": {"$addToSet": "$%s" % key}}},
            {"$project": {"times": {"$size": "$times"}}},
            {"$sort": {"times": -1}},
        ]
        info = self.run_pipeline(table, pipeline)
        info = list(info)
        if info:
            return info[0]["times"]
        else:
            return 0

    def run_pipeline(self, table, pipeline, allowDiskUse=True):
        """
        @attention:  统计管道函数
        """
        con = self.get_collection(table)
        return con.aggregate(pipeline, allowDiskUse=allowDiskUse)

    def drop(self, table):
        con = self.get_collection(table)
        con.drop()

    def create_index(self, table, index_list):
        """
        @attention:
        @param index_list: ('dt',1),('domain_port',1)
        """
        con = self.get_collection(table)
        con.create_index(index_list)

    def create_table(self, name):
        self.client[self.db].create_collection(name)

    def has_table(self, table):
        tables = self.client[self.db].collection_names()
        return table in tables

    # 复合类方法
    def update_or_create(self, table, query, update):
        """
        @attention: 如果存在，则修改，否则新增（针对单独一条数据）
        """
        res = self.get_one_info(table, query)
        if res:
            res["_id"] = ObjectId(res["_id"])
            self.update(table, res, update)
            pk = res["_id"]
        else:
            pk = self.single_insert(table, update)

        return str(pk)

    def sum(self, table, mfilter, keys):
        """
        @attention:  查询数据列表求和
        """
        keys_group = {item: {"$sum": "$%s" % item} for item in keys}
        keys_group.update({"_id": "sum"})
        pipeline = [
            {"$match": mfilter},
            {"$group": keys_group},
        ]
        res = list(self.run_pipeline(table, pipeline))
        if res:
            return res[0]
        else:
            return {}.fromkeys(keys, 0)

    def top(
        self,
        table,
        query,
        classify_param,
        count_param,
        top=0,
        sort_tag=-1,
        has_space=False,
    ):
        """
        @attention: 某个指定字段分布情况
        @param table: 表名
        @param query: 过滤条件
        @param classify_param: 分类字段
        @param count_param: 分类字段对应的次数字段,注意该字段的值必须是数字
        @param top: 取值范围,0表示获取全部
        @param sort_tag: 排序标识,默认按数字大小倒叙排列(从大到小);1:从小到大,-1:从大到小,0:不排序
        """
        if isinstance(classify_param, list):
            if not has_space:
                for param in classify_param:
                    if param in query:
                        query[param]["$ne"] = ""
                    else:
                        query.update({param: {"$ne": ""}})

            id_group = {"_id": {item: "$%s" % item for item in classify_param}}
            show = {"_id": 0, count_param: 1}
            show.update({item: "$_id.%s" % item for item in classify_param})
        else:
            if not has_space:
                if classify_param in query:
                    query[classify_param]["$ne"] = ""
                else:
                    query.update({classify_param: {"$ne": ""}})
            id_group = {"_id": {classify_param: "$%s" % classify_param}}
            show = {
                "_id": 0,
                count_param: 1,
                classify_param: "$_id.%s" % classify_param,
            }

        times_group = {count_param: {"$sum": "$%s" % count_param}}
        cgroup = {}
        cgroup.update(id_group)
        cgroup.update(times_group)

        pipeline = [
            {"$match": query},
            {"$group": cgroup},
        ]
        if sort_tag != 0:
            pipeline.append({"$sort": {count_param: sort_tag}})

        if top > 0:
            pipeline.append({"$limit": top})

        pipeline.append({"$project": show})
        info = self.run_pipeline(table, pipeline)

        #         for item in info:
        #             print item

        return info

    def show_indexes(self, table):
        """
        @attention: 显示索引
        """
        con = self.get_collection(table)
        return con.index_information()


def id_to_object(info):
    if isinstance(info, str):
        return ObjectId(info)
    elif isinstance(info, (list, tuple)):
        return [ObjectId(item) for item in info]


# -------------------- 常用函数 ------------------------------
def get_month_deltas(smon, emon):
    """
    @attention: 获取月份列表
    @param smon: 开始日期月份,字符串,例如:201709
    @param emon: 结束日期月份,字符串,例如:201810
    @note: 获取开始月份和结束月份之间的所有月份
    > 列出开始月份到结束月份所在年的所有月份,也就是说一年会生成12个字符串 201701~201712,
    > 用开始结束月份过滤上面那个集合
    """
    syear = int(smon[:4])
    eyear = int(emon[:4])
    years = range(syear, eyear + 1)
    months = ["%s%s" % (i, str(j).rjust(2, "0")) for i in years for j in range(1, 13)]
    return [item for item in months if smon <= item <= emon]


def get_day_deltas(sdate, edate):
    """
    @attention: 获取天列表
    """
    stdate = datetime.datetime.strptime(sdate, "%Y%m%d")
    etdate = datetime.datetime.strptime(edate, "%Y%m%d")
    ndays = (etdate - stdate).days

    dl = [stdate + datetime.timedelta(days=i) for i in range(ndays)]
    dl.append(etdate)

    datelist = [item.strftime("%Y%m%d") for item in dl]
    return [item for item in datelist if sdate <= item <= edate]


def get_hour_detas(shour, ehour):
    """
    @attention: 获取小时列表
    """
    sdate = shour[:8]
    edate = ehour[:8]
    datelist = get_day_deltas(sdate, edate)
    hours = [str(i).rjust(2, "0") for i in range(24)]
    return [d + h for d in datelist for h in hours if shour <= d + h <= ehour]


def get_everyhour_for_day(dt):
    """
    @attention: 获取某一天的每个小时
    """
    hours = [str(i).rjust(2, "0") for i in range(24)]
    return [dt + h for h in hours]


def str2ObjectId(cid):
    """
    @attention: 字符串ID转mongodb的ID
    """
    return ObjectId(cid)


# # mongo_manager = MongoManager("file_data","10.10.1.80",50001,"root","root")
# mongo_manager = MongoManager(*constant.MONGO_CONFIG)
