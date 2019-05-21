from django.contrib import admin
from blog.models import Content, Category, Tag, Comment
# Register your models here.


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    '''文章管理'''

    list_per_page = 10
    list_display = ('title', 'slug', 'status', 'views', 'category', 'author', 'created')

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display = ('id', 'name')

@admin.register(Category)
class Category_Admin(admin.ModelAdmin):
    list_display = ('id', 'name')



@admin.register(Comment)
class Comment_Admin(admin.ModelAdmin):
    list_display = ('id', 'text', 'created', 'name', 'host', 'article', 'reply')
