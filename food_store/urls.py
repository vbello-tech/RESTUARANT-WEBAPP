from django.urls import path

from .views import *
#from django.contrib.auth.views import LoginView, LogoutView


app_name = "food"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('about/', AboutView.as_view(), name="about"),
    path('food/', FoodListView.as_view(), name="food_list"),
    path('food/<int:pk>/', ProductView, name="food_detail"),
    path('search_food/', search_food, name="search_food"),
    path('reservation/', ReservationView.as_view(), name="reservation"),
    path('reservation/confirmation/<int:pk>/', reservation_confirm, name="reserved"),
    path('food/add-to-cart/<int:pk>/', add_to_cart, name="add_to_cart"),
    path('food/add-to-cart/<int:pk>/', add_to_cart_item, name="add_to_cart_item"),
    path('remove-from-cart/<int:pk>/', remove_from_cart, name="remove_from_cart"),
    path('remove-single-item-from-cart/<int:pk>/', remove_from_cart_item, name="remove_from_cart_item"),
    path('order_summary/', order_summaryView.as_view(), name="order_summary"),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('payment/stripe-payment/', PaymentView.as_view(), name="payment"),
]