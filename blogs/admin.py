from django.contrib import admin
from .models import Blog, Post, Category


class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'related_blog',)

    @admin.display()
    def related_blog(self, model):
        return model.blog.name


class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Blog, BlogAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)