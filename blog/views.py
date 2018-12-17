from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.views.generic import ListView

from markdown import markdown

from comment.forms import CommentForm
from .models import Article, Category, Tag


def pagintor_reuse(page_num, paginator):
    # 分页信息

    try:
        articles = paginator.page(page_num)
    except PageNotAnInteger:
        # 如果页面不是整数，返回第一页
        articles = paginator.page(1)
    except EmptyPage:
        # 如果页面超出范围，提交最后一页的结果
        articles = paginator.page(paginator.num_pages)

    return articles


def rank_info():
    # 排行信息

    articles_rank = Article.objects.get_queryset().order_by('-view')[0:6]

    return articles_rank


def tag_cloud():
    # 标签云

    tags = Tag.objects.all()

    return tags


class IndexView(View):

    def get(self, request):
        """首页"""

        page_num = request.GET.get('page')

        articles_list = Article.objects.get_queryset()

        paginator = Paginator(list(articles_list), 10)

        articles = pagintor_reuse(page_num, paginator)

        articles_rank = rank_info()

        tags = tag_cloud()

        data = {
            'articles': articles,
            'articles_rank': articles_rank,
            'tags': tags
        }

        return render(request, 'index.html', context=data)


class DetailView(View):

    def get(self, request, pk=1):
        """详情页"""

        article = get_object_or_404(Article, pk=pk)

        article_tag = article.tags.all()

        name = article.category.name

        content = markdown(article.content, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])

        articles_rank = rank_info()

        tags = tag_cloud()

        form = CommentForm()
        # 获取这篇 article 下的全部评论
        comment_list = article.comment_set.all()

        data = {
            'id': pk,
            'article_title': article.title,
            'article_abstact': article.abstract,
            'article_content': content,
            'article_tag': article_tag,
            'article_created_time': article.created_time,
            'article_view': article.view,
            'article_category': name,
            'articles_rank': articles_rank,
            'tags': tags,
            'form': form,
            'comment_list': comment_list

        }

        return render(request, 'detail.html', context=data)


class CategoryView(View):

    def get(self, requset, category_name):
        """分类"""

        # 获取分类下的文章
        categories = Category.objects.get(other_name=category_name)

        articles_list = categories.article_set.all().order_by('-created_time')

        page_num = requset.GET.get('page')

        paginator = Paginator(list(articles_list), 10)

        articles = pagintor_reuse(page_num, paginator)

        articles_rank = rank_info()

        tags = tag_cloud()

        data = {
            'articles': articles,
            'articles_rank': articles_rank,
            'tags': tags,
            'categories': categories
        }

        html = str(categories.other_name) + '.html'

        return render(requset, html, context=data)


class TagView(View):

    def get(self, request, tag_name):

        tag = Tag.objects.get(name=tag_name)
        article_list = tag.article_set.all().order_by('-created_time')
        paginator = Paginator(article_list, 10)

        page_num = request.GET.get('page')

        articles = pagintor_reuse(page_num, paginator)

        articles_rank = rank_info()

        tags = tag_cloud()

        data = {
            'articles': articles,
            'articles_rank': articles_rank,
            'tags': tags,
            'tag_name': tag_name
        }

        return render(request, 'tag.html', context=data)


class SearchView(View):

    def post(self, request):

        keyword = request.POST.get("keyword")

        article_list = Article.objects.filter(content__contains=keyword).order_by('-created_time')

        paginator = Paginator(article_list, 10)

        page_num = request.GET.get('page')

        articles = pagintor_reuse(page_num, paginator)

        articles_rank = rank_info()

        tags = tag_cloud()

        data = {
            'articles': articles,
            'articles_rank': articles_rank,
            'tags': tags,
            'keyword': keyword
        }

        return render(request, 'search.html', context=data)


def page_not_found(request):
    return render(request, '404.html')


def page_errors(request):
    return render(request, '500.html')
