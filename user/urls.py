from django.urls import path

from .views import *

urlpatterns = [
    # 首页
    path('index', index),

    # 用户后台主页
    path('user_main_page', user_main_page),
    # 登录
    path('login', login),
    path('login_process', login_process),
    path('back_index', back_index),



]
