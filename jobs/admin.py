from django.contrib import admin
from .models import JobPost, Category, Tag, Comment, Profile

class JobPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'price', 'views', 'created_at')
    list_filter = ('category', 'tags', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username',)

admin.site.register(JobPost, JobPostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Profile, ProfileAdmin)
