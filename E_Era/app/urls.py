from django.urls import path
from . import views


urlpatterns = [
    path('',views.s_login),
    path('register',views.register),
    path('shop',views.shop_home),
    path('logout',views.s_logout),
    path('user_home',views.user_home),
]