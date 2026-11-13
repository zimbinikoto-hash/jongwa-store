from django.urls import path

from .api_views import (
    StoreCreateAPIView,
    VendorStoresAPIView,
    StoreProductsAPIView,
    ProductReviewsAPIView,
)

urlpatterns = [
    path(
        'stores/',
        StoreCreateAPIView.as_view(),
        name='api-store-create'
    ),

    path(
        'vendors/<int:vendor_id>/stores/',
        VendorStoresAPIView.as_view(),
        name='api-vendor-stores'
    ),

    path(
        'stores/<int:store_id>/products/',
        StoreProductsAPIView.as_view(),
        name='api-store-products'
    ),

    path(
        'products/<int:product_id>/reviews/',
        ProductReviewsAPIView.as_view(),
        name='api-product-reviews'
    ),
]
