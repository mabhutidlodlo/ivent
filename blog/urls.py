from django.urls import path, include , re_path
from django.views.generic import TemplateView
from . import  views
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('', views.ListBlogs.as_view()),
    path('my_article/<str:slug>', views.Blogs.as_view()),
    path('category/<str:category>',views.CategoryBlogs.as_view()),
    path('comment/<str:slug>',views.Comments.as_view()),
    path('mycomment/<int:pk>',views.MyComment.as_view()),
    path('claps/<str:slug>',views.Claps.as_view()),
    path('myPost',views.MyBlog.as_view()),
    path('getAuthor/<str:slug>', views.GetAuthor.as_view()),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
