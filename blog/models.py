from django.db import models
# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone


class PublishedManager(models.Manager):
        def get_queryset(self):
            return super(PublishedManager, self).get_queryset().filter(status='published')


class DraftManager(models.Manager):
    def get_queryset(self):
        return super(DraftManager, self).get_queryset().filter(status='draft')


class Post(models.Model):
    published = PublishedManager()
    draft = DraftManager()
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='blog_posts',null=True)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
