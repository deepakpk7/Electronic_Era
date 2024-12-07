from django.urls import path
from . import views


urlpatterns = [
    path('',views.e_era_login),
    path('register',views.register)
 
# -------------user----------
]