from django.urls import path
from . import views


urlpatterns = [
    path('login',views.s_login),
    path('register',views.register),

    # ------------shop-------------
    path('shop',views.shop_home),
    path('logout',views.s_logout),
    path('add_pro',views.add_pro),
    path('delete_product/<pid>',views.delete_product),
    path('edit_product/<pid>',views.edit_product),
    path('view_booking',views.view_bookings),
    path('admin_cancel_order/<pid>',views.admin_cancel_order),
    

    # ------------USER-------------
    
    path('',views.user_home),
    path('view_product/<pid>',views.view_product),
    path('contact',views.contact),
    path('address',views.address),
    path('update_username',views.update_username),
    path('delete_address/<pid>',views.delete_address),
    path('about',views.about),
    path('qty_in/<cid>',views.qty_in),
    path('qty_dec/<cid>',views.qty_dec),
    path('add_to_cart/<pid>',views.add_to_cart),
    path('cart_pro_buy/<cid>',views.cart_pro_buy),
    path('cancel_order/<pid>',views.cancel_order),
    path('cancel_order/<int:pid>',views.cancel_order, name='cancel_order'),
    path('pro_buy/<pid>',views.pro_buy),
    path('order',views.bookings),
    path('view_cart/',views.view_cart),
    path('clear_cart',views.clear_cart),
    path('order_payment',views.order_payment),
    
    
]