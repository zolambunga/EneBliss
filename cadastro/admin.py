from django.contrib import admin

# Register your models here.
from .models import PT, Post, Residencia


admin.site.register(PT)
admin.site.register(Post)
admin.site.register(Residencia)
