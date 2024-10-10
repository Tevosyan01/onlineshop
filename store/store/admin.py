from django import forms
from django.contrib import admin
from .models import Category, SubCategory, Product

class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]
    prepopulated_fields = {'slug': ('name',)}

class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'subcategory_slug')
    list_filter = ('category',)

    def subcategory_slug(self, obj):
        if obj.subcategory:
            return obj.subcategory.slug
        return 'No subcategory'
    subcategory_slug.short_description = 'Subcategory Slug'


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
