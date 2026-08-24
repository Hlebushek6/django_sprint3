from datetime import datetime
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from.models import Category, Post


# Create your views here.
def index(request):
    template = 'blog/index.html'
    posts = Post.objects.select_related('category', 'location', 'author').filter(
        pub_date__lte=datetime.now(), is_published=True, category__is_published=True
    ).order_by('-pub_date')[:5]
    context = {'post_list': posts}
    return render(request, template, context)


def post_detail(request, id):
    template = 'blog/detail.html'
    post = get_object_or_404(Post.objects.select_related('category', 'location', 'author').filter(
        pub_date__lte=datetime.now(), is_published=True, category__is_published=True
    ), pk=id)
    context = {'post': post}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    category = get_object_or_404(Category.objects.all().filter(is_published=True), slug=category_slug)
    posts = Post.objects.select_related('category', 'location', 'author').filter(
        category__slug=category_slug, pub_date__lte=datetime.now(), is_published=True
    ).order_by('-pub_date')
    context = {'category': category, 'post_list': posts}
    return render(request, template, context)
