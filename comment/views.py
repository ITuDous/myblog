from django.shortcuts import render, get_object_or_404, redirect
from markdown import markdown

from blog.models import Article
from blog.views import rank_info, tag_cloud

from .models import Comment
from .forms import CommentForm


def article_comment(request, pk):
    # 先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来。
    # 这里我们使用了 Django 提供的一个快捷函数 get_object_or_404，
    # 这个函数的作用是当获取的文章（Article）存在时，则获取；否则返回 404 页面给用户。
    article = get_object_or_404(Article, pk=pk)

    # HTTP 请求有 get 和 post 两种，一般用户通过表单提交数据都是通过 post 请求，
    # 因此只有当用户的请求为 post 时才需要处理表单数据。
    if request.method == 'POST':
        # 用户提交的数据存在 request.POST 中，这是一个类字典对象。
        # 我们利用这些数据构造了 CommentForm 的实例，这样 Django 的表单就生成了。
        form = CommentForm(request.POST)

        # 当调用 form.is_valid() 方法时，Django 自动帮我们检查表单的数据是否符合格式要求。
        if form.is_valid():
            # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            comment = form.save(commit=False)

            # 将评论和被评论的文章关联起来。
            comment.article = article

            # 最终将评论数据保存进数据库，调用模型实例的 save 方法
            comment.save()

            # 重定向到 article 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL。
            return redirect(article)

        else:
            # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
            # comment_list = article.comment_set.all()
            # context = {'article': article,
            #            'form': form,
            #            'comment_list': comment_list
            #            }
            # return render(request, 'detail.html', context=context)
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
            # 获取这篇 post 下的全部评论
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
                'commnet_list': comment_list

            }

            return render(request, 'detail.html', context=data)
    # 不是 post 请求，说明用户没有提交数据，重定向到文章详情页。
    return redirect(article)
