import pytest

from .conftest import api_client

from django.urls import reverse
from product.models import Product, Review

from rest_framework import serializers


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

    return review1, review2, review3


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


def test_non_existing_product_retrieve(api_client, product_data):
    url = reverse("products-retrieve", args=[999])
    response = api_client.get(url)
    
    assert response.status_code == 404


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


def test_reviews_list_for_non_existing_product(api_client, reviews_data):
    url = reverse("product-reviews-list", args=[999])
    response = api_client.get(url)

    expected = {
        "reviews": []
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


def test_total_review_for_non_existing_product(api_client, reviews_data):
    url = reverse("product-total-rating", args=[999])
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


@pytest.mark.django_db
def test_create_product_with_invaid_data(api_client):
    url = reverse("product-create")
    payload = {
        "wrong_name_field": "Some_product", 
        "price": 100
    }
    response = api_client.post(url, payload, format="json")

    assert response.status_code == 400


@pytest.mark.django_db
def test_create_product_with_number_name_field(api_client):
    url = reverse("product-create")
    payload = {
        "name": 1, 
        "price": 100
    }
    response = api_client.post(url, payload, format="json")

    assert response.status_code == 400
    assert response.data["name"][0] == "Name cannot be a number"


@pytest.mark.django_db
def test_create_review(api_client, product_data):
    url = reverse("review-create")
    payload = {
        "product": product_data.id,
        "price_rating": 4,
        "quality_rating": 3,
        "functionality_rating": 5,
        "design_rating": 2,
        "brand_rating": 1,
        "ergonomics_rating": 5
    }

    response = api_client.post(url, payload, format="json")

    assert Product.objects.filter(id=product_data.id).exists() == True
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_review_for_non_existing_product(api_client):
    url = reverse("review-create")
    payload = {
        "product": 999,
        "price_rating": 4,
        "quality_rating": 3,
        "functionality_rating": 5,
        "design_rating": 2,
        "brand_rating": 1,
        "ergonomics_rating": 5
    }

    response = api_client.post(url, payload, format="json")

    assert Product.objects.filter(id=999).exists() == False
    assert response.status_code == 400


def test_delete_product(api_client, product_data):
    url = reverse("product-delete", args=[1])
    response = api_client.delete(url)

    assert response.status_code == 200
    assert Product.objects.filter(id=1).exists() == False


def test_delete_non_existing_product(api_client, product_data):
    url = reverse("product-delete", args=[999])
    response = api_client.delete(url)

    assert response.status_code == 404


def test_delete_review(api_client, reviews_data):
    url = reverse("review-delete", args=[1])
    response = api_client.delete(url)

    assert response.status_code == 200
    assert Review.objects.filter(id=1).exists() == False


def test_delete_non_existing_review(api_client, reviews_data):
    url = reverse("review-delete", args=[999])
    response = api_client.delete(url)

    assert response.status_code == 404

