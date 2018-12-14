from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view()),
    url(r'^articles/(?P<pk>\d+)', views.DetailView.as_view()),
    url(r'^articles/$', views.DetailView.as_view()),
    url(r'^categories/(?P<category_name>\w+)$', views.CategoryView.as_view()),
    url(r'^tags/(?P<tag_name>\w+)$', views.TagView.as_view()),
    url(r'^searches/(?P<keyword>\w+)$', views.SearchView.as_view()),
    url(r'^searches/$', views.SearchView.as_view()),
]

