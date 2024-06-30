from django.contrib import admin

from .models import Post, Category, Location, Comment


admin.site.empty_value_display = 'Не задано'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'pub_date',
        'author',
        'location',
        'category',
        'is_published',
        'created_at',
        'image'
    )
    list_editable = (
        'is_published',
    )
    search_fields = ('title',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_published'
    )
    list_editable = (
        'is_published',
    )


admin.site.register(Location)
admin.site.register(Comment)
