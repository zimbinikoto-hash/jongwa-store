from rest_framework import serializers
from .models import Store, Product, Review


class StoreSerializer(serializers.ModelSerializer):
    """Serialise store information for the API."""

    class Meta:
        model = Store
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    """Serialise product information for the API."""

    class Meta:
        model = Product
        fields = [
            'id', 'store', 'name', 'description',
            'price', 'stock', 'created_at'
        ]
        read_only_fields = ['id', 'store', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    """Serialise review information for the API."""

    class Meta:
        model = Review
        fields = [
            'id', 'product', 'rating', 'user',
            'comment', 'is_verified', 'created_at',
        ]

        read_only_fields = ['id', 'user', 'is_verified', 'created_at']
