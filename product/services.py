from .models import Product, Review



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


def get_total_product_review(product_id:int) -> dict:
    reviews = Review.objects.filter(product=product_id)

    res = {
        "total_rating": 0,
        "price_rating": 0,
        "quality_rating": 0,
        "functionality_rating": 0,
        "design_rating": 0,
        "brand_rating": 0,
        "ergonomics_rating": 0,
    }
    n = 0

    for review in reviews:
        n +=1 
        ratings = [
            review.price_rating,
            review.quality_rating,
            review.functionality_rating,
            review.design_rating,
            review.brand_rating,
            review.ergonomics_rating
        ]
        
        res["total_rating"] += round(sum(ratings) / (len(reviews) * 6), 2)
        res["price_rating"] += round(review.price_rating / len(reviews), 2)
        res["quality_rating"] += round(review.quality_rating / len(reviews), 2)
        res["functionality_rating"] += round(review.functionality_rating / len(reviews), 2)
        res["design_rating"] += round(review.design_rating / len(reviews), 2)
        res["brand_rating"] += round(review.brand_rating / len(reviews), 2)
        res["ergonomics_rating"] += round(review.ergonomics_rating / len(reviews), 2)

    return res