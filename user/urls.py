from django.urls import path

from .views import *

urlpatterns = [
    # 首页
    path('index', index),

    path('back_index', back_index),



]
