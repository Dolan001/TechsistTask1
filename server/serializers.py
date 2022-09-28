from pyexpat import model
from rest_framework import serializers

from .models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "slug",
            "get_product_url",
            "description",
            "price",
            "get_img",
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
            'get_category_url',
        )


class CategoryProductSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
            'get_category_url',
            'products',
        )