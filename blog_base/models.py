from django.db import models
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=225)
    slug = models.SlugField(unique=True)
    timestap = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return self.name

class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag,blank='True')
    title = models.CharField(max_length=225)
    content = models.TextField()
    description = models.CharField(max_length=225)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(blank=True, null=True)
    is_public = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images',null=True,blank=True)

    class Meta :
        ordering = ['-create_at']

    def save(self, *args):
        if self.is_public and not self.published_at:
            self.published_at = timezone_now()
        super().save(*args)

    def __str__(self):
        return self.title

class ContentImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    content_image = models.ImageField(upload_to='content_images', null=True, blank='True')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=50)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)

    class Meta:
        ordering = ['-timestamp']

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
         return self.text

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    author =models.CharField(max_length=50)
    text = models.TextField()
    timestap = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)

    def approve(self):
        self.approved = True
        self.save()
