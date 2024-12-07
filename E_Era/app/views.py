from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
import os
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

# email : electronicera@gmail.com
# password :eera

def e_era_login(req):
    return render(req,'login.html')
    

# -----------------SHOP-------------------

def shop_home(req):
    return render(req,'shop/shop_home.html')

# -----------------USER---------------------
def register(req):
    return render(req,'user/register.html')
def user_home(req):
    return render(req,'user/user_home.html')
