from django.shortcuts import render_to_response, get_object_or_404, render, redirect, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from blog.models import Content, Category, Tag, Comment
from blog.froms import CommentForm
from django.views.generic import View
from blog.froms import CommentForm
from django.views.generic import ListView, DetailView





def blog_paginator(request, post_list):

    paginator = Paginator(post_list, 10)  # 每页显示10条
    page_num = request.GET.get('page', 1)  # 获取页码
    page_of_blog = paginator.get_page(page_num)
    current_page = page_of_blog.number  # 获取当页码

    page_list = list()  # 页码
    for x in range(current_page - 2, current_page + 3):
        if x > 0 and x < paginator.num_pages + 1:
            page_list.append(x)


    return page_of_blog, page_list


def base_inquire():
    popular_list = Content.objects.all().order_by('-views')[0:6]  # 热门文章
    sort_list = Category.objects.all()  # 分类
    clound_tag = Tag.objects.all()  # 标签
    blog_dates = Content.objects.dates('created', 'month', order='DESC')  # 归档

    context = dict()
    context['popular_list'] = popular_list
    context['sort_list'] = sort_list
    context['tags'] = clound_tag
    context['blog_dates'] = blog_dates


    return context


# def index(request):
#
#     post_list = Content.objects.all().order_by('-created')
#     page_of_blog, page_list =blog_paginator(request, post_list)
#
#     context = base_inquire()
#     context['blogs'] = page_of_blog
#     context['page_range']  = page_list
#
#     return render(request, 'index.html', context)


class IndexView(ListView):
    model = Content
    template_name = 'index.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        post_list = Content.objects.all().order_by('-created')
        self.page_of_blog, self.page_list = blog_paginator(self.request, post_list)


    def get_context_data(self, **kwargs):

        context = super(IndexView, self).get_context_data()
        context['popular_list'] = Content.objects.all().order_by('-views')[0:6]  # 热门文章
        context['sort_list'] = Category.objects.all()  # 分类
        context['tags'] = Tag.objects.all()  # 标签
        context['blog_dates'] = Content.objects.dates('created', 'month', order='DESC')  # 归档
        context['blogs'] = self.page_of_blog
        context['page_range'] = self.page_list

        return context


class SearchView(ListView):

    model = Content
    template_name = 'blog_list.html'
    context_object_name = 'blogs'

    def get_queryset(self):

        key = self.request.GET.get('search') # 查询关键字
        search_result = Content.objects.filter(Q(title__contains=key)|Q(text__contains=key)).order_by('-created')  # 查询和 关键字相关的文章

        self.page_of_blog, self.page_list = blog_paginator(self.request, search_result)

        if key:  # 判断 接受到的key 是否为空
            return self.page_of_blog
        else:
            return None

    def get_context_data(self, *, object_list=None, **kwargs):

        context = super(SearchView, self).get_context_data(**kwargs)
        context['key'] = self.request.GET.get('serach', default=None)  # 获取关键字存入传入模板的数据中
        context['popular_list'] = Content.objects.all().order_by('-views')[0:6]  # 热门文章
        context['sort_list'] = Category.objects.all()  # 分类
        context['tags'] = Tag.objects.all()  # 标签
        context['blog_dates'] = Content.objects.dates('created', 'month', order='DESC')  # 归档
        context['blogs'] = self.page_of_blog
        context['page_range'] = self.page_list
        return context


class ArticleDetail(DetailView):

    model = Content
    template_name = 'detail.html'
    context_object_name = 'blog'

    def get(self, request, *args, **kwargs):
        response = super(ArticleDetail, self).get(request, *args, **kwargs)

        blog_content = get_object_or_404(Content, pk=kwargs['pk'])
        if not request.COOKIES.get('blog_%s_read' % kwargs['pk']):
            blog_content.views += 1  # 阅读书+1
            blog_content.save()

        response.set_cookie('blog_%s_read' % kwargs['pk'], 'true')

        return response


    def comment_sort(self, comments):  # 评论排序函数
        self.comment_list = []  # 排序后的评论列表
        self.top_level = []  # 存储顶级评论
        self.sub_level = {}  # 存储回复评论
        for comment in comments:  # 遍历所有评论
            if comment.reply == None:  # 如果没有回复目标
                self.top_level.append(comment)  # 存入顶级评论列表
            else:  # 否则
                self.sub_level.setdefault(comment.reply.id, []).append(comment)  # 以回复目标（父级评论）id为键存入字典
        for top_comment in self.top_level:  # 遍历顶级评论
            self.format_show(top_comment)  # 通过递归函数进行评论归类
        return self.comment_list  # 返回最终的评论列表

    def format_show(self, top_comment):  # 递归函数
        self.comment_list.append(top_comment)  # 将参数评论存入列表
        try:
            self.kids = self.sub_level[top_comment.id]  # 获取参数评论的所有回复评论
        except KeyError:  # 如果不存在回复评论
            pass  # 结束递归
        else:  # 否则
            for kid in self.kids:  # 遍历回复评论
                self.format_show(kid)  # 进行下一层递归

    def get_context_data(self, **kwargs):
        context = super(ArticleDetail, self).get_context_data(**kwargs)
        blog_content = get_object_or_404(Content, pk=self.kwargs['pk'])
        comments = Comment.objects.filter(article=blog_content)  # 通过文章id查询评论内容
        comment_form = CommentForm()  # 创建评论表单对象
        context['form'] = comment_form  # 将表单对象传送到模板的数据中
        context['comment_list'] = self.comment_sort(comments)  # 将排序归类后的文章列表存入传送到模板的数据中
        context['comment_count'] = Comment.objects.filter(article=blog_content).count()
        context['blog'] = blog_content
        context['popular_list'] = Content.objects.all().order_by('-views')[0:6]  # 热门文章
        context['sort_list'] = Category.objects.all()  # 分类
        context['tags'] = Tag.objects.all()  # 标签
        context['blog_dates'] = Content.objects.dates('created', 'month', order='DESC')  # 归档

        return context


def pub_comment(request):  # 发布评论函数
    if request.method == 'POST':  # 如果是post请求
        comment = Comment()  # 创建评论对象
        comment.article = Content.objects.get(id=request.POST.get('article'))  # 设置评论所属的文章
        if request.POST.get('reply') != '0':  # 如果回复的不是文章而是他人评论
            comment.reply = Comment.objects.get(id=request.POST.get('reply'))  # 设置回复的目标评论
        form = CommentForm(request.POST, instance=comment)  # 将用户的输入和评论对象结合为完整的表单数据对象
        if form.is_valid():  # 如果表单数据校验有效
            try:
                form.save()  # 将表单数据存入数据库
                result = '200'  # 提交结果为成功编码
            except:  # 如果发生异常
                result = '100'  # 提交结果为失败编码

        else:  # 如果表单数据校验无效
            result = '100'  # 提交结果为失败编码
        return HttpResponse(result)  # 返回提交结果到页面
    else:  # 如果不是post请求
        return HttpResponse('非法请求！')  # 返回提交结果到页面


# class BlogCommentView(View):
#
#     def format_show(self, top_comment):
#
#         self.comment_list.append(top_comment)   # 将参数评论存入列表
#
#         try:
#             self.kids = self.sub_level[top_comment.id]
#         except KeyError:  # 如果不存在回复评论
#             pass
#         else:
#             for kid in self.kids:
#                 self.format_show(kid)  # 进行下一层递归
#
#     def get(self, request, blog_pk):
#
#         self.blog_pk = blog_pk
#
#         blog_content = get_object_or_404(Content, pk=self.blog_pk)
#         if not request.COOKIES.get('blog_%s_read' % self.blog_pk):
#             # 判断COOKIES
#             blog_content.views += 1  # 阅读书+1
#             blog_content.save()
#         context = base_inquire()
#         context['blog'] = blog_content
#         context['user'] = request.user
#
#         self.comment_list = list()  # 评论列表
#         self.top_level = list()  # 顶级评论
#         self.sub_level = dict()  # 回复评论
#
#         comments = Comment.objects.filter(article=blog_content)
#         for comment in comments:
#             if comment.reply == None:  # 如果没有回复目标
#                 self.top_level.append(comment)  # 添加到顶级评论
#             else:
#                 self.sub_level.setdefault(comment.reply.id, []).append(comment)  # 把评论以 父级评论的 id 作为key 存入字典
#         for top_comment in self.top_level:  # 遍历顶级评论
#             self.format_show(top_comment)  # 把 顶级评论 通过递归进行归类
#         context['commnet_list'] = self.comment_list
#
#         form = CommentForm()
#         context['form'] = form  # 显示 评论列表
#
#         response = render(request, 'detail.html', context)  # 响应
#         response.set_cookie('blog_%s_read' % self.blog_pk, 'true', )
#         return response
#
#     def post(self, request):
#
#
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             host = form.cleaned_data['host']
#             text = form.cleaned_data['text']
#             article = Content.objects.get(id=self.blog_pk)
#             p = Comment(name=name, email=email, host=host, text=text, article=article)
#             p.save()
#
#         return render(request, 'detail.html')  # 响应


def blog_with_type(request, blog_type_pk):


    blog_type = get_object_or_404(Category, pk=blog_type_pk)
    blog_type_list = Content.objects.filter(category=blog_type)
    page_of_blog, page_list = blog_paginator(request, blog_type_list)

    context = base_inquire()
    context['blog_list'] = blog_type_list
    context['blogs'] = page_of_blog
    context['page_range']  = page_list

    return render(request, 'blog_list.html', context)


def blog_with_tag(request, tag_pk):

    blog_tag = get_object_or_404(Tag, pk=tag_pk)
    blog_type_list = Content.objects.filter(tags=blog_tag)
    page_of_blog, page_list = blog_paginator(request, blog_type_list)

    context = base_inquire()
    context['blog_list'] = blog_type_list
    context['blogs'] = page_of_blog

    return render(request, 'blog_list.html', context)


def blog_with_date(request, year, month):

    blog_list = Content.objects.filter(created__year=year,
                                       created__month=month
                                       ).order_by('-created')

    page_of_blog, page_list = blog_paginator(request, blog_list)

    context = base_inquire()
    context['blog_list'] = blog_list
    context['blogs'] = page_of_blog
    context['page_range']  = page_list


    return render(request, 'blog_list.html', context)


def blog_archive(request):

    context = base_inquire()

    return render(request, 'categories.html', context)





