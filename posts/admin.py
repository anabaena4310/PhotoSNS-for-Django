from django.contrib import admin
from .models import Post, CustomUser, Interest, Tag

admin.site.register(Post)
admin.site.register(CustomUser)
admin.site.register(Interest)
admin.site.register(Tag)
