from django.contrib import admin

from .models import Group, Post, Comment, Follow

admin.site.register((Group, Post, Comment, Follow))
