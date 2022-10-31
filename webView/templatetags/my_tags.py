#!/usr/bin/env python3.8
# @Time:2022/5/4
# @Author:CarryLee
# @File:my_tags.py
# @Info:存放自定义的标签和过滤器
from django import template

register = template.Library()  # register的名字是固定的,不可改变


# 利用装饰器 @register.filter 自定义过滤器
# 利用装饰器 @register.simple_tag 自定义标签

@register.filter
def x100(v1):
    return round(v1 * 100, 2)


@register.filter
def split(v1, v2):
    return v1.split(',')[v2]


@register.filter
def split_num(v1):
    return len(v1.split(','))
