from .models import Product, Review

from collections import defaultdict


def get_products_with_average_ratings() -> list:
    products = Product.objects.prefetch_related("reviews")

    result = []

    for product in products:
        rating_sum = 0
        review_count = 0

        for review in product.reviews.all():
            ratings = [
                review.price_rating,
                review.quality_rating,
                review.functionality_rating,
                review.design_rating,
                review.brand_rating,
                review.ergonomics_rating,
            ]

            rating_sum += sum(ratings)
            review_count += 1

        if review_count > 0:
            overall_rating = rating_sum / (review_count * 6)
        else:
            overall_rating = 0

        result.append({
            "name": product.name,
            "price": product.price,
            "overall_rating": overall_rating,
        })

    return result


def get_product_reviews(product_id:int) -> list:
    reviews = Review.objects.filter(product=product_id)

    res = []

    for review in reviews:
        ratings = [
            review.price_rating,
            review.quality_rating,
            review.functionality_rating,
            review.design_rating,
            review.brand_rating,
            review.ergonomics_rating,
        ]

        rating_sum = sum(ratings)

        res.append({
            "total_rating": rating_sum / 6,
            "price_rating":review.price_rating,
            "quality_rating": review.quality_rating,
            "functionality_rating": review.functionality_rating,
            "design_rating": review.design_rating,
            "brand_rating": review.brand_rating,
            "ergonomics_rating": review.ergonomics_rating
        })

    return res