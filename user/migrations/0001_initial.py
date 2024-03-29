# Generated by Django 2.1.4 on 2019-05-04 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('admin_name', models.CharField(max_length=30)),
                ('admin_phone', models.CharField(max_length=20)),
                ('admin_password', models.CharField(max_length=30)),
                ('admin_email', models.CharField(max_length=30)),
                ('admin_img', models.ImageField(null=True, upload_to='img')),
            ],
            options={
                'db_table': 'admin',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('critic_id', models.IntegerField()),
                ('critic_name', models.CharField(max_length=30)),
                ('critic_img', models.ImageField(null=True, upload_to='img')),
                ('publisher_id', models.IntegerField()),
                ('comment_content', models.CharField(max_length=400)),
                ('comment_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'comments',
            },
        ),
        migrations.CreateModel(
            name='DynamicInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dynamic_content', models.CharField(max_length=400)),
                ('dynamic_img', models.ImageField(null=True, upload_to='img')),
                ('dynamic_time', models.DateTimeField(auto_now=True)),
                ('like_status', models.IntegerField(null=True)),
                ('dynamic_likes', models.IntegerField()),
                ('dynamic_comments', models.IntegerField()),
            ],
            options={
                'db_table': 'dynamic_info',
            },
        ),
        migrations.CreateModel(
            name='DynamicTopic',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('topic_content', models.CharField(max_length=100)),
                ('topic_create_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'dynamic_topic',
            },
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('praises_id', models.IntegerField()),
                ('publisher_id', models.IntegerField()),
                ('likes_time', models.DateTimeField(auto_now=True)),
                ('dynamic_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.DynamicInfo')),
            ],
            options={
                'db_table': 'likes',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('news_title', models.CharField(max_length=200)),
                ('news_content', models.CharField(max_length=1600)),
                ('news_img', models.ImageField(null=True, upload_to='')),
                ('news_views', models.IntegerField()),
                ('news_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('notice_content', models.CharField(max_length=400)),
                ('notice_status', models.CharField(max_length=20)),
                ('notice_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'notice',
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('place_name', models.CharField(max_length=400)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('label_height', models.IntegerField()),
                ('vertical_angle', models.FloatField()),
                ('horizontal_angle', models.FloatField()),
                ('submit_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'place',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('question_content', models.CharField(max_length=400)),
                ('question_img', models.ImageField(null=True, upload_to='img')),
                ('question_replies', models.IntegerField(default=0)),
                ('question_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'question',
            },
        ),
        migrations.CreateModel(
            name='ReplyQuestion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('responses_id', models.IntegerField()),
                ('reply_content', models.CharField(max_length=400)),
                ('responses_name', models.CharField(max_length=30)),
                ('responses_img', models.ImageField(null=True, upload_to='img')),
                ('reply_time', models.DateTimeField(auto_now=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Question')),
            ],
            options={
                'db_table': 'reply_question',
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('resource_type', models.CharField(max_length=400)),
                ('resource_name', models.CharField(max_length=400)),
                ('resource_file', models.FileField(null=True, upload_to='resource')),
                ('resource_status', models.CharField(max_length=30)),
                ('submit_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'resource',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=30)),
                ('user_phone', models.CharField(max_length=20)),
                ('user_sex', models.CharField(max_length=4, null=True)),
                ('user_password', models.CharField(max_length=30)),
                ('user_email', models.CharField(max_length=30)),
                ('user_description', models.CharField(max_length=200, null=True)),
                ('user_state', models.CharField(max_length=20)),
                ('user_img', models.ImageField(null=True, upload_to='img')),
                ('last_login_time', models.DateTimeField(null=True)),
                ('register_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.AddField(
            model_name='resource',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
        migrations.AddField(
            model_name='question',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
        migrations.AddField(
            model_name='notice',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
        migrations.AddField(
            model_name='dynamicinfo',
            name='dynamic_topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.DynamicTopic'),
        ),
        migrations.AddField(
            model_name='dynamicinfo',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
        migrations.AddField(
            model_name='comments',
            name='dynamic_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.DynamicInfo'),
        ),
    ]
