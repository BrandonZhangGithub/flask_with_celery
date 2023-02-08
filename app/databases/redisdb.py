#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
Created on 2017年9月13日

@author: jianzhihua
"""

import re
from typing import List, Tuple

from redis import Redis, StrictRedis
from redis.sentinel import Sentinel


def create_sentinel_redis(config: dict) -> Tuple[Redis, Redis]:
    """创建一个Redis的主从链接"""
    host_port = parse_host(config["host-port"])
    sentinel = Sentinel(host_port, socket_timeout=2, password=config['pwd'], db=config['db'])
    master = sentinel.master_for('mymaster', socket_timeout=5)
    slave = sentinel.slave_for('mymaster', socket_timeout=2)
    return master, slave


def create_default_redis(redis_config):
    """
    @attention: 创建一个默认的redis环境
    """
    connect = StrictRedis(
        host=redis_config['host'], port=redis_config['port'], db=redis_config["db"], password=redis_config["passwd"])
    return connect


def parse_host(val: str) -> List[Tuple[str, int]]:
    """
    @attention: 分解host,把10.1.113.158-26379分割为("10.1.113.158",26379)
    """
    info = re.findall(r"([\d\.]+)-(\d+)", val)
    return [(item[0], int(item[1])) for item in info]


if __name__ == '__main__':
    a = "10.1.113.158-26379"
    print(parse_host(a))
