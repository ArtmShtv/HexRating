from django.urls import path
from .views import (ProductsListAPI, 
                    ProductsRetrieveAPI, 
                    ProductCreateAPI, 
                    ReviewCreateAPI, 
                    ProductDeleteAPI, 
                    ReviewDeleteAPI,
                    ProductReviewsListAPI
                    )

urlpatterns = [
    path("", ProductsListAPI.as_view(), name="products-list"),
    path("<int:product_id>/", ProductsRetrieveAPI.as_view(), name="products-retrieve"),
    path("create/", ProductCreateAPI.as_view(), name="product-create"),
    path("delete/<int:product_id>/", ProductDeleteAPI.as_view(), name="product-delete"),

    path("review/<int:product_id>/", ProductReviewsListAPI.as_view(), name="review-create"),
    path("review/create/", ReviewCreateAPI.as_view(), name="review-create"),
    path("review/delete/<int:review_id>/", ReviewDeleteAPI.as_view(), name="review-delete"),
]
