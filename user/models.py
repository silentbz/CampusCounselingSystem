from django.db import models


# 用户信息表
class User(models.Model):
    # 用户名
    user_name = models.CharField(max_length=30)
    # 用户手机号
    user_phone = models.CharField(max_length=20)
    # 用户性别
    user_sex = models.CharField(max_length=4,null=True)
    # 用户密码
    user_password = models.CharField(max_length=30)
    # 用户邮箱
    user_email = models.CharField(max_length=30)

    # 用户自我描述
    user_description = models.CharField(max_length=200,null=True)
    # 用户状态 正常 冻结
    user_state = models.CharField(max_length=20)
    # 用户头像
    user_img = models.ImageField(upload_to='img',null=True)
    # 上次登录时间
    last_login_time = models.DateTimeField(null=True)
    # 注册时间
    register_time = models.DateTimeField()

    class Meta:
        db_table = 'user'

# 动态信息表
class DynamicInfo(models.Model):
    # 动态id
    id = models.AutoField(primary_key=True)
    # 用户id
    user = models.ForeignKey(to='User',to_field='id',on_delete=models.CASCADE)
    # 版块id
    dynamic_topic = models.ForeignKey(to='DynamicTopic',to_field='id',on_delete=models.CASCADE)
    # 动态内容
    dynamic_content = models.CharField(max_length=400)
    # 图片
    dynamic_img = models.ImageField(upload_to='img',null=True)
    # 发布动态时间
    dynamic_time = models.DateTimeField()
    # 用户是否点赞
    like_status = models.IntegerField(null=True)
    # 点赞数
    dynamic_likes = models.IntegerField()
    # 评论数
    dynamic_comments = models.IntegerField()

    class Meta:
        db_table = 'dynamic_info'

# 版块信息表
class DynamicTopic(models.Model):
    # 版块id
    id = models.AutoField(primary_key=True)
    # 版块内容
    topic_content = models.CharField(max_length=100)
    # 创建时间
    topic_create_time = models.DateTimeField()

    class Meta:
        db_table = 'dynamic_topic'
# 新闻信息表
class News(models.Model):
    # 新闻id
    id = models.AutoField(primary_key=True)
    # 新闻标题
    news_title = models.CharField(max_length=200)
    # 新闻内容
    news_content = models.CharField(max_length=1600)
    # 新闻图片
    news_img = models.ImageField(null=True)
    # 浏览量
    news_views = models.IntegerField()
    # 发布时间
    news_time = models.DateTimeField()



# 评论表
class Comments(models.Model):
    # 评论id
    id = models.AutoField(primary_key=True)
    # 动态id
    dynamic_info = models.ForeignKey(to='DynamicInfo',to_field='id',on_delete=models.CASCADE)
    # 评论者id
    critic_id = models.IntegerField()
    # 评论者姓名
    critic_name = models.CharField(max_length=30)
    # 评论者头像
    critic_img =  models.ImageField(upload_to='img',null=True)
    # 动态发布者id
    publisher_id = models.IntegerField()
    # 评论内容
    comment_content = models.CharField(max_length=400)
    # 评论时间
    comment_time = models.DateTimeField()

    class Meta:
        db_table = 'comments'



# 点赞表
class Likes(models.Model):
    # 点赞id
    id = models.AutoField(primary_key=True)
    # 动态id
    dynamic_info = models.ForeignKey(to='DynamicInfo',to_field='id',on_delete=models.CASCADE)
    # 点赞者id
    # user = models.ForeignKey(to='User',to_field='id',on_delete=models.CASCADE)
    praises_id = models.IntegerField()
    # 发布者id
    publisher_id = models.IntegerField()
    # 点赞时间
    likes_time = models.DateTimeField()

    class Meta:
        db_table = 'likes'

# 问题表
class Question(models.Model):
    # 问题id
    id = models.AutoField(primary_key=True)
    # 提问者id
    user = models.ForeignKey(to='User',to_field='id',on_delete=models.CASCADE)
    # 问题内容
    question_content = models.CharField(max_length=400)
    # 问题图片
    question_img = models.ImageField(upload_to='img',null=True)
    # 问题回复数
    question_replies = models.IntegerField(default=0)
    # 问题提出时间
    question_time = models.DateTimeField()

    class Meta:
        db_table = 'question'

# 问题回复表
class ReplyQuestion(models.Model):
    # 问题回复id
    id = models.AutoField(primary_key=True)
    # 问题id
    question = models.ForeignKey(to='Question',to_field='id',on_delete=models.CASCADE)
    # 回复者id
    # user = models.ForeignKey(to='User',to_field='id',on_delete=models.CASCADE)
    responses_id = models.IntegerField()
    # 回复内容
    reply_content = models.CharField(max_length=400)
    # 回复者姓名
    responses_name = models.CharField(max_length=30)
    # 回复者头像


    responses_img = models.ImageField(upload_to='img',null=True)
    # 回复时间
    reply_time = models.DateTimeField()

    class Meta:
        db_table = 'reply_question'


# 通知表
class Notice(models.Model):
    # 通知id
    id = models.AutoField(primary_key=True)
    # 用户id
    user = models.ForeignKey(to='User',to_field='id',on_delete=models.CASCADE)
    # 通知内容
    notice_content = models.CharField(max_length=400)

    # 通知状态 未读 or 已读
    notice_status = models.CharField(max_length=20)

    # 通知时间
    notice_time = models.DateTimeField()

    class Meta:
        db_table = 'notice'
# 资源表
class Resource(models.Model):
    # 资源id
    id = models.AutoField(primary_key=True)
    # 上传用户的id
    user = models.ForeignKey(to='User',to_field='id',on_delete=models.CASCADE)
    # 资源类别
    resource_type = models.CharField(max_length=400)
    # 资源文件名
    resource_name = models.CharField(max_length=400)
    # 资源文件
    resource_file = models.FileField(upload_to='resource', null=True)
    # 资源状态
    resource_status = models.CharField(max_length=30)
    # 下载次数 默认设置为0
    #download_times = models.IntegerField(default=0)
    # 资源评分
    #resource_grade = models.IntegerField(null=True)
    # 上传时间
    submit_time = models.DateTimeField()

    class Meta:
        db_table = 'resource'

class Place(models.Model):
    # 地点id
    id = models.AutoField(primary_key=True)
    # 地点名
    place_name = models.CharField(max_length=400)
    # 经度
    longitude = models.FloatField()
    # 纬度
    latitude = models.FloatField()
    # 标签高度
    label_height = models.IntegerField()
    # 仰俯角度
    vertical_angle = models.FloatField()
    # 偏航角
    horizontal_angle = models.FloatField()
    # 创建时间
    submit_time = models.DateTimeField()

    class Meta:
        db_table = 'place'

# admin----------------------------------------------------------------------------

# 管理员信息表
class Admin(models.Model):
    # 管理员 id
    id = models.AutoField(primary_key=True)
    # 管理员名
    admin_name = models.CharField(max_length=30)
    # 管理员手机号
    admin_phone = models.CharField(max_length=20)

    # 管理员密码
    admin_password = models.CharField(max_length=30)
    # 管理员邮箱
    admin_email = models.CharField(max_length=30)


    # 管理员头像
    admin_img = models.ImageField(upload_to='img',null=True)


    class Meta:
        db_table = 'admin'






