from django.shortcuts import render, redirect
from .models import JobPost
from .forms import JobPostForm

def create_post(request):
    if request.method == 'POST':
        form = JobPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = JobPostForm()

    return render(request, 'jobs/post_create.html', {'form': form})
