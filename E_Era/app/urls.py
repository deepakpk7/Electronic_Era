from django.urls import path
from . import views


urlpatterns = [
    path('',views.s_login),
    path('register',views.register),

    # ------------shop-------------
    path('shop',views.shop_home),
    path('logout',views.s_logout),
    path('add_pro',views.add_pro),
    path('delete_product/<pid>',views.delete_product),
    path('edit_product/<pid>',views.edit_product),
    path('view_booking',views.view_booking),
    

    # ------------USER-------------
    
    path('user_home',views.user_home),
    path('view_product/<pid>',views.view_product),
    path('contact',views.contact),
    path('qty_in/<cid>',views.qty_in),
    path('qty_dec/<cid>',views.qty_dec),
    path('add_to_cart/<pid>',views.add_to_cart),
    path('cart_pro_buy/<cid>',views.cart_pro_buy),
    path('cancel_order/<pid>',views.cancel_order),
    path('order',views.bookings),
    path('view_cart/',views.view_cart),
    
    
]