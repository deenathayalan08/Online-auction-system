from django.urls import path
from . import views

urlpatterns = [
    path('', views.auction_list, name='auction_list'),
    path('auction/<int:auction_id>/', views.auction_detail, name='auction_detail'),
    path('create/', views.create_auction, name='create_auction'),
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login_view, name='login'),
    path('logout/', views.user_logout_view, name='logout'),
]
