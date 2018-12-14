from django.db import models

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=8)
    other_name = models.CharField(max_length=32)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=50)
    abstract = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    view = models.IntegerField(default=0)
    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        # 让文章按时间和浏览排序
        ordering=['-created_time']

    def __str__(self):
        return self.title


def get_absolute_url(self):
    return reverse('detail', kwargs={'pk': self.pk})
