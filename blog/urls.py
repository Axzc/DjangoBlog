from django.urls import path
from django.views.generic import TemplateView
from blog import views

urlpatterns = [
    path('bloglist', views.IndexView.as_view(), name='blog_list'),
    path('archive', views.blog_archive, name='blog_archive'),
    path('tag/<int:tag_pk>', views.blog_with_tag, name='blog_with_tag'),
    path('type/<int:blog_type_pk>', views.blog_with_type, name='blog_with_type'),
    path('date/<int:year>/<int:month>', views.blog_with_date, name='blog_with_date'),
    path('about/', TemplateView.as_view(template_name='aboutme.html'), name='blog_about'),
    path('blog/<int:pk>', views.ArticleDetail.as_view(), name='blog_detail'),
    path('blog/comment/', views.pub_comment, name='comment'),
    path('blog/search/', views.SearchView.as_view(), name='search'),
    path('', views.IndexView.as_view(), name='index'),

]
