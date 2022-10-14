from django.contrib import admin
from .models import Blog, Post, Category


class BlogAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'name', 'owner',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('blog', 'title',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('blog', 'slug', 'name', )
    # pass

admin.site.register(Blog, BlogAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)