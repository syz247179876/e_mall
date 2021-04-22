# -*- coding: utf-8 -*-
# @Time  : 2021/4/13 下午2:19
# @Author : 司云中
# @File : display_api.py
# @Software: Pycharm

from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from Emall.exceptions import DataFormatError, DataNotExist
from search_app.signals import retrieve_from_es, parse_hits, record_search, retrieve_heat_keyword, retrieve_record
from search_app.utils.common import identity
from shop_app.models.commodity_models import Commodity
from shop_app.serializers.diplay_serializers import CommodityCardSerializer, CommodityDetailSerializer
from user_app.signals import retrieve_collect, retrieve_foot, retrieve_bought


class CommodityCardDisplay(GenericViewSet):
    """用于商品的显示API"""

    serializer_class = CommodityCardSerializer

    def dsl_body(self, q):
        """
        DSL表达式的body部分
        使用bool表达式将多个叶子语句合并成单一语句进行查找
        """
        return {
            "query": {
                "bool": {
                    "should": [
                        {"match": {"commodity_name": q}},
                        {"match": {"intro": q}},
                        {"match": {"category": q}}
                    ]
                }
            }
        }

    def dsl_single_body(self, q):
        """
        搜索分数值最高的一个商品
        :return: dict
        """
        return {
            "query": {
                "bool": {
                    "should": [
                        {"match": {"commodity_name": q}},
                        {"match": {"intro": q}},
                        {"match": {"category": q}}
                    ]
                }
            },
            "from": 0,  # 从第0个商品开始查
            "size": 1  # 查询一个结果
        }

    def retrieve_dsl(self, index=None, **kwargs):
        """
        获取商品的dsl表达式
        :param index: 索引库名，可自定义/从配置文件读
        :param kwargs: 其他body参数
        :return:
        """
        return {
            "sender": index or settings.ES_INDICES.get('default'),
            "body": kwargs
        }

    def get_keyword_queryset(self, pk_list):
        """按照pk_list进行查询，然后按照指定的顺序排序"""
        ordering = 'FIELD(`id`, {})'.format(','.join([str(pk) for pk in pk_list]))  # 设定排序
        return Commodity.commodity_.filter(pk__in=pk_list).extra(select={"ordering": ordering},
                                                                 order_by=("ordering",))

    @identity
    def send_record_signal(self, request, unique_identity):
        """发送记录历史搜索记录信号"""
        record_search.send(sender=unique_identity, request=request, keyword=self.request.query_params.get('q'))

    @action(detail=False, methods=['GET'], url_path='keyword')
    def keyword_list(self, request):
        """关键字搜索，获取商品API"""
        if not request.query_params.get('q', None):
            raise DataFormatError('缺少必要参数')
        keyword = request.query_params.get('q')
        results = retrieve_from_es.send(**self.retrieve_dsl(**self.dsl_body(keyword)))[0]  # 发送信号，搜索es，获取id列表
        code, res = results[1]
        print(code, res)
        if code == 200:
            pk_list = parse_hits.send(sender=self.__class__.__name__, result=res)[0]  # 解析数据
            serializer = self.get_serializer(instance=self.get_keyword_queryset(pk_list[1]), many=True)
            self.send_record_signal(request)  # 发送信号,记录用户搜索记录
            return Response(serializer.data)
        return Response([])

    @action(detail=False, methods=['GET'], url_path='recommend')
    @identity
    def recommend_list(self, request, unique_identity, *args, **kwargs):
        """
        首页推荐商品，数据来源：
        1.用户的搜索关键字 -- weight=10
        2.用户的收藏商品 -- weight= 10
        3.用户的足迹商品 -- weight=5
        4.用户的购买商品 -- weight=15

        采用zset，key为类型，score为类型出现的次数，作为推荐衡量

        """

        search_history = retrieve_record.send(sender=unique_identity, request=request)
        collect = retrieve_collect.send(sender=unique_identity)
        foot = retrieve_foot.send(sender=unique_identity)
        bought = retrieve_bought.send(sender=unique_identity)

    @action(detail=False, methods=['GET'], url_path='discount')
    def discount_list(self, request):
        """每日打折商品"""
        pass

    @action(detail=False, methods=['GET'], url_path='prise')
    def prise_list(self, request):
        """每日好评商品"""
        pass

    @action(detail=False, methods=['GET'], url_path='heats')
    def heat_list(self, request):
        """每日最火搜索的商品"""
        result = retrieve_heat_keyword.send(sender=None)
        cur_heat = [word.decode() for word in result[0][1]]  # 当天热搜词
        print(cur_heat)
        heat_keyword = cur_heat[0] if cur_heat else '美食'
        results = retrieve_from_es.send(**self.retrieve_dsl(**self.dsl_single_body(heat_keyword)))[0]
        code, res = results[1]
        if code == 200:
            pk_list = parse_hits.send(sender=self.__class__.__name__, result=res)[0]  # 解析数据
            serializer = self.get_serializer(instance=self.get_keyword_queryset(pk_list[1]), many=True)
            return Response(serializer.data)
        return Response(cur_heat)


class CommodityDetailDisplay(GenericViewSet):
    """
    商品详情页API
    包含商品基本信息API，商品SKU属性键值API
    """

    serializer_class = CommodityDetailSerializer

    model = Commodity

    def get_instance(self, pk):
        """根据pk获取商品对象，join联合查询多表"""
        try:
            return self.model.commodity_.select_related('store').select_related('freight').prefetch_related(
                'sku').prefetch_related('remark').get(
                pk=pk)
        except self.model.DoesNotExist:
            raise DataNotExist()

    @action(detail=False, methods=['GET'], url_path='detail')
    def detail_list(self, request):
        """获取指定商品详情信息"""
        pk = request.query_params.get('pk')
        obj = self.get_instance(pk)
        serializer = self.get_serializer(instance=obj)
        return Response(serializer.data)
