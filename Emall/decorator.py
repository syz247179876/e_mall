# -*- coding: utf-8 -*-
# @Time  : 2021/1/8 下午7:32
# @Author : 司云中
# @File : decorator.py
# @Software: Pycharm

from Emall import drf_validators
from Emall.exceptions import DataFormatError


def validate_url_data(model, field, null=None):
    """
    通用校验字段装饰器工厂函数
    校验GET请求方式下不同Model中字段的数据格式
    :param model: 具体field所处的model类型,涉及多个模块,Model不一样,如foot, history, favorites, commodity, user等
    :param field: 具体字段,如pk, username, phone, commodity_name等
    :param null: 是否允许不存在数据
    :return: callback func(self, field)
    """

    def decorate(func):
        def inner(self, *args, **kwargs):
            value = self.request.query_params.get(field, None) or kwargs.get(field, None) or self.request.data.get(field, None)
            if not null and not value:
                raise DataFormatError('缺少必要的数据')

            validate_func_name = f'validate_{model}_{field}'
            validate_func = getattr(drf_validators, validate_func_name, None)  # 找到目标校验方法
            if not validate_func:
                raise ImportError('位于drf_validators中无匹配的校验方法')

            if value and not validate_func(value):
                raise DataFormatError()
            return func(self, *args, **kwargs)

        return inner

    return decorate
