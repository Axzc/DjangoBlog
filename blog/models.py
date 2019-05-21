from django.db import models
from db.base_model import BaseModel
from django.contrib.auth.models import AbstractUser
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.


class Tag(models.Model):
    '''标签表'''
    name = models.CharField(max_length=50)

    def __str__(self):

        return self.name


class Category(models.Model):
    '''分类表'''
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)


    def __str__(self):

        return self.name


class User(AbstractUser, BaseModel):

    host = models.CharField(max_length=200, null=True, blank=True, default=' ')

    class Meta:
        db_table = 'blog_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class Content(BaseModel):
    '''文章表'''
    status_choices = (
        (0, '上线'),
        (1, '下线'),
    )

    title = models.CharField(max_length=70, verbose_name='文章标题')
    slug = models.CharField(max_length=200, blank=True, null=True, verbose_name='文章概述')
    text = RichTextUploadingField()
    status = models.SmallIntegerField(default=0, choices=status_choices, verbose_name='文章状态')
    views = models.PositiveIntegerField(default=0, verbose_name='阅读数量')
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')
    author = models.ForeignKey(User, verbose_name='文章作者', on_delete=models.DO_NOTHING)

    def __str__(self):

        return self.title

    class Meta:
        db_table = 'blog_content'
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created']

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])


class Comment(BaseModel):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, verbose_name='昵称', default='')
    email = models.CharField(max_length=50, verbose_name='email')
    host = models.CharField(max_length=20, null=True, blank=True, verbose_name='网站')
    text = models.TextField(null=False, verbose_name='回复内容')
    article = models.ForeignKey(Content, on_delete=models.CASCADE, verbose_name='所属文章', default='')
    reply = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name='回复')

    class Meta:
        db_table = 'blog_comment'
        verbose_name = '评论'
        verbose_name_plural = verbose_name

    def __str__(self):

        return self.text









