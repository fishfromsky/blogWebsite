from django.shortcuts import render_to_response, get_object_or_404, render
from .models import BlogType, Blog
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment


def blog_list(request):
    page_num = request.GET.get('page', 1)  #获取页码参数
    blog_all_lists = Blog.objects.all()
    paginator = Paginator(blog_all_lists, 3)  #每10页进行分类
    page_of_blog = paginator.get_page(page_num)
    current_page_num = page_of_blog.number
    page_range = list(range(max(current_page_num-2, 1), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num+2, paginator.num_pages)+1))

    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}
    context['blogs'] = page_of_blog.object_list
    context['page_of_blogs'] = page_of_blog
    context['page_range'] = page_range
    context['blog_tyepes'] = BlogType.objects.all()
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order='DESC')
    return render_to_response('blog_list.html', context)


def blog_detail(request, blog_pk):

    context = {}
    context['blog'] = get_object_or_404(Blog, pk=blog_pk)
    blog = get_object_or_404(Blog, pk=blog_pk)
    blog_content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk)

    context['previous_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).last()
    context['next_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).first()
    context['user'] = request.user
    context['comments'] = comments
    return render(request, 'blog_detail.html', context)


def blog_with_type(request, blog_type_pk):
    context = {}
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    context['blogs'] = Blog.objects.filter(blog_type=blog_type)
    context['blog_type'] = blog_type
    return render_to_response('blogs_with_type.html', context)


def blog_with_date(request, year, month):

    page_num = request.GET.get('page', 1)  # 获取页码参数
    blog_all_lists = Blog.objects.filter(created_time__year=year, created_time__month=month)
    paginator = Paginator(blog_all_lists, 5)  # 每10页进行分类
    page_of_blog = paginator.get_page(page_num)
    current_page_num = page_of_blog.number
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))

    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}
    context['blog_with_date'] = '%s年%s月' % (year, month)
    context['blog_date'] = blog_all_lists
    context['blogs'] = page_of_blog.object_list
    context['page_of_blogs'] = page_of_blog
    context['page_range'] = page_range
    context['blog_tyepes'] = BlogType.objects.all()
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order='DESC')
    return render_to_response('blog_with_date.html', context)