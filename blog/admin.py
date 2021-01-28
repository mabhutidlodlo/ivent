from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Blog, Comment 

class BlogAdmin(SummernoteModelAdmin):
    exclude=('slug',)
    summernote_fields = ('content',)

admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment,)

