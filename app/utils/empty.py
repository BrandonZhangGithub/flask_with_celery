# -*- coding: utf-8 -*-
'''
@Create_at: 2020/08/22

@author: LuShuYang

@attention: 使用Empty来和原生的None Ellipsis区分.
'''


class Empty(object):
    """
    Distinct from Python's None and Ellipsis
    """
    is_Ellipsis = False
    is_None = False
