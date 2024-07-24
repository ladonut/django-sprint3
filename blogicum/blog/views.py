from django.conf import settings

from django.shortcuts import render, get_object_or_404

from django.http import HttpRequest, HttpResponse

from django.utils.timezone import now

from blog.models import Post, Category


def get_post_list():
    return (
        Post.objects.select_related(
            'author', 'category', 'location'
        ).filter(
            is_published=True,
            pub_date__lt=now(),
            category__is_published=True,
        )
    )


def index(request: HttpRequest) -> HttpResponse:
    post_list = get_post_list()[:settings.POSTS_BY_PAGE]

    return render(request, 'blog/index.html', {'post_list': post_list})


def post_detail(request: HttpRequest, post_id: int) -> HttpResponse:
    post = get_object_or_404(
        get_post_list(),
        id=post_id
    )

    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request: HttpRequest, category_slug) -> HttpResponse:
    category = get_object_or_404(
        Category.objects,
        slug=category_slug,
        is_published=True
    )

    post_list = Post.objects.select_related(
        'author', 'category', 'location',
    ).filter(
        is_published=True,
        pub_date__lt=now(),
        category__is_published=True,
        category__slug=category_slug
    )

    return render(request, 'blog/category.html', {
        'category': category,
        'post_list': post_list
    })
