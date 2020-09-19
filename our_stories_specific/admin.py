from django.contrib import admin
from .models import *

admin.site.register(OurStoriesSpecific)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on')
    search_fields = ('name', 'email', 'body')
    
