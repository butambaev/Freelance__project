from django.shortcuts import render, get_object_or_404, redirect
from .models import JobPost, Category, Tag, Comment, Profile
from .forms import JobPostForm, CommentForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

@login_required
def create_post(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('post_list')
    else:
        form = JobPostForm()
    return render(request, 'jobs/post_create.html', {'form': form})

@login_required
def edit_post(request, pk):
    post = get_object_or_404(JobPost, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("Вы не можете редактировать этот пост")
    if request.method == 'POST':
        form = JobPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = JobPostForm(instance=post)
    return render(request, 'jobs/post_create.html', {'form': form, 'edit': True})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(JobPost, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("Вы не можете удалить этот пост")
    post.delete()
    return redirect('post_list')

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
    if sort in ['title', 'created_at', '-created_at', 'price', '-price']:
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
    post.views += 1
    post.save()

    comments = post.comments.all()
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'jobs/post_detail.html', {'post': post, 'comments': comments, 'form': form})

@login_required
def profile_edit(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'jobs/profile_edit.html', {'form': form})

@login_required
def profile_delete(request):
    profile = get_object_or_404(Profile, user=request.user)
    profile.user.delete()
    return redirect('post_list')
