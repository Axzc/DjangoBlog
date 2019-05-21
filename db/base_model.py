from django.db import models


class BaseModel(models.Model):
    '''模型类 抽象基类'''
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    modified = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')

    class Meta:
        '''说明抽象模型类'''
        abstract = True
