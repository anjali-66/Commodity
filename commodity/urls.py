from django.urls import path
from .views import UserSignupView, ProductsListView, PlaceBidView, AcceptBidView

urlpatterns = [
    path('user/signup/', UserSignupView.as_view(), name='user_signup'),
    path('Products/list/', ProductsListView.as_view(), name='Products_list'),
    path('Products/bid/', PlaceBidView.as_view(), name='place_bid'),
    path('Products/accept-bid/', AcceptBidView.as_view(), name='accept_bid'),
]
