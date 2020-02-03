# from django.views.decorators import csrf
# from user.models import User
# from user import *
import logging
#
from django.core import serializers
# import json
import numpy
# from itertools import chain
from django.db.models import F
import user.zhenzismsclient as smsclient
import random
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import redirect
# from django.shortcuts import render_to_response
from django.shortcuts import render
from django.db.models import Q
from .models import User, DynamicInfo, Comments, Likes, Question, ReplyQuestion, Notice, DynamicTopic, Resource, Admin, \
    Place, News
from . import models
import  datetime
import numpy as np
import user.recommend_new as recommend
from django.core.paginator import Paginator


# Create your views here.
# 首页------------------------------------------------------------------------------------------
def index(request):
    print("ok entered!")
    # 加载全景图中所有的标注
    all_places = models.Place.objects.all()

    return render(request, "index/index.html", {"all_places": all_places})


# 登录成功后 用户返回首页
def back_index(request):
    all_places = models.Place.objects.all()

    return render(request, "index/back_index.html", {"all_places": all_places})





# 登录注册模块=-----------------------------------------------------------------------------------
def login(request):
    print("You enter the method of login")
    return render(request, "login_register/login.html")


# 用于存储转化的时间
class Date_Info:
    def __init__(self, date, time_line):
        self.date = date
        self.time = time_line

    def get_date(self):
        return self.date

    def get_time(self):
        return self.time


def user_main_page(request):
    user = request.session.get('user', None)
    # 用户如果没有登录 跳转到登录界面
    if not user:
        return redirect('/user/login')
    my_notices_unread = models.Notice.objects.filter(Q(user=user) & Q(notice_status='未读')).count()
    my_dynamic_info = models.DynamicInfo.objects.all().order_by("-dynamic_time")

    all_user = models.User.objects.all()

    all_dynamic = models.DynamicInfo.objects.all()
    users_list = []
    init_first = []
    flag = 0
    for dynamic in all_dynamic:
        init_first.append(0)
    # [0,0,0,0,...,0]
    users_list.append(init_first)
    current_user_index = 1
    user_index_flag = 0
    user_dict = {}
    user_count = 1
    for user_for_init_list in all_user:
        user_dict[str(user_count)] = user_for_init_list.id
        user_count = user_count + 1
    for user_for_init_list in all_user:
        user_list = []
        if user_index_flag==0:
            if user_for_init_list!=user:
                current_user_index = current_user_index+1
            else:
                user_index_flag = 1
                print("current_user_index is%d"%current_user_index)

        for dynamic_for_init_list in all_dynamic:
            if flag == 0:
                # print(dynamic_for_init_list.id, end=" ")
                print(dynamic_for_init_list.id)
            # 用户是否发布过该动态
            user_dynamic = models.DynamicInfo.objects.filter(
                Q(user=user_for_init_list) & Q(id=dynamic_for_init_list.id))
            # 用户是否评论过
            user_comment = models.Comments.objects.filter(
                Q(critic_id=user_for_init_list.id) & Q(dynamic_info=dynamic_for_init_list))
            # 用户是否点赞过
            user_like = models.Likes.objects.filter(
                Q(praises_id=user_for_init_list.id) & Q(dynamic_info=dynamic_for_init_list))

            if not user_comment:

                if not user_like:
                    if not user_dynamic:
                        user_list.append(0)  # 如果用户没有发布 评论、点赞该动态则设置为0

                    else:
                        user_list.append(1)  # 用户发布过该动态 但没有评论和点赞 设置为1
                else:
                    user_list.append(1)  # 用户没有评论 但点赞过该动态 设置为1
            else:
                user_list.append(1)  # 用户评论过该动态 设置为1

        # print("user_id为%d" % user_for_init_list.id)
        # print('**'*30)
        # print(user_list)
        # print('**' * 30)
        users_list.append(user_list)
        flag = 1
    users_array = np.array(users_list)
    for i in range(users_array.__len__()):
        print(users_array[i])
        pass
    sim_users_id = recommend.get_sim_users_id(users_array, current_user_index, all_user.count() + 1)  # 获得用户列表 类型为list 已按相似度排序
    #print("相似用户序列id为")
    #print(type(sim_users_id))
    #print(sim_users_id)
    sim_user_result_dynamic = {}  # 获得相似用户中的动态 并且当前用户没有对这些动态评论或点赞过 这样就推荐给当前用户
    for sim_user in sim_users_id:
        #print(user_dict[sim_user[0]])  # 输出用户id（按用户相似度依次递减）
        #print(sim_user[1])  # 输出用户相似度
        sim_user = models.User.objects.get(id=user_dict[sim_user[0]])  # 得到相似用户
        sim_user_dynamic = models.DynamicInfo.objects.filter(user=sim_user)  # 获取相似用户动态
        #
        # 得到相似用户评论过的动态
        print("sim_user_comment------------------>")
        sim_user_dynamic_for_comment = models.Comments.objects.filter(critic_id=sim_user.id)
        #print("用户%d评论过%d条动态" % (sim_user.id, sim_user_dynamic_for_comment.count()))
        for sim_dynamic_for_comment in sim_user_dynamic_for_comment:
            # 当前用户是否发布过该动态
            user_dynamic = models.DynamicInfo.objects.filter(
                Q(user=user) & Q(id=sim_dynamic_for_comment.dynamic_info.id))
            # 当前用户是否评论过该动态
            user_comment = models.Comments.objects.filter(
                Q(critic_id=user.id) & Q(dynamic_info=sim_dynamic_for_comment.dynamic_info))
            # 用户是否点赞过该动态
            user_like = models.Likes.objects.filter(
                Q(praises_id=user.id) & Q(dynamic_info=sim_dynamic_for_comment.dynamic_info))
            if not user_comment:
                if not user_like:
                    if not user_dynamic:
                        #print(sim_dynamic_for_comment.dynamic_info.dynamic_content)
                        # 每次保证推送3条动态
                        print("长度为----------------->%d"%len(sim_user_result_dynamic))
                        if len(sim_user_result_dynamic)<3:
                            sim_user_result_dynamic[
                                sim_dynamic_for_comment.dynamic_info.id] = sim_dynamic_for_comment.dynamic_info
        # 得到相似用户点赞过的动态
        sim_user_dynamic_for_like = models.Likes.objects.filter(praises_id=sim_user.id)
        print("sim_user_like------------------>")
        for sim_dynamic_for_like in sim_user_dynamic_for_like:
            # 当前用户是否发布过该动态
            user_dynamic = models.DynamicInfo.objects.filter(
                Q(user=user) & Q(id=sim_dynamic_for_like.dynamic_info.id))
            # 当前用户是否评论过该动态
            user_comment = models.Comments.objects.filter(
                Q(critic_id=user.id) & Q(dynamic_info=sim_dynamic_for_like.dynamic_info))
            # 用户是否点赞过该动态
            user_like = models.Likes.objects.filter(
                Q(praises_id=user.id) & Q(dynamic_info=sim_dynamic_for_like.dynamic_info))

            #print("get_id-----")
            if not user_comment:
                if not user_like:
                    if not user_dynamic:
                        #print(sim_dynamic_for_like.dynamic_info.dynamic_content)
                        #print(sim_dynamic_for_like.dynamic_info.id)
                        # 每次保证推送3条动态
                        print("长度为----------------->%d"%len(sim_user_result_dynamic))

                        if len(sim_user_result_dynamic) <3:
                            sim_user_result_dynamic[sim_dynamic_for_like.dynamic_info.id] = sim_dynamic_for_like.dynamic_info

        for sim_dynamic in sim_user_dynamic:
            # 当前用户是否发布过该动态
            user_dynamic = models.DynamicInfo.objects.filter(
                Q(user=user) & Q(id=sim_dynamic.id))
            #     # 当前用户是否评论过该动态
            user_comment = models.Comments.objects.filter(Q(critic_id=user.id) & Q(dynamic_info=sim_dynamic))
            #     # 用户是否点赞过该动态
            user_like = models.Likes.objects.filter(Q(praises_id=user.id) & Q(dynamic_info=sim_dynamic))
            # sim_user_result_dynamic[sim_dynamic.id] = sim_dynamic
            # print(sim_dynamic.dynamic_content)
            if not user_comment:
                if not user_like:
                    if not user_dynamic:
                        # 每次保证推送3条动态
                        print("长度为----------------->%d"%len(sim_user_result_dynamic))

                        if len(sim_user_result_dynamic) < 3:
                            sim_user_result_dynamic[sim_dynamic.id] = sim_dynamic

    print("***************************************")
    users_list =  np.array(users_list)
    print(users_list[current_user_index])
    print("***************************************")
    if users_list[current_user_index].any() == 0:# 当前用户是新用户
        # 当给新注册的用户进行推荐(推荐前3条) 按评论数和点赞数之和 进行排序 由高到低 防止冷启动问题
        print("当前用户是新用户")
        sim_user_result_dynamic = models.DynamicInfo.objects.all().order_by(F('dynamic_likes') + F('dynamic_comments')).reverse()[:3]
    else:
        # 如果不是新用户
        sim_user_result_dynamic = sim_user_result_dynamic.values()
    now = datetime.datetime.now()
    all_comments = {}
    #print("dynamic_id---------------------->")
    # for dynamic in sim_user_result_dynamic.values():
    for dynamic in my_dynamic_info:
        print(dynamic.id)
        comments = models.Comments.objects.filter(dynamic_info=dynamic).order_by("comment_time")

        # 得到每条动态的评论数
        comment_number = models.Comments.objects.filter(dynamic_info=dynamic).count()
        dynamic.dynamic_comments = comment_number
        dynamic.save()
        all_comments[dynamic.id] = comments
    return render(request, "dynamic_manage/user_main_page.html",
                  {
                        "recommend_dynamic_info": sim_user_result_dynamic
                      , "dynamic_info": my_dynamic_info
                      , "notices": my_notices_unread
                      , "user": user
                      , "all_comments": all_comments
                      , "now": now
                  })

    # return render(request, "user_main_page.html",
    #               {"dynamic_info": my_dynamic_info, "notices": my_notices_unread, "user": user,
    #                "all_comments": all_comments, "now": now})


# 个人中心
def person_info(request):
    user = request.session.get('user', None)
    # 用户如果没有登录 跳转到登录界面
    if not user:
        return redirect('/user/login')
    notice_three = models.Notice.objects.filter(Q(user=user) & Q(notice_status='未读')).count()

    return render(request, "user_info_manage/person_info.html", {"notices": notice_three, "user": user})


def edit_person_info(request):
    user = request.session.get('user', None)
    # 用户如果没有登录 跳转到登录界面
    if not user:
        return redirect('/user/login')
    notice_three = models.Notice.objects.filter(Q(user=user) & Q(notice_status='未读')).count()
    user_name = request.POST['user_name']
    user_sex = None
    user_description = None
    # 为防止用户没有输入进行提交
    try:
        user_sex = request.POST['user_sex']
        user_description = request.POST['user_description']
        print('--------------------->' + user_sex)
        print('--------------------->' + user_description)
    except Exception as e:
        logging.info(e)
        print("用户没有输入数据")
    if user_sex is None:
        user_sex = None
    if user_description is None:
        user_description = None

    user_phone = request.POST['user_phone']
    user_email = request.POST['user_email']

    print('--------------------->' + user_email)

    user.user_name = user_name
    user.user_sex = user_sex
    user.user_phone = user_phone
    user.user_email = user_email
    user.user_description = user_description
    user.save()
    # request.session.clear()
    # request.session['user'] = user
    # user = request.session.get('user', None)
    print("ENTERED!")
    return render(request, "user_info_manage/person_info.html", {"notices": notice_three, "user": user, "hint": "保存成功！"})


# -------------------------------------------------This is test
# 得到所有的用户动态信息
# def user_dynamic_result(request):
#     dynamic_info = models.DynamicInfo.objects.all()
#     return render(request, "user_dynamic_result.html", {"dynamic_info": dynamic_info})


def dynamic_for_index(request):
    place_value = request.GET['place_value']
    dynamic_topic = ""

    my_dynamic_info = ""
    recommend_dynamic = ""
    try:
        # 遇到异常时不会执行 print(place_value)及其以下的语句
        # 推荐的动态
        recommend_dynamic = models.DynamicInfo.objects.filter(id=place_value)
        print("推荐的id-----------------------")
        print(place_value)
        print(recommend_dynamic)
    except Exception as e1:
        pass
    try:
        dynamic_topic = models.DynamicTopic.objects.get(topic_content=place_value)

    except Exception as e:
        #print(dynamic_topic)
        #print(recommend_dynamic)
        pass
    if recommend_dynamic:
        my_dynamic_info = recommend_dynamic
    else:
        if not dynamic_topic:
            print("+" * 20)
            my_dynamic_info = models.DynamicInfo.objects.filter(
            Q(dynamic_content__contains=place_value)).order_by("-dynamic_time")
            # return render(request, "dynamic_for_index.html")
            print(my_dynamic_info)
        else:
            my_dynamic_info = models.DynamicInfo.objects.filter(
                Q(dynamic_topic=dynamic_topic) | Q(dynamic_content__contains=place_value)).order_by("-dynamic_time")

    # 找到版块为图书馆或找到内容中包含图书馆的动态

    all_comments = {}
    # print(my_dynamic_info.count())
    for dynamic in my_dynamic_info:
        comments = models.Comments.objects.filter(dynamic_info=dynamic)

        # 得到每条动态的评论数
        comment_number = models.Comments.objects.filter(dynamic_info=dynamic).count()
        dynamic.dynamic_comments = comment_number
        dynamic.save()
        all_comments[dynamic.id] = comments
    print('**' * 25)
    print(place_value)
    return render(request, "dynamic_manage/dynamic_for_index.html", {"dynamic_info": my_dynamic_info, "all_comments": all_comments})


# ----------------------------------------------------------------
def login_process(request):
    user_info = request.POST['user_info']
    user_password = request.POST['user_password']
    user = models.User.objects.filter(
        (Q(user_name=user_info) | Q(user_phone=user_info) | Q(user_email=user_info)) & Q(
            user_password=user_password)).first()
    admin = models.Admin.objects.filter(
        (Q(admin_name=user_info) | Q(admin_phone=user_info) | Q(admin_email=user_info)) & Q(
            admin_password=user_password)).first()
    # 管理员登录
    if admin:
        request.session['admin'] = admin
        page_index = None

        try:

            page_index = request.GET['page_index']
        except Exception as e:
            logging.info(e)

        if page_index is None:
            page_index = 1

        else:
            if page_index != "":
                page_index = int(page_index)
            else:
                page_index = 1
        all_user = models.User.objects.all()
        users = Paginator(all_user, 3)
        page_info = users.page(page_index)

        return render(request, "admin/admin_main_page.html", {"admin": admin, "all_user": page_info})

    # 用户不存在 返回登录界面
    # if user.count()==0:
    #     return render(request, "login.html",{"login_failure":"failure"})
    if user:
        # 判断用户状态是否正常
        if user.user_state == '已冻结':
            return render(request, "login_register/login.html", {"login_failure": "freeze"})
        request.session['user'] = user
        # 记住用户上次登录时间
        now = datetime.datetime.now()
        user.last_login_time = now
        user.save()
        # 我的通知 得到通知数
        my_notices_unread = models.Notice.objects.filter(Q(user=user) & Q(notice_status='未读')).count()
        my_dynamic_info = models.DynamicInfo.objects.all().order_by("-dynamic_time")

        all_comments = {}
        for dynamic in my_dynamic_info:
            comments = models.Comments.objects.filter(dynamic_info=dynamic)

            # 得到每条动态的评论数
            comment_number = models.Comments.objects.filter(dynamic_info=dynamic).count()
            dynamic.dynamic_comments = comment_number
            dynamic.save()
            all_comments[dynamic.id] = comments



            # 判断查询集是否为空
            # 1. if user.exist() 2. if user.count()==0 3. if user:
        # for dynamic in my_dynamic_info:
        #     for ct in all_comments[dynamic.id]:
        #         print(ct.comment_content)
        # for comment in all_comments.values():
        #     print(comment)
        now = datetime.datetime.now()

        # return render(request, "user_main_page.html",{"dynamic_info": my_dynamic_info})
        return render(request, "dynamic_manage/user_main_page.html",
                      {"dynamic_info": my_dynamic_info, "notices": my_notices_unread, "user": user,
                       "all_comments": all_comments, "now": now})

    return render(request, "login_register/login.html", {"login_failure": "failure"})


def register(request):
    return render(request, "login_register/register.html")


def register_process(request):
    user_name = request.POST['user_name']

    user_email = request.POST['user_email']
    user_phone = request.POST['user_phone']
    user_password = request.POST['user_password']
    user_state = '正常'
    # 判断当前用户是否已经注册
    user = models.User.objects.filter(Q(user_email=user_email) | Q(user_phone=user_phone))
    if user:
        return render(request, "login_register/register.html", {"register_failure": "failure"})
    now = datetime.datetime.now()
    user = User(
        user_name=user_name,
        user_email=user_email,
        user_phone=user_phone,
        user_password=user_password,
        user_state=user_state,
        register_time=now,
    )
    user.save()
    return render(request, "login_register/register.html", {"register_success": "success"})
    # 重定向
    # return redirect("/user/login")
    # return render(request,"login.html")
# 网站服务协议（注册）
def website_service(request):
    return render(request,"login_register/website_service.html")

# 动态模块------------------------------------------------------------------------------------
def personal_dynamic_info(request):
    user = request.session.get('user', None)
    # 用户如果没有登录 跳转到登录界面
    if not user:
        return redirect('/user/login')
    my_notice = models.Notice.objects.filter(Q(user=user) & Q(notice_status='未读')).count()

    my_dynamic_info = models.DynamicInfo.objects.filter(user=user).order_by("-dynamic_time")
    all_comments = {}
    # print(my_dynamic_info.count())
    for dynamic in my_dynamic_info:
        comments = models.Comments.objects.filter(dynamic_info=dynamic)

        # 得到每条动态的评论数
        comment_number = models.Comments.objects.filter(dynamic_info=dynamic).count()
        dynamic.dynamic_comments = comment_number
        dynamic.save()
        all_comments[dynamic.id] = comments
    print(my_dynamic_info.count())
    # return HttpResponse("dynamic_info")


    return render(request, "dynamic_manage/personal_dynamic_info.html",
                  {"dynamic_info": my_dynamic_info, "notices": my_notice, "user": user, "all_comments": all_comments})


# 发布动态界面
def submit_dynamic(request):
    # 判断用户是否已经登陆
    user = request.session.get('user', None)
    if not user:  # 用户未被登录
        print("#" * 50)
        print('not login!')
        return redirect("/user/login")
    else:  # 用户已登录
        print("#" * 50)
        print('login!')

    # 加载版块信息
    dynamic_topic = models.DynamicTopic.objects.all()

    notice_one = models.Notice.objects.filter(Q(user=user) & Q(notice_status='未读')).count()

    return render(request, "dynamic_manage/submit_dynamic.html", {"dynamic_topic": dynamic_topic, "user": user, "notices": notice_one})


# 发布动态
def dynamic_process(request):
    user = request.session.get('user', None)
    if not user:  # 用户未被登录
        print("#" * 50)
        print('not login!')
        return redirect("/user/login")

    topic_id = request.POST['topic_id']
    dynamic_topic = models.DynamicTopic.objects.get(id=topic_id)
    dynamic_content = request.POST['dynamic_content']
    dynamic_img = None
    try:
        dynamic_img = request.FILES['dynamic_img']
    except Exception as e:

        pass

    now = datetime.datetime.now()
    dynamic = DynamicInfo(
        user=user,
        dynamic_topic=dynamic_topic,
        dynamic_content=dynamic_content,
        dynamic_img=dynamic_img,

        dynamic_likes=0,
        dynamic_comments=0,
        dynamic_time=now,

    )
    print("save success")
    dynamic.save()
    # return HttpResponse("dynamic_process_success")
    return render(request, "dynamic_manage/submit_dynamic_success.html", {"user": user})


# 删除动态
def delete_dynamic(request):
    dynamic_id = request.GET['dynamic_id']
    dynamic = models.DynamicInfo.objects.get(id=dynamic_id)
    # 将该动态的评论和点赞都删除
    likes = models.Likes.objects.filter(dynamic_info=dynamic)
    comments = models.Comments.objects.filter(dynamic_info=dynamic)
    for l in likes:
        l.delete()
    for c in comments:
        c.delete()
    dynamic.delete()
    return HttpResponse("删除成功")


# 评论模块------------------------------------------------------------------------------------

# 用户发布评论
def submit_comment(request):
    user = request.session.get('user', None)
    if not user:  # 用户未被登录
        print("#" * 50)
        print('not login!')
        return redirect("/user/login")
    # 'data': {dynamic_id: dynamic_id, user_comment: user_comment},
    dynamic_id = request.POST['dynamic_id']
    comment_content = request.POST['user_comment']
    # 根据dynamic_id得到dynamic
    dynamic_info = models.DynamicInfo.objects.get(id=dynamic_id)

    # 评论者id
    critic_id = user.id
    # 评论者姓名
    critic_name = user.user_name
    # 评论者头像
    critic_img = user.user_img
    # 发布者id
    publisher_id = dynamic_info.user.id
    # django.utils.datastructures.MultiValueDictKeyError: 'comment_comment' 没有提取到key值

    print(type(comment_content))
    print("**" * 30)
    now = datetime.datetime.now()
    comment = Comments(
        dynamic_info=dynamic_info,
        critic_id=critic_id,
        critic_name=critic_name,
        critic_img=critic_img,
        publisher_id=publisher_id,
        comment_content=comment_content,
        comment_time=now,
    )

    comment.save()
    # 当用户评论后 要发送通知给原用户
    notice_content_for_comment = user.user_name + "评论了你编号为" + str(dynamic_info.id) + "的动态"
    now = datetime.datetime.now()
    notice_for_comment = Notice(
        user=dynamic_info.user,
        notice_status='未读',
        notice_content=notice_content_for_comment,
        notice_time=now,
    )
    notice_for_comment.save()
    # 获得当前用户的通知数
    my_notice = models.Notice.objects.filter(Q(user=user) & Q(notice_status='未读')).count()
    # 按照时间从大到小排序
    my_dynamic_info = models.DynamicInfo.objects.all().order_by("-dynamic_time")
    all_comments = {}
    for dynamic in my_dynamic_info:
        comments = models.Comments.objects.filter(dynamic_info=dynamic)

        # 得到每条动态的评论数
        comment_number = models.Comments.objects.filter(dynamic_info=dynamic).count()
        dynamic.dynamic_comments = comment_number
        dynamic.save()
        all_comments[dynamic.id] = comments
    return render(request, "dynamic_manage/user_main_page.html",
                  {"dynamic_info": my_dynamic_info, "notices": my_notice, "user": user, "all_comments": all_comments})


def comment_info(request):
    dynamic = models.DynamicInfo.objects.get(id=4)
    comments = models.Comments.objects.filter(dynamic_info=dynamic)
    for comment in comments:
        print(comment.comment_content)
    return HttpResponse("comment_info")


def comment_process(request):
    dynamic_info_id = models.DynamicInfo.objects.get(id=1)
    # 评论者id
    critic_id = 5
    # 发布者id
    publisher_id = 1
    # django.utils.datastructures.MultiValueDictKeyError: 'comment_comment' 没有提取到key值

    comment_content = request.POST['comment_content']
    print(type(comment_content))
    print("**" * 30)
    comments = Comments(
        dynamic_info=dynamic_info_id,
        critic_id=critic_id,
        publisher_id=publisher_id,
        comment_content=comment_content,
    )
    comments.save()

    return HttpResponse("comment_process")


# 点赞模块----------------------------------------------------

def like_process(request):
    # 动态id
    dynamic_info_id = models.DynamicInfo.objects.get(id=1)
    # 点赞者id
    praises_id = 5
    # 发布者id
    publisher_id = 1
    likes = Likes(
        dynamic_info=dynamic_info_id,
        praises_id=praises_id,
        publisher_id=publisher_id,
    )
    likes.save()

    return HttpResponse("like_process")


def like(request):
    dynamic_id = request.GET['dynamic_id']  # 动态id
    dynamic = models.DynamicInfo.objects.get(id=dynamic_id)  # 根据动态id得到动态信息
    dynamic_user = dynamic.user  # 动态发布者id
    user = request.session.get('user', None)

    if not user:
        return redirect('/user/login')
    # 判断用户是否点赞过该动态 如果点赞过 再次点击将会取消点赞 并通知用户
    like_or_not = models.Likes.objects.filter(
        Q(dynamic_info=dynamic) & Q(praises_id=user.id) & Q(publisher_id=dynamic.id)).first()
    if like_or_not:
        # 取消点赞后 总点赞数减一
        dynamic.dynamic_likes = dynamic.dynamic_likes - 1
        dynamic.like_status = None
        dynamic.save()
        like_or_not.delete()
        notice_content_for_unlike = user.user_name + "对你编号为" + dynamic_id + "的动态取消了点赞"
        now = datetime.datetime.now()
        notice_for_unlike = Notice(
            user=dynamic_user,
            notice_status='未读',
            notice_content=notice_content_for_unlike,
            notice_time = now,
        )
        notice_for_unlike.save()
        return HttpResponse("取消点赞")
    now = datetime.datetime.now()
    likes = Likes(
        dynamic_info=dynamic,
        praises_id=user.id,
        publisher_id=dynamic.id,
        likes_time=now,
    )
    # 点赞后总点赞数加1
    dynamic.dynamic_likes = dynamic.dynamic_likes + 1
    dynamic.like_status = user.id
    dynamic.save()
    # 给用户发送通知
    notice_content_for_like = user.user_name + "点赞了你编号为" + dynamic_id + "的动态"
    notice_for_like = Notice(
        user=dynamic_user,
        notice_status='未读',
        notice_content=notice_content_for_like,
        notice_time=now,
    )
    notice_for_like.save()

    likes.save()

    return HttpResponse("点赞成功")


# 问题模块---------------------------------------------------------------
def question_area(request):
    user = request.session.get('user', None)
    # 用户如果没有登录 跳转到登录界面
    if not user:
        return redirect('/user/login')
    my_notices = models.Notice.objects.filter(Q(user=user) & Q(notice_status='未读')).count()
    # 加载所有用户提出的问题
    all_replies = {}
    questions_info = models.Question.objects.all().order_by("-question_time")
    for question in questions_info:
        # 得到每个问题的所有回复
        replies = models.ReplyQuestion.objects.filter(question=question)

        # 得到每条问题的回复数
        reply_number = models.ReplyQuestion.objects.filter(question=question).count()
        question.question_replies = reply_number

        question.save()
        all_replies[question.id] = replies

    for question in questions_info:
        print(question.question_content)
    return render(request, "question_manage/question_area.html",
                  {"question_info": questions_info, "notices": my_notices, "user": user, "all_replies": all_replies})
# 分享问题
def delete_question(request):
    question_id = request.GET['question_id']
    question = models.Question.objects.get(id=question_id)
    question.delete()
    return HttpResponse("删除问题成功")
# 分享问题
def question_share(request):
    question_id = request.GET['question_id']
    question = models.Question.objects.get(id=question_id)
    return render(request,"question_manage/question_share.html",{"question":question})
def question_info(request):
    user = models.User.objects.get(id=1)
    question_content = request.POST['question_content']
    question_img = request.FILES['question_img']
    question = Question(
        user=user,
        question_content=question_content,
        question_img=question_img,
    )

    question.save()
    return HttpResponse("question_info")


def personal_question_info(request):
    user = request.session.get('user', None)
    # 用户如果没有登录 跳转到登录界面
    if not user:
        return redirect('/user/login')
    my_notices = models.Notice.objects.filter(Q(user=user) & Q(notice_status='未读')).count()
    my_question_info = models.Question.objects.filter(user=user).order_by("-question_time")
    # 加载所有用户提出的问题
    all_replies = {}

    for question in my_question_info:
        # 得到每个问题的所有回复
        replies = models.ReplyQuestion.objects.filter(question=question)

        # 得到每条问题的回复数
        reply_number = models.ReplyQuestion.objects.filter(question=question).count()
        question.question_replies = reply_number

        question.save()
        all_replies[question.id] = replies
    for question in my_question_info:
        print(question.question_content)
    return render(request, "question_manage/personal_question_info.html",
                  {"question_info": my_question_info, "notices": my_notices, "user": user, "all_replies": all_replies})


def my_reply(request):
    user = request.session.get('user', None)
    # 用户如果没有登录 跳转到登录界面
    if not user:
        return redirect('/user/login')

    my_notices = models.Notice.objects.filter(Q(user=user) & Q(notice_status='未读')).count()
    reply_question_info = models.ReplyQuestion.objects.filter(responses_id=user.id)

    return render(request, "question_manage/my_reply.html",
                  {"reply_question_info": reply_question_info, "notices": my_notices, "user": user})


def question_reply(request):
    user = request.session.get('user', None)
    # 用户如果没有登录 跳转到登录界面
    if not user:
        return redirect('/user/login')
    question = models.Question.objects.get(id=1)
    # 回复者id
    responses_id = 5
    reply_content = request.POST['reply_content']
    reply_img = None
    # 为防止用户没有上传图片而出现异常 这里进行捕获 用户上传图片是可选的
    try:
        reply_img = request.FILES['reply_img']
    except Exception as e:
        logging.info(e)
        print("用户没有上传图片")
    if reply_img is None:
        reply_img = None
    print('--' * 50)
    print(reply_img)
    print(type(reply_img))
    print('--' * 50)
    if reply_img is None:
        reply_img = None
    now = datetime.datetime.now()
    reply_question = ReplyQuestion(
        question=question,
        responses_id=responses_id,
        reply_content=reply_content,
        reply_img=reply_img,
        reply_time=now,
    )
    reply_question.save()
    return HttpResponse("question_reply")


def submit_reply(request):
    user = request.session.get('user', None)
    if not user:  # 用户未被登录
        print("#" * 50)
        print('not login!')
        return redirect("/user/login")
    # 'data': {question_id: question_id, user_reply: user_reply},
    question_id = request.POST['question_id']
    print(question_id)
    user_reply = request.POST['user_reply']
    # print('You enter the method of submit_reply')
    question = models.Question.objects.get(id=question_id)
    # 回复者id
    responses_id = user.id
    # 回复者姓名
    responses_name = user.user_name
    # 回复者头像
    responses_img = user.user_img
    now = datetime.datetime.now()
    reply_question = ReplyQuestion(
        question=question,
        responses_id=responses_id,
        responses_name=responses_name,
        responses_img=responses_img,
        reply_content=user_reply,
        reply_time=now
    )
    reply_question.save()
    notice_content = user.user_name + '回复了你编号为' + str(question.id) + "的问题"
    notice_for_reply = Notice(
        user=question.user,
        notice_status='未读',
        notice_content=notice_content,
        notice_time=now,
    )
    notice_for_reply.save()
    notice_two = models.Notice.objects.filter(Q(user=user) & Q(notice_status='未读')).count()
    # 按照时间从大到小排序
    questions_info = models.Question.objects.all().order_by("-question_time")
    all_replies = {}
    # 获得当前系统时间
    now = datetime.datetime.now()
    for question in questions_info:
        # 得到每个问题的所有回复
        replies = models.ReplyQuestion.objects.filter(question=question)

        # 得到每条问题的回复数
        reply_number = models.ReplyQuestion.objects.filter(question=question).count()
        question.question_replies = reply_number

        question.save()
        all_replies[question.id] = replies
    return render(request, "question_manage/question_area.html",
                  {"question_info": questions_info, "notices": notice_two, "user": user, "all_replies": all_replies,
                   "now": now})


def submit_question(request):
    user = request.session.get('user', None)
    # 用户如果没有登录 跳转到登录界面
    if not user:
        return redirect('/user/login')
    # my_notice = models.Notice.objects.filter(user=user).count()
    my_notices = models.Notice.objects.filter(Q(user=user) & Q(notice_status='未读')).count()

    return render(request, "question_manage/submit_question.html", {"notices": my_notices, "user": user})


def submit_question_process(request):
    user = request.session.get('user', None)
    # 用户如果没有登录 跳转到登录界面
    if not user:
        return redirect('/user/login')
    # my_notice = models.Notice.objects.filter(user=user).count()
    my_notices = models.Notice.objects.filter(Q(user=user) & Q(notice_status='未读')).count()

    question_content = request.POST['question_content']
    question_img = None
    # 为防止用户没有上传图片而出现异常 这里进行捕获 用户上传图片是可选的
    try:
        question_img = request.FILES['question_img']
    except Exception as e:
        logging.info(e)
        print("用户没有上传图片")

    if question_img is None:
        question_img = None
    now = datetime.datetime.now()
    question = Question(
        user=user,
        question_content=question_content,
        question_img=question_img,
        question_time=now,
    )

    question.save()
    return render(request, "question_manage/submit_question_success.html", {"notices": my_notices, "user": user})


# 通知模块-----------------------------------------------------------------------------------------

# 查看我的通知
def my_notice(request):
    user = request.session.get('user', None)
    # 用户如果没有登录 跳转到登录界面
    if not user:
        return redirect('/user/login')
    page_index = None

    try:

        page_index = request.GET['page_index']
    except Exception as e:
        logging.info(e)

    if page_index is None:
        page_index = 1

    else:
        if page_index != "":
            page_index = int(page_index)
        else:
            page_index = 1

    # 共几页
    # unread_pages = paginator_for_notice.num_pages

    my_notices_info = models.Notice.objects.filter(Q(user=user))
    paginator_for_read_notice = Paginator(my_notices_info, 5)

    page_info = paginator_for_read_notice.page(page_index)

    # 未读通知数目
    my_notice_count = models.Notice.objects.filter(Q(user=user) & Q(notice_status='未读')).count()

    return render(request, "notice_manage/my_notice.html",
                  {"user": user
                      , "notices": my_notice_count
                      , "notice_info": page_info
                   })


# 将通知设置为已读
def notice_set_for_read(request):
    user = request.session.get('user', None)
    # 用户如果没有登录 跳转到登录界面
    if not user:
        return redirect('/user/login')
    notice_id = request.GET['notice_id']
    notice = models.Notice.objects.get(id=notice_id)
    notice.notice_status = '已读'
    notice.save()

    return HttpResponse("设置成功")


def delete_notice(request):
    user = request.session.get('user', None)
    # 用户如果没有登录 跳转到登录界面
    if not user:
        return redirect('/user/login')
    notice_id = request.GET['notice_id']
    notice = models.Notice.objects.get(id=notice_id)
    notice.delete()

    return HttpResponse("删除成功")


def get_code(request):
    code = ''
    # 发送4位验证码
    for num in range(1, 5):
        code = code + str(random.randint(0, 9))
    print(code)
    client = smsclient.ZhenziSmsClient('http://sms_developer.zhenzikj.com', '100931',
                                       'ca7f2b7c-1778-4ef4-abc9-fa0206f499eb')

    uinfo = {}
    hd_user_name = ""
    hd_user_phone = request.POST['hd_user_phone']
    print(client.send(hd_user_phone, '校园咨询网站欢迎您注册，您的验证码为' + code))
    hd_user_password = ""
    hd_user_email = ""
    uinfo['valid_code'] = code

    try:
        # 对于get来讲 不安全 建议使用POST 创建一个隐形的表单

        hd_user_name = request.POST['hd_user_name']

        hd_user_password = request.POST['hd_user_password']
        hd_user_email = request.POST['hd_user_email']
        # user_name = request.GET['user_name']
        uinfo['user_name'] = hd_user_name
        uinfo['user_phone'] = hd_user_phone
        uinfo['user_password'] = hd_user_password
        uinfo['user_email'] = hd_user_email
        # uinfo['user_name'] = user_name
    except Exception as e:
        logging.info(e)

    # return render(request, "admin_main_page.html",{"user_phone":hd_user_phone})
    return render(request, "login_register/register.html", uinfo)
    # 此处若使用重定向会导致数据无法再次载入
    # return redirect("/user/register")


# 资源管理-------------------------------------------------------------------------------------------------

def my_resource(request):
    user = request.session.get('user', None)
    # 用户如果没有登录 跳转到登录界面
    if not user:
        return redirect('/user/login')
    notice_five = models.Notice.objects.filter(Q(user=user) & Q(notice_status='未读')).count()
    # 得到所有文件
    all_resource = models.Resource.objects.filter(user=user)
    # 得到txt文件
    txt_resource = models.Resource.objects.filter(Q(user=user) & Q(resource_name__contains='.txt'))
    # 得到doc文件
    doc_resource = models.Resource.objects.filter(Q(user=user) & Q(resource_name__contains='.doc'))
    # 得到xls文件
    xls_resource = models.Resource.objects.filter(Q(user=user) & Q(resource_name__contains='.xls'))
    # 得到ppt文件
    ppt_resource = models.Resource.objects.filter(Q(user=user) & Q(resource_name__contains='.ppt'))
    # 得到pdf文件
    pdf_resource = models.Resource.objects.filter(Q(user=user) & Q(resource_name__contains='.pdf'))
    # 得到其他文件
    other_resource = models.Resource.objects.filter(~Q(
        Q(resource_name__icontains='.txt') | Q(resource_name__icontains='.doc') | Q(
            resource_name__icontains='.xls') | Q(resource_name__icontains='.ppt') | Q(
            resource_name__icontains='.pdf')) & Q(user=user))

    return render(request, "resource_manage/my_resource.html",
                  {"notices": notice_five,
                   "user": user,
                   "all_resource": all_resource,
                   "txt_resource": txt_resource,
                   "doc_resource": doc_resource,
                   "xls_resource": xls_resource,
                   "ppt_resource": ppt_resource,
                   "pdf_resource": pdf_resource,
                   "other_resource": other_resource,
                   "my_resource_flag": "YES",  # 当前页面是我的资源页面
                   })


def search_resource(request):
    user = request.session.get('user', None)
    # 用户如果没有登录 跳转到登录界面
    if not user:
        return redirect('/user/login')
    notice_five = models.Notice.objects.filter(Q(user=user) & Q(notice_status='未读')).count()
    resource_name = request.GET['resource_name']
    page_type = request.GET['page_type']
    page_template = "resource_manage/my_resource.html"
    search_result = models.Resource.objects.filter(Q(resource_name__contains=resource_name) & Q(user=user))
    if page_type == "资源广场":
        print('------+++++++++++++++++++++++++++++++++++++++++——————————————————————————————————————')
        page_template = "resource_manage/download_resource_area.html"
        search_result = models.Resource.objects.filter(
            Q(resource_name__contains=resource_name) & Q(resource_status='已审核'))
    # 得到所有文件
    all_resource = models.Resource.objects.filter(resource_status='已审核')
    # 搜索结果

    return render(request, page_template,
                  {"notices": notice_five,
                   "user": user,
                   "all_resource": all_resource,
                   "search_result": search_result,
                   "search_resource_flag": "YES"  # 进行资源搜索后的结果
                   })


def upload_resource(request):
    user = request.session.get('user', None)
    # 用户如果没有登录 跳转到登录界面
    if not user:
        return redirect('/user/login')
    notice_five = models.Notice.objects.filter(Q(user=user) & Q(notice_status='未读')).count()

    return render(request, "resource_manage/upload_resource.html",
                  {"notices": notice_five, "user": user})


def upload_resource_process(request):
    user = request.session.get('user', None)
    # 用户如果没有登录 跳转到登录界面
    if not user:
        return redirect('/user/login')
    notice_five = models.Notice.objects.filter(Q(user=user) & Q(notice_status='未读')).count()
    files_count = request.POST['files_count']
    resource_type = request.POST['resource_type']
    print('file_count---------->%s' % files_count)
    now = datetime.datetime.now()
    for i in range(int(files_count)):
        resource_file = request.FILES['file' + str(i)]
        resource = Resource(
            user=user,
            resource_type=resource_type,
            resource_name=resource_file,
            resource_file=resource_file,
            resource_status='待审核',
            submit_time=now,

        )
        resource.save()
        print(resource_file)
    print('*' * 50)

    print("uploading--------------------------------------------")
    return render(request, "resource_manage/upload_resource.html",
                  {"notices": notice_five, "user": user})


# 资源广场 download_resource_area
def download_resource_area(request):
    user = request.session.get('user', None)
    # 用户如果没有登录 跳转到登录界面
    if not user:
        return redirect('/user/login')
    notice_six = models.Notice.objects.filter(Q(user=user) & Q(notice_status='未读')).count()
    # 得到所有文件
    all_resource = models.Resource.objects.filter(resource_status='已审核')
    # 得到txt文件
    txt_resource = models.Resource.objects.filter(Q(resource_name__contains='.txt') & Q(resource_status='已审核'))
    # 得到doc文件
    doc_resource = models.Resource.objects.filter(Q(resource_name__contains='.doc') & Q(resource_status='已审核'))
    # 得到xls文件
    xls_resource = models.Resource.objects.filter(Q(resource_name__contains='.xls') & Q(resource_status='已审核'))
    # 得到ppt文件
    ppt_resource = models.Resource.objects.filter(Q(resource_name__contains='.ppt') & Q(resource_status='已审核'))
    # 得到pdf文件
    pdf_resource = models.Resource.objects.filter(Q(resource_name__contains='.pdf') & Q(resource_status='已审核'))
    # 得到其他文件
    other_resource = models.Resource.objects.filter(~Q(
        Q(resource_name__icontains='.txt') | Q(resource_name__icontains='.doc') | Q(
            resource_name__icontains='.xls') | Q(resource_name__icontains='.ppt') | Q(
            resource_name__icontains='.pdf')) & Q(resource_status='已审核'))

    return render(request, "resource_manage/download_resource_area.html",
                  {"notices": notice_six,
                   "user": user,
                   "all_resource": all_resource,
                   "txt_resource": txt_resource,
                   "doc_resource": doc_resource,
                   "xls_resource": xls_resource,
                   "ppt_resource": ppt_resource,
                   "pdf_resource": pdf_resource,
                   "other_resource": other_resource,
                   "all_resource_flag": "YES",
                   })


def audit_resource(request):
    resource_id = request.GET['resource_id']
    resource = models.Resource.objects.get(id=resource_id)
    resource.resource_status = '已审核'
    resource.save()
    return HttpResponse("资源审核成功")


# 删除资源
def delete_resource(request):
    resource_id = request.GET['resource_id']
    resource = models.Resource.objects.get(id=resource_id)
    resource.delete()
    return HttpResponse("删除资源成功")


# 下载资源
def download_resource(request):
    # do something
    the_file_name = request.GET['file_name']
    # 显示在弹出对话框中的默认的下载文件名
    print('the_file_name--------->' + the_file_name)
    filename = 'media/resource/' + the_file_name  # 要下载的文件路径
    print('filename--------------->' + filename)

    response = StreamingHttpResponse(readFile(filename))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response


def readFile(filename, chunk_size=512):
    with open(filename, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


# 新闻管理 ----------------------------------------------------------------------------------
def school_news(request):
    user = request.session.get('user', None)
    # 用户如果没有登录 跳转到登录界面
    if not user:
        return redirect('/user/login')
    school_new = models.News.objects.all()
    my_notices = models.Notice.objects.filter(Q(user=user) & Q(notice_status='未读')).count()

    return render(request, "school_news/school_news.html", {"notices": my_notices, "user": user, "school_news": school_new})


# 聊天机器人----------------------------------------------------------------------------------
def chat_page(request):
    user = request.session.get('user', None)
    # 用户如果没有登录 跳转到登录界面
    if not user:
        return redirect('/user/login')
    # my_notice = models.Notice.objects.filter(user=user).count()
    my_notices = models.Notice.objects.filter(Q(user=user) & Q(notice_status='未读')).count()

    return render(request, "chat_bot/chat_page.html", {"notices": my_notices, "user": user})


def chat_page_component(request):
    return render(request, "chat_bot/chat_page_component.html")

    # 修改密码-----------------------------------------------------------------


def change_password(request):
    user = request.session.get('user', None)
    # 用户如果没有登录 跳转到登录界面
    if not user:
        return redirect('/user/login')
    notice_three = models.Notice.objects.filter(Q(user=user) & Q(notice_status='未读')).count()

    return render(request, "user_info_manage/change_password.html", {"notices": notice_three, "user": user})


def change_password_process(request):
    user = request.session.get('user', None)
    # 用户如果没有登录 跳转到登录界面
    if not user:
        return redirect('/user/login')
    notice_three = models.Notice.objects.filter(Q(user=user) & Q(notice_status='未读')).count()
    hint = ""
    print("+++++++++++++++++++++++++++")
    old_password = request.POST['old_password']
    new_password = request.POST['new_password']
    if user.user_password != old_password:
        hint = "原始密码错误"
    else:
        user.user_password = new_password
        hint = "修改成功，请重新登录"
        user.save()
    return render(request, "user_info_manage/change_password.html", {"notices": notice_three, "user": user, "hint": hint})


# -------------------------------------------------------修改头像
def change_user_img(request):
    user = request.session.get('user', None)
    # 用户如果没有登录 跳转到登录界面
    if not user:
        return redirect('/user/login')
    notice_three = models.Notice.objects.filter(Q(user=user) & Q(notice_status='未读')).count()
    return render(request, "user_info_manage/change_user_img.html", {"notices": notice_three, "user": user})


def change_user_img_process(request):
    user = request.session.get('user', None)
    # 用户如果没有登录 跳转到登录界面
    if not user:
        return redirect('/user/login')

    notice_three = models.Notice.objects.filter(Q(user=user) & Q(notice_status='未读')).count()
    user_img = request.FILES['user_img']
    user.user_img = user_img
    user.save()
    # 修改图片 先将之前的session清除掉 再设置新的session
    request.session.clear()
    request.session['user'] = user

    hints = "修改成功"
    return render(request, "user_info_manage/change_user_img.html", {"notices": notice_three, "user": user, "hint": hints})


# 修改密码后重新登录
def login_again(request):
    # 将session销毁
    request.session.clear()
    return render(request, "login_register/login.html")


#  评论点赞--------------------------------------------------------------------------------------------
# 我的评论 我的点赞

def my_comment(request):
    user = request.session.get('user', None)
    # 用户如果没有登录 跳转到登录界面
    if not user:
        return redirect('/user/login')

    notice_three = models.Notice.objects.filter(Q(user=user) & Q(notice_status='未读')).count()

    comments = models.Comments.objects.filter(critic_id=user.id).order_by("-comment_time")

    return render(request, "comment_manage/my_comment.html", {"notices": notice_three, "user": user, "comments": comments})


def my_like(request):
    user = request.session.get('user', None)
    # 用户如果没有登录 跳转到登录界面
    if not user:
        return redirect('/user/login')

    notice_three = models.Notice.objects.filter(Q(user=user) & Q(notice_status='未读')).count()


    likes = models.Likes.objects.filter(praises_id=user.id).order_by("-likes_time")

    return render(request, "like_manage/my_like.html", {"notices": notice_three, "user": user, "likes": likes})


# 退出系统 -----------------------------------------------------------------------------------
def exit(request):
    # 将session销毁
    request.session.clear()
    all_places = models.Place.objects.all()

    return render(request, "index/index.html", {"all_places": all_places})


# admin-----------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------
# Admin--------------------------------------------------------------------------------------------------

def admin_index(request):
    # 查看是否登录若没登录则回到登录界面
    admin = request.session.get('admin', None)
    if not admin:
        return redirect('/user/login')
    page_index = None

    try:

        page_index = request.GET['page_index']
    except Exception as e:
        logging.info(e)

    if page_index is None:
        page_index = 1

    else:
        if page_index != "":
            page_index = int(page_index)
        else:
            page_index = 1
    all_user = models.User.objects.all()
    users = Paginator(all_user, 3)
    page_info = users.page(page_index)

    return render(request, "admin/admin_main_page.html", {"all_user": page_info, "admin": admin})


# 用户管理--------------------------------------------------------------------------------------------------
# 冻结用户
def freeze_user(request):
    user_id = request.POST['user_id']
    user = models.User.objects.get(id=user_id)
    user.user_state = "已冻结"
    print("freeze_user method")
    user.save()
    return HttpResponse("已冻结")


# 用户解冻
def unfreeze_user(request):
    user_id = request.POST['user_id']
    user = models.User.objects.get(id=user_id)
    user.user_state = "正常"
    user.save()
    print("unfreeze_user method")
    return HttpResponse("解冻成功 ")


# 删除用户
def delete_user(request):
    user_id = request.POST['user_id']
    user = models.User.objects.get(id=user_id)
    user.delete()
    print("delete_user method")
    return HttpResponse("删除用户")


# --------------------------------------------------------------------资源管理
def resource_manage(request):
    admin = request.session.get('admin', None)
    if not admin:
        return redirect('/user/login')
    page_index = None

    try:

        page_index = request.GET['page_index']
    except Exception as e:
        logging.info(e)

    if page_index is None:
        page_index = 1

    else:
        if page_index != "":
            page_index = int(page_index)
        else:
            page_index = 1

    all_resource = models.Resource.objects.all()
    resources = Paginator(all_resource, 3)
    page_info = resources.page(page_index)

    print(all_resource.count())
    return render(request, "admin/resource_manage/resource_manage.html", {"admin": admin, "all_resource": page_info})


# ------------------------------------------------------------------地图标注管理
# 查看版块
def check_dynamic_topic(request):
    # 查看是否登录若没登录则回到登录界面
    admin = request.session.get('admin', None)
    if not admin:
        return redirect('/user/login')
    page_index = None

    try:

        page_index = request.GET['page_index']
    except Exception as e:
        logging.info(e)

    if page_index is None:
        page_index = 1

    else:
        if page_index != "":
            page_index = int(page_index)
        else:
            page_index = 1
    dynamic_tops = models.DynamicTopic.objects.all()
    dynamic_topics = Paginator(dynamic_tops, 3)
    page_info = dynamic_topics.page(page_index)
    return render(request, "admin/dynamic_topic/check_dynamic_top.html", {"admin": admin, "dynamic_tops": page_info})


# ---------------------------------------------------------------------------版块管理
# 添加版块
def add_dynamic_topic(request):
    # 查看是否登录若没登录则回到登录界面
    admin = request.session.get('admin', None)
    if not admin:
        return redirect('/user/login')
    return render(request, "admin/dynamic_topic/add_dynamic_top.html", {"admin": admin})


def add_dynamic_topic_process(request):
    # 查看是否登录若没登录则回到登录界面
    admin = request.session.get('admin', None)
    if not admin:
        return redirect('/user/login')
    topic_content = request.POST['topic_content']
    dynamic_topic_judge = models.DynamicTopic.objects.filter(topic_content=topic_content)
    if dynamic_topic_judge:
        return render(request, "admin/dynamic_topic/add_dynamic_top.html", {"admin": admin, "hint": "topic exist"})
    now = datetime.datetime.now()
    dynamic_topic = DynamicTopic(
        topic_content=topic_content,
        topic_create_time = now,

    )
    dynamic_topic.save()
    return render(request, "admin/dynamic_topic/add_dynamic_top_success.html", {"admin": admin})


# 删除版块
def delete_dynamic_topic(request):
    dynamic_topic_id = request.POST['dynamic_topic_id']
    dynamic_topic = models.DynamicTopic.objects.get(id=dynamic_topic_id)
    dynamic_topic.delete()
    return HttpResponse("删除成功")


# --------------------------------------------------------------------------标注管理
# 查看标注
def check_map_label(request):
    # 查看是否登录若没登录则回到登录界面
    admin = request.session.get('admin', None)
    if not admin:
        return redirect('/user/login')
    page_index = None

    try:

        page_index = request.GET['page_index']
    except Exception as e:
        logging.info(e)

    if page_index is None:
        page_index = 1

    else:
        if page_index != "":
            page_index = int(page_index)
        else:
            page_index = 1
    all_places = models.Place.objects.all()
    places = Paginator(all_places, 3)
    page_info = places.page(page_index)

    print("check-------------------->")
    return render(request, "admin/map_label/check_map_label.html", {"all_places": page_info, "admin": admin})


# 添加标注
def add_map_label(request):
    # 查看是否登录若没登录则回到登录界面
    admin = request.session.get('admin', None)
    if not admin:
        return redirect('/user/login')
    all_places = models.Place.objects.all()
    return render(request, "admin/map_label/add_map_label.html", {"all_places": all_places, "admin": admin})


def add_map_label_process(request):
    admin = request.session.get('admin', None)
    if not admin:
        return redirect('/user/login')
    place_name = request.POST['label_name']
    longitude = request.POST['longitude']
    latitude = request.POST['latitude']
    vertical_angle = request.POST['vertical_angle']
    horizontal_angle = request.POST['horizontal_angle']
    now = datetime.datetime.now()
    place = Place(
        place_name=place_name,
        longitude=longitude,
        latitude=latitude,
        label_height=3,
        vertical_angle=vertical_angle,
        horizontal_angle=horizontal_angle,
        submit_time=now,
    )
    place.save()
    all_places = models.Place.objects.all()
    return render(request, "admin/map_label/add_map_label.html", {"all_places": all_places, "admin": admin})


# 删除标注
def delete_map_label(request):
    place_id = request.POST['place_id']
    place = models.Place.objects.get(id=place_id)
    place.delete()
    return HttpResponse("删除成功")


# ----------------------------------------------------------------------新闻管理
def check_school_news(request):
    # 查看是否登录若没登录则回到登录界面
    admin = request.session.get('admin', None)
    if not admin:
        return redirect('/user/login')
    all_news = models.News.objects.all()
    return render(request, "admin/school_news/check_school_news.html", {"admin": admin, "all_news": all_news})


def submit_school_news(request):
    # 查看是否登录若没登录则回到登录界面
    admin = request.session.get('admin', None)
    if not admin:
        return redirect('/user/login')

    return render(request, "admin/school_news/submit_school_news.html", {"admin": admin})


def submit_school_news_process(request):
    admin = request.session.get('admin', None)
    if not admin:
        return redirect('/user/login')
    news_title = request.POST['news_title']
    news_content = request.POST['news_content']
    news_img = None
    # 为防止用户没有上传图片而出现异常 这里进行捕获 用户上传图片是可选的
    try:
        news_img = request.FILES['news_img']
    except Exception as e:
        logging.info(e)
        print("没有上传图片")

    if news_img is None:
        news_img = None
    now = datetime.datetime.now()
    news = News(
        news_title=news_title,
        news_content=news_content,
        news_img=news_img,
        news_views=0,
        news_time=now,

    )
    news.save()
    return render(request, "admin/school_news/submit_school_news_success.html", {"admin": admin})


# 删除新闻
def delete_news(request):
    news_id = request.POST['news_id']
    news = models.News.objects.get(id=news_id)
    news.delete()
    return HttpResponse("删除成功")


# -------------------------------------------------------------------账户密码修改

def change_admin_img(request):
    # 查看是否登录若没登录则回到登录界面
    admin = request.session.get('admin', None)
    if not admin:
        return redirect('/user/login')

    return render(request, "admin/admin_info/change_admin_img.html", {"admin": admin})


def change_admin_img_process(request):
    admin = request.session.get('admin', None)
    # 用户如果没有登录 跳转到登录界面
    if not admin:
        return redirect('/admin/login')

    admin_img = request.FILES['admin_img']
    admin.admin_img = admin_img
    admin.save()
    # 修改图片 先将之前的session清除掉 再设置新的session
    request.session.clear()
    request.session['admin'] = admin

    hints = "修改成功"
    return render(request, "admin/admin_info/change_admin_img.html", {"admin": admin, "hint": hints})


# 修改密码
def change_admin_password(request):
    admin = request.session.get('admin', None)
    # 用户如果没有登录 跳转到登录界面
    if not admin:
        return redirect('/admin/login')

    return render(request, "admin/admin_info/change_admin_password.html", {"admin": admin})


def change_admin_password_process(request):
    admin = request.session.get('admin', None)
    # 用户如果没有登录 跳转到登录界面
    if not admin:
        return redirect('/admin/login')

    hint = ""
    print("+++++++++++++++++++++++++++")
    old_password = request.POST['old_password']
    new_password = request.POST['new_password']
    if admin.admin_password != old_password:
        hint = "原始密码错误"
    else:
        admin.admin_password = new_password
        hint = "修改成功，请重新登录"
        admin.save()
    return render(request, "admin/admin_info/change_admin_password.html", {"admin": admin, "hint": hint})
