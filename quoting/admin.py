from django.contrib import admin
from .models import post
# Register your models here.

class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated', 'timestamp']
    list_display_links = ['updated']
    list_filter = ['updated', 'timestamp']
    search_fields = ['title', 'content']
    class Meta:
        Model = post

admin.site.register(post, PostModelAdmin)
