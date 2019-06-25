from django.contrib import admin
from blog.models import Post
# Register your models here.
# from django.contrib.auth.models import User


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'created', 'updated')
    search_fields = ('title', 'body')
    ordering = ['status', 'publish']


admin.site.register(Post, PostAdmin)
