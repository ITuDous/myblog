# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-13 16:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_created=True, verbose_name='创建日期')),
                ('name', models.CharField(max_length=30, verbose_name='用户名')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('content', models.TextField(verbose_name='评论')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Article')),
            ],
            options={
                'verbose_name': '用户评论',
                'verbose_name_plural': '用户评论',
            },
        ),
    ]
