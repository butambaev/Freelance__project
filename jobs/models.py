from django.db import models
from django.utils import timezone

class Post(models.Model):
    title = models.CharField("Название проекта", max_length=200)
    content = models.TextField("Описание проекта")
    author = models.CharField("Автор", max_length=100)
    photo = models.ImageField("Фото проекта", upload_to="posts/", blank=True, null=True)
    created_at = models.DateTimeField("Дата создания", default=timezone.now)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField("Категория", max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="categories")

    def __str__(self):
        return f"{self.name} ({self.post.title})"
    
photo = models.ImageField("Фото проекта", upload_to="posts/", blank=True, null=True)
