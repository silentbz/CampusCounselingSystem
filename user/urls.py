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

    # 注册

    path('register', register),
    path('register_process', register_process),
    path('website_service',website_service),
    # 个人中心
    path('person_info', person_info),
    # 修改个人信息
    path('edit_person_info', edit_person_info),
    # 修改密码

    path('change_password', change_password),
    path('change_password_process', change_password_process),
    # 修改头像
    path('change_user_img', change_user_img),
    path('change_user_img_process', change_user_img_process),

    # 动态信息

    path('personal_dynamic_info', personal_dynamic_info),
    path('dynamic_process', dynamic_process),
    # path('user_dynamic_result',user_dynamic_result),

    path('delete_dynamic', delete_dynamic),
    # 发布动态的界面
    path('submit_dynamic', submit_dynamic),
    # 评论信息
    path('submit_comment', submit_comment),
    path('comment_info', comment_info),
    path('comment_process', comment_process),

    # 点赞
    path('like_process', like_process),
    path('like', like),

    # 问题信息
    path('question_info', question_info),
    # 问题分享
    path('question_share',question_share),
    # 发布问题
    path('submit_question', submit_question),
    path('submit_question_process', submit_question_process),
    path('personal_question_info', personal_question_info),
    # 删除问题
    path('delete_question',delete_question),
    # 回复问题
    path('submit_reply', submit_reply),
    # 问答频道
    path('question_area', question_area),
    path('question_reply', question_reply),
    # 我的回答
    path('my_reply', my_reply),
    # 通知信息
    path('my_notice', my_notice),
    # 删除通知信息
    path('delete_notice',delete_notice),
    # 校园新闻
    path('school_news', school_news),

    path('notice_set_for_read', notice_set_for_read),
    # 获取手机验证码
    path('get_code', get_code),

    # 资源信息
    # 上传资源
    path('upload_resource', upload_resource),
    path('upload_resource_process', upload_resource_process),
    # 删除资源
    path('delete_resource',delete_resource),
    #
    path('download_resource', download_resource),
    # 资源广场
    path('download_resource_area', download_resource_area),
    # 我的资源
    path('my_resource', my_resource),
    # 搜索资源
    path('search_resource', search_resource),


    # ---------------------the content of below is test
    path('dynamic_for_index', dynamic_for_index),
    # ---------------------- end

    # -----------------------the chat page
    path('chat_page', chat_page),

    # -----------------------the chat page component
    path('chat_page_component', chat_page_component),
    # -------------------修改密码需重新登录
    path('login_again', login_again),
    # 我的评论 我的点赞
    path('my_comment', my_comment),
    path('my_like', my_like),
    # -------------------退出系统
    path('exit', exit),

    # admin----------------------------------------------------------------
    path('admin_index', admin_index),
    # 用户管理-------------------------------------------------------------
    # 冻结用户
    path('freeze_user', freeze_user),
    # 解冻用户
    path('unfreeze_user', unfreeze_user),
    # 删除用户
    path('delete_user', delete_user),

    # 资源管理-------------------------------------------------------------
    path('resource_manage',resource_manage),
    path('audit_resource',audit_resource),

    # 版块管理--------------------------------------------------------------------
    # 查看版块
    path('check_dynamic_topic', check_dynamic_topic),
    # 添加版块
    path('add_dynamic_topic', add_dynamic_topic),
    path('add_dynamic_topic_process', add_dynamic_topic_process),
    # 删除版块
    path('delete_dynamic_topic', delete_dynamic_topic),

    # 标注管理--------------------------------------------------------------------
    # 查看标注
    path('check_map_label', check_map_label),
    # 添加标注
    path('add_map_label', add_map_label),
    path('add_map_label_process', add_map_label_process),
    # 删除标注
    path('delete_map_label', delete_map_label),

    # 新闻管理----------------------------------------------------------------------------
    # 查看新闻
    path('check_school_news', check_school_news),
    # 发布新闻
    path('submit_school_news', submit_school_news),
    path('submit_school_news_process', submit_school_news_process),
    # 删除新闻
    path('delete_news', delete_news),
    # 修改密码和头像
    # 修改头像
    path('change_admin_img', change_admin_img),
    path('change_admin_img_process', change_admin_img_process),
    # 修改密码
    path('change_admin_password', change_admin_password),
    path('change_admin_password_process', change_admin_password_process),


]
