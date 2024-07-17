from django.shortcuts import render

from django.http import Http404


# posts_dictionary = {post['id']: post for post in posts}
def index(request):
    template = 'blog/index.html'
    context = {'posts': reversed()}
    return render(request, template, context)


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
