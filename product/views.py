from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

from django.shortcuts import get_object_or_404

from product.models import Product, Review

from .services import get_products_with_average_ratings, get_total_product_review


class ProductsListAPI(APIView):
    class ProductsOutputSerializer(serializers.Serializer):
        name = serializers.CharField()
        price = serializers.DecimalField(max_digits=9, decimal_places=2)
        overall_rating = serializers.DecimalField(max_digits=3, decimal_places=2)

    def get(self, request):
        products = get_products_with_average_ratings()

        serializer = self.ProductsOutputSerializer(products, many=True)

        return Response(
            {"products": serializer.data},
            status=status.HTTP_200_OK
        )


class ProductsRetrieveAPI(APIView):
    class ProductOutputSerializer(serializers.Serializer):
        name = serializers.CharField()
        price = serializers.DecimalField(max_digits=9, decimal_places=2)

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
 
        serializers = self.ProductOutputSerializer(product)

        return Response({
            "products": serializers.data
            }, status=status.HTTP_200_OK)
    

class ProductCreateAPI(APIView):
    class ProductsInputSerializer(serializers.ModelSerializer):
        name = serializers.CharField(required=True)
        price = serializers.DecimalField(max_digits=9, decimal_places=2, required=True)

        def validate_name(self, value):
            try:
                int(value)
            except ValueError:
                return value
            raise serializers.ValidationError("Name cannot be a number")

        class Meta:
            model = Product
            fields = ["name", "price"]


    def post(self, request):
        serializer = self.ProductsInputSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class ProductDeleteAPI(APIView):
    def delete(self, request, product_id: int):
        product = get_object_or_404(Product, id=product_id)
        
        product.delete()

        return Response(status=status.HTTP_200_OK)
    

class ProductReviewsListAPI(APIView):
    class ProductReviewsOutputSerializer(serializers.Serializer):
        price_rating = serializers.IntegerField()
        quality_rating = serializers.IntegerField()
        functionality_rating = serializers.IntegerField()
        design_rating = serializers.IntegerField()
        brand_rating = serializers.IntegerField()
        ergonomics_rating = serializers.IntegerField()

    def get(self, request, product_id):
        reviews = Review.objects.filter(product=product_id)

        serializer = self.ProductReviewsOutputSerializer(reviews, many=True)

        return Response({"reviews":serializer.data}, status=status.HTTP_200_OK)
    

class ProductTotalReviewAPI(APIView):
    class ProductReviewsOutputSerializer(serializers.Serializer):
        total_rating = serializers.DecimalField(max_digits=3, decimal_places=2)
        price_rating = serializers.IntegerField()
        quality_rating = serializers.IntegerField()
        functionality_rating = serializers.IntegerField()
        design_rating = serializers.IntegerField()
        brand_rating = serializers.IntegerField()
        ergonomics_rating = serializers.IntegerField()

    def get(self, request, product_id):
        reviews = get_total_product_review(product_id)

        serializer = self.ProductReviewsOutputSerializer(reviews)

        return Response({"total_rating":serializer.data}, status=status.HTTP_200_OK)


class ReviewCreateAPI(APIView):
    class ReviewInputSerializer(serializers.ModelSerializer):
        product = serializers.PrimaryKeyRelatedField(
            queryset=Product.objects.all()
        )

        class Meta:
            model = Review
            fields = [
                "product",
                "price_rating",
                "quality_rating",
                "functionality_rating",
                "design_rating",
                "brand_rating",
                "ergonomics_rating",
            ]


    def post(self, request) -> Response:
        serializer = self.ReviewInputSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ReviewDeleteAPI(APIView):
    def delete(self, request, review_id: int):
        review = get_object_or_404(Product, id=review_id)
        
        review.delete()

        return Response(status=status.HTTP_200_OK)