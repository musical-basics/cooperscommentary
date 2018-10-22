from django.contrib import admin
from .models import Post
# from blog.models import Post (this is same as above line)
# Register your models here.

class PostsAdmin(admin.ModelAdmin):
    fields = ['title','author','date_posted']


admin.site.register(Post, PostsAdmin)

# admin.site.register(models.Movie,MovieAdmin)