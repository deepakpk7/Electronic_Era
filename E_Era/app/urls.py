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
    path('add_phone',views.add_phone),
    path('edit_phone/<id>',views.edit_phone),
    path('edit_accessories/<id>',views.edit_accessories),
    path('add_accessories',views.add_accessories),
    

    # ------------USER-------------
    
    path('user_home',views.user_home),
    path('view_product/<pid>',views.view_product),
    path('view_product/<id>',views.view_product),
    path('contact',views.contact),
    path('add_to_cart/<pid>',views.add_to_cart),
    path('view_cart/',views.view_cart),
    
]