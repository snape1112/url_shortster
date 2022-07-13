from django.contrib import admin

from .models import BlogPost, TagHistory

# Register your models here.
admin.site.register(BlogPost)
admin.site.register(TagHistory)