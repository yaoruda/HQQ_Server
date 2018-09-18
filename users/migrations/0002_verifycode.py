# Generated by Django 2.1.1 on 2018-09-17 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VerifyCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=8, verbose_name='验证码')),
                ('expires', models.TimeField(auto_now=True, verbose_name='短信验证码创建时间')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='loginphonemessage', to='users.MyUser', verbose_name='外键用户id')),
            ],
        ),
    ]
