from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Articles)
admin.site.register(BlogComment)
admin.site.register(ArticleViewCount)