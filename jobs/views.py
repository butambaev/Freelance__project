from django.shortcuts import render, get_object_or_404, redirect
from .models import JobPost
from .forms import JobPostForm
from django.contrib.auth.decorators import login_required

def post_list(request):
    posts = JobPost.objects.all()
    return render(request, 'jobs/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(JobPost, pk=pk)
    return render(request, 'jobs/post_detail.html', {'post': post})

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
