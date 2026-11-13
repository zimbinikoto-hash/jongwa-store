from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from .models import Store, Product, Review
from .serializers import (
    StoreSerializer,
    ProductSerializer,
    ReviewSerializer
)
from .permissions import IsVendor


class StoreCreateAPIView(APIView):
    """Allow authenticated vendors to create stores."""

    permission_classes = [IsAuthenticated, IsVendor]

    def post(self, request):
        serializer = StoreSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class VendorStoresAPIView(APIView):
    """Retrieve all stores belonging to a vendor."""

    permission_classes = [IsAuthenticated]

    def get(self, request, vendor_id):
        stores = Store.objects.filter(owner_id=vendor_id)
        serializer = StoreSerializer(stores, many=True)

        return Response(serializer.data)


class StoreProductsAPIView(APIView):
    """Retrieve all products belonging to a store."""

    permission_classes = [IsAuthenticated]

    def get(self, request, store_id):
        products = Product.objects.filter(store_id=store_id)

        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)

    def get_permissions(self):
        """Apply different permissions for GET and POST requests."""

        if self.request.method == 'POST':
            return [IsAuthenticated(), IsVendor()]

        return [IsAuthenticated()]

    def post(self, request, store_id):
        """Allow a vendor to add a product to their own store."""

        store = get_object_or_404(
            Store,
            pk=store_id,
            owner=request.user
        )

        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(store=store)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ProductReviewsAPIView(APIView):
    """Retrieve all reviews belonging to a product."""

    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        reviews = Review.objects.filter(product_id=product_id)

        serializer = ReviewSerializer(reviews, many=True)

        return Response(serializer.data)
