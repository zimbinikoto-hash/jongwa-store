from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='store/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),


    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='store/password_reset.html',
            email_template_name='store/password_reset_email.html',
            subject_template_name='store/password_reset_subject.txt',
        ),
        name='password_reset'
    ),

    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='store/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='store/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='store/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),


    path(
        'vendor/dashboard/',
        views.vendor_dashboard,
        name='vendor_dashboard'
    ),

    path(
        'vendor/store/create/',
        views.create_store,
        name='create_store'
    ),

    path(
        'vendor/store/<int:store_id>/edit/',
        views.edit_store,
        name='edit_store'
    ),

    path(
        'vendor/store/<int:store_id>/delete/',
        views.delete_store,
        name='delete_store'
    ),

    path(
        'vendor/store/<int:store_id>/add-product/',
        views.add_product,
        name='add_product'
    ),

    path(
        'vendor/product/<int:product_id>/edit/',
        views.edit_product,
        name='edit_product'
    ),

    path(
        'vendor/product/<int:product_id>/delete/',
        views.delete_product,
        name='delete_product'
    ),

    path(
        'product/<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),

    path('cart/', views.view_cart, name='view_cart'),

    path(
        'cart/add/<int:product_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/remove/<int:product_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

    path(
        'cart/update/<int:product_id>/',
        views.update_cart,
        name='update_cart'
    ),

    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),

    path(
        'order-success/<int:order_id>/',
        views.order_success,
        name='order_success'
    ),

    path(
        'invoice/<int:order_id>/download/',
        views.download_invoice,
        name='download_invoice'
    ),
]
