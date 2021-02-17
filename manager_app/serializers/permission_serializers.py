# -*- coding: utf-8 -*-
# @Time  : 2021/2/15 下午2:40
# @Author : 司云中
# @File : permission_serializers.py
# @Software: Pycharm
import time

from rest_framework import serializers

from manager_app.models import ManagerPermission


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ManagerPermission
        fields = ('pk', 'name', 'description', 'pid')
        read_only_fields = ('pk', )

    def create_permission(self):
        """添加权限"""
        credential = self.get_credential
        self.Meta.model.manager_permission_.create(**credential)

    def update_permission(self):
        """修改权限"""
        pk = self.validated_data.pop('pk'),
        credential = self.get_credential
        self.Meta.model.manager_permission_.filter(pk=pk).update(**credential)

    @property
    def get_credential(self):
        return {
            'name': self.validated_data.pop('name'),
            'description': self.validated_data.pop('description'),
            'pid': self.validated_data.pop('pid')
        }


class PermissionDeleteSerializer(serializers.Serializer):

    class Meta:
        model = ManagerPermission

    pk_list = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)

    def delete_permission(self):
        self.Meta.model.manager_permission_.filter(pk__in=self.validated_data.get('pk_list'))
