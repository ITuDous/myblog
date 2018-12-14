from django.conf.urls import url

from . import views

app_name = 'comment'
urlpatterns = [
    url(r'^article/(?P<pk>\d+)$', views.article_comment, name='article_comment'),
]

