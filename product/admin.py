from django.contrib import admin
from .models import Product, Review

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price") 

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
            "product",
            "price_rating",
            "quality_rating",
            "functionality_rating",
            "design_rating",
            "brand_rating",
            "ergonomics_rating",
        ]
