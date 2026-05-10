from django.urls import path
from . import views
from .views import product_detail


urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.ec_dashboard, name='ec_dashboard'),
    path('profile/', views.profile, name='profile'),

    path('products/', views.product_list, name='product_list'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),

    path('category/<int:id>/', views.product_by_category, name='product_by_category'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('password-reset/', views.password_reset, name='password_reset'),

    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:id>/', product_detail, name='add_to_cart'),
    path('add_to_cart/<int:id>/',product_detail,name='add_to_cart'),
    path("remove-from-cart/<int:id>/", views.remove_from_cart, name="remove_from_cart"),

    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    path('checkout/', views.checkout, name='checkout'),
    path('upi-payment/', views.upi_payment, name='upi_payment'),

    path('orders/', views.order_page, name='order'),
    path('order-success/', views.order_success, name='order_success'),

]
