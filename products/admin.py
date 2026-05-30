from django.contrib import admin
from .models import Category, Product, ProductImage, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'stock', 'featured', 'is_active')
    list_filter = ('category', 'featured', 'is_active')
    search_fields = ('title', 'summary', 'description')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': ('category', 'title', 'slug', 'summary', 'description', 'price', 'stock')
        }),
        ('Catalog controls', {
            'fields': ('featured', 'is_active')
        }),
    )
    inlines = [ProductImageInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    search_fields = ('product__title', 'user__username', 'comment')
