from django.shortcuts import render, get_object_or_404, redirect
from .models import JobPost, Category, Tag
from .forms import JobPostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

@login_required
def create_post(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = JobPostForm()
    return render(request, 'jobs/post_create.html', {'form': form})

def post_list(request):
    posts = JobPost.objects.all()
    all_categories = Category.objects.all()
    all_tags = Tag.objects.all()

    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(title__icontains=search_query)

    category_id = request.GET.get('category')
    if category_id:
        posts = posts.filter(category__id=category_id)

    tag_ids = request.GET.getlist('tags')
    if tag_ids:
        posts = posts.filter(tags__id__in=tag_ids).distinct()

    sort = request.GET.get('sort')
    if sort in ['title', 'created_at', '-created_at']:
        posts = posts.order_by(sort)

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'posts': page_obj,
        'page_obj': page_obj,
        'all_categories': all_categories,
        'all_tags': all_tags,
        'search_query': search_query,
        'selected_category': category_id,
        'selected_tags': tag_ids,
        'sort': sort
    }
    return render(request, 'jobs/post_list.html', context)

def post_detail(request, pk):
    post = get_object_or_404(JobPost, pk=pk)
    return render(request, 'jobs/post_detail.html', {'post': post})
