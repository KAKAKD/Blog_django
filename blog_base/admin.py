from django.contrib import admin
from .models import Category,Post,Tag,ContentImage

class ContentImageInline(admin.TabularInline):
    model = ContentImage
    extra = 1

class PostAdmin(admin.ModelAdmin):
    inlines = [
        ContentImageInline,
    ]

# Register your models here.
admin.site.register(Category)
admin.site.register(Post,PostAdmin)
admin.site.register(Tag)
