from django.contrib import admin
from .models import JobPost, Category, Tag

admin.site.register(JobPost)
admin.site.register(Category)
admin.site.register(Tag)
