import pytest

from .conftest import api_client

from django.urls import reverse
from product.models import Product, Review


@pytest.fixture
def product_data(db) -> Product:
    first_product = Product.objects.create(name="Some product 1", price=1.11)

    return first_product


@pytest.fixture
def products_data(db) -> list[Product]:
    first_product = Product.objects.create(name="Some product 1", price=1.11)
    second_product = Product.objects.create(name="Some product 2", price=2.22)
    third_product = Product.objects.create(name="Some product 3", price=3.33)

    review1 = Review.objects.create(
        product = first_product,
        price_rating = 5,
        quality_rating = 5,
        functionality_rating = 5,
        design_rating = 5,
        brand_rating = 5,
        ergonomics_rating = 5
    )
    review2 = Review.objects.create(
        product = second_product,
        price_rating = 5,
        quality_rating = 5,
        functionality_rating = 5,
        design_rating = 5,
        brand_rating = 5,
        ergonomics_rating = 5
    )
    review3 = Review.objects.create(
        product = second_product,
        price_rating = 4,
        quality_rating = 4,
        functionality_rating = 4,
        design_rating = 4,
        brand_rating = 4,
        ergonomics_rating = 4
    )

    return first_product, second_product, third_product


@pytest.fixture
def reviews_data(db) -> list[Review]:
    first_product = Product.objects.create(name="Some product 1", price=1.11)
    second_product = Product.objects.create(name="Some product 2", price=2.22)
    third_product = Product.objects.create(name="Some product 3", price=3.33)

    review1 = Review.objects.create(
        product = first_product,
        price_rating = 5,
        quality_rating = 5,
        functionality_rating = 5,
        design_rating = 5,
        brand_rating = 5,
        ergonomics_rating = 5
    )
    review2 = Review.objects.create(
        product = second_product,
        price_rating = 5,
        quality_rating = 5,
        functionality_rating = 5,
        design_rating = 5,
        brand_rating = 5,
        ergonomics_rating = 5
    )
    review3 = Review.objects.create(
        product = second_product,
        price_rating = 4,
        quality_rating = 4,
        functionality_rating = 4,
        design_rating = 4,
        brand_rating = 4,
        ergonomics_rating = 4
    )


def test_product_retrieve(api_client, product_data):
    url = reverse("products-retrieve", args=[1])
    response = api_client.get(url)

    expected = { 
        "products": {
            "name": "Some product 1",
            "price": "1.11"
        }
    }
    
    assert response.status_code == 200
    assert response.data == expected


def test_product_list(api_client, products_data):
    url = reverse("products-list")
    response = api_client.get(url)

    expected = { 
        "products": [
            {
            "name": "Some product 1",
            "price": "1.11",
            "overall_rating": "5.00",
            },
            {
            "name": "Some product 2",
            "price": "2.22",
            "overall_rating": "4.50",
            },
            {
            "name": "Some product 3",
            "price": "3.33",
            "overall_rating": "0.00",
            },
        ]
    }

    assert response.status_code == 200
    assert response.data == expected


def test_reviews_list_for_product(api_client, reviews_data):
    url = reverse("product-reviews-list", args=[2])
    response = api_client.get(url)

    expected = {
        "reviews": [
            {
                "price_rating": 5,
                "quality_rating": 5,
                "functionality_rating": 5,
                "design_rating": 5,
                "brand_rating": 5,
                "ergonomics_rating": 5
            },
            {
                "price_rating": 4,
                "quality_rating": 4,
                "functionality_rating": 4,
                "design_rating": 4,
                "brand_rating": 4,
                "ergonomics_rating": 4
            }
        ]
    }

    assert response.status_code == 200
    assert response.data == expected


def test_total_review_for_product(api_client, reviews_data):
    url = reverse("product-total-rating", args=[2])
    response = api_client.get(url)

    expected = {
        "total_rating": {
            "total_rating": "4.50",
            "price_rating": 4,
            "quality_rating": 4,
            "functionality_rating": 4,
            "design_rating": 4,
            "brand_rating": 4,
            "ergonomics_rating": 4
        }
    }

    assert response.status_code == 200
    assert response.data == expected


def test_total_review_for_product_without_reviews(api_client, reviews_data):
    url = reverse("product-total-rating", args=[3])
    response = api_client.get(url)

    expected = {
        "total_rating": {
            "total_rating": "0.00",
            "price_rating": 0,
            "quality_rating": 0,
            "functionality_rating": 0,
            "design_rating": 0,
            "brand_rating": 0,
            "ergonomics_rating": 0
        }
    }

    assert response.status_code == 200
    assert response.data == expected


@pytest.mark.django_db
def test_create_product(api_client):
    url = reverse("product-create")
    payload = {
        "name": "Some_product", 
        "price": 100
    }
    headers = {"Content-Type": "application/json"}
    response = api_client.post(url, payload, format="json")

    assert response.status_code == 201