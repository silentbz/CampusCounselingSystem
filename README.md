# 项目提交

1.项目git clone之后，先在pycharm下将所需安装包进行安装（requirements.txt）
2.每个人的分支为名字首拼字母
3.提交代码时，先提交至自己分支，再确认与master主分支是否有冲突，无冲突再与master主分支进行合并

# 项目必须安装包

mysqlclient、numpy、django、Pillow 
分别使用pip install 进行安装

# 项目结构

python web框架：django
数据库端：Mysql
前端：Bootstrap、Layui

# 项目部署

1.项目git clone之后<br/>
2.创建数据库compuscounseling
3.修改数据库配置，在settings.py文件中修改DATABASES属性值
4.在项目根目录下运行：python manage.py migrate
5.对应INSTALLED_APPS来生成数据库表模型：python manage.py makemigrations user

# 项目运行

运行前提条件：JDK1.8、Python3.x+

python manage.py runserver 0.0.0.0:port

port可指定

eg：python manage.py runserver 0.0.0.0:9000



