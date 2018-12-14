from django.db import models

from blog.models import Article


# Create your models here.
class Comment(models.Model):
    name = models.CharField(max_length=30, verbose_name='用户名')
    email = models.EmailField(verbose_name='邮箱')
    content = models.TextField(verbose_name='评论')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    article = models.ForeignKey(Article)

    class Meta:
        verbose_name = '用户评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content[:5]
