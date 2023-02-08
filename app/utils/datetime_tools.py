import time


def get_current_timeformat(fmt="%Y-%m-%d %H:%M:%S"):
    """
    获取当前时间格式
    """
    return time.strftime(fmt)


def get_current_timestamp(by_sc=False, by_ms=False, by_mcs=False):
    """
    @params by_sc 秒级
    @params by_ms 毫秒级
    @params by_mcs 微秒级
    """
    if by_sc:
        return int(time.time())
    if by_ms:
        return int(time.time() * 1000)
    if by_mcs:
        return int(time.time() * 1000000)
    return int(time.time())


def timestamp_2_format(timestamp, format="%Y-%m-%d %H:%M:%S") -> str:
    """
    时间戳转化为日期字符串
    """
    time_array = time.localtime(timestamp)
    return time.strftime(format, time_array)


def formattime_2_timestamp(formattime, format="%Y-%m-%d %H:%M:%S") -> int:
    """
    时间字符串转化为时间戳
    """
    if not formattime:
        return 0
    return int(time.mktime(time.strptime(formattime, format)))
