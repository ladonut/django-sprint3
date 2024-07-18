from typing import Union

from django.conf import settings
from django.shortcuts import render
from django.http import Http404, HttpRequest, HttpResponse
from django.utils.timezone import now 
from blog.models import Post, Location, Category


def index(request: HttpRequest) -> HttpResponse:
    post_list = Post.objects.select_related(
        'author', 'category', 'location',
    ).filter(
        is_published=True,
        pub_date__lt=now(),
        category__is_published=True, 
    )[:settings.POSTS_BY_PAGE]
    
    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request, id):
    template = 'blog/detail.html'
    post = None
    global posts_dictionary

    # Find post by its id key
    if id in posts_dictionary:
        post = posts_dictionary[id]

    if post is None:
        raise Http404(f'Post {id} not found')

    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    context = {'slug': category_slug}
    return render(request, template, context)


