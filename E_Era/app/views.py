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

def s_login(req):
    if 'shop' in req.session:
        return redirect(shop_home)
    if 'user' in req.session:
        return redirect(user_home)
    else:
        if req.method=='POST':
            uname=req.POST['uname']
            password=req.POST['password']
            data=authenticate(username=uname,password=password)
            if data:
                login(req,data)
                if data.is_superuser:
                    req.session['shop']=uname     #create
                    return redirect(shop_home)
                else:
                    req.session['user']=uname
                    return redirect(user_home)
            else:
                messages.warning(req, "Invalid Username or Password")
                return redirect(s_login)
    return render(req,'login.html')

def s_logout(req):
    logout(req)
    req.session.flush()
    return redirect(s_login)

def register(req):
    if req.method=='POST':
        uname=req.POST['uname']
        email=req.POST['email']
        pswd=req.POST['pswd']
        # send_mail('Eshop Registration', 'EShop account created sucssfully', settings.EMAIL_HOST_USER, [email])

        try:
            data=User.objects.create_user(first_name=uname,email=email,
                                        username=email,password=pswd)
            data.save()
        except:
            messages.warning(req, "Username or Email already exist")
            return redirect(register)
        return redirect(s_login)
    else:
        return render(req,'register.html')






def shop_home(req):
    if 'shop' in req.session:
        data=Product.objects.all()
        return render(req,'shop/shop_home.html',{'products':data})
    else:
        return redirect(s_login)

def add_pro(req):
    if 'shop' in req.session:
        if req.method=='POST':
            pid=req.POST['pid']
            name=req.POST['name']
            specifications=req.POST['specifications']
            price=req.POST['price']
            offer_price=req.POST['offer_price']
            brand=req.POST['brand']
            color=req.POST['color']
            highlights=req.POST['highlights']
            warranty=req.POST['warranty']
            services=req.POST['services']
            stock=req.POST['stock']
            img=req.FILES['img']
            product = Product(pid=pid,name=name,specifications=specifications,
                price=price,offer_price=offer_price,brand=brand,color=color,
                highlights=highlights,warranty=warranty,services=services,
                stock=stock,img=img
                )
            product.save()  
            return redirect(shop_home)
        else:
            return render(req,'shop/add_product.html')
    else:
        return redirect(s_login)
    
            
def edit_product(req,pid):
    if req.method=='POST':
        # pid=req.POST['pid']
        name=req.POST['name']
        specifications=req.POST['specifications']
        price=req.POST['price']
        offer_price=req.POST['offer_price']
        brand=req.POST['brand']
        color=req.POST['color']
        highlights=req.POST['highlights']
        warranty=req.POST['warranty']
        services=req.POST['services']
        stock=req.POST['stock']
        img=req.FILES.get('img')
        if img:
            Product.objects.filter(pk=pid).update(pid=pid,name=name,specifications=specifications,
                price=price,offer_price=offer_price,brand=brand,color=color,
                highlights=highlights,warranty=warranty,services=services,
                stock=stock)
            data=Product.objects.get(pk=pid)
            data.img=img
            data.save()
        else:
            Product.objects.filter(pk=pid).update(pid=pid,name=name,specifications=specifications,
                price=price,offer_price=offer_price,brand=brand,color=color,
                highlights=highlights,warranty=warranty,services=services,
                stock=stock)
        return redirect(shop_home)
    else:
        data=Product.objects.get(pk=pid)
        return render(req,'shop/edit.html',{'data':data})

def delete_product(req,pid):
    data=Product.objects.get(pk=pid)
    file=data.img.url
    file=file.split('/')[-1]
    os.remove('media/'+file)
    data.delete()
    return redirect(shop_home)


def view_bookings(req):
    buy=Buy.objects.all()[::-1]
    return render(req,'shop/view_bookings.html',{'buy':buy})

def admin_cancel_order(req,pid):
    data =Buy.objects.get(pk=pid)
    data.delete()
    return redirect(view_bookings) 

    

# ---------------user---------------
def user_home(req):
    if 'user' in req.session:
        data=Product.objects.all()
        apple = Product.objects.filter(brand='Apple')
        hp=Product.objects.filter(brand='HP')
        dell=Product.objects.filter(brand='DELL')
        asus=Product.objects.filter(brand='ASUS')
        lenovo=Product.objects.filter(brand='Lenovo')
        acer=Product.objects.filter(brand='acer')
        return render(req,'user/user_home.html',{'products':data,'apple': apple,'hp':hp,'dell':dell,'asus': asus,'lenovo':lenovo,'acer':acer})
    else:
        return redirect(s_login)
    
def view_product(req,pid):
    if 'user' in req.session:
        data=Product.objects.get(pk=pid)
        relate=Product.objects.all()
        return render(req,'user/view_product.html',{'product': data,'relate':relate})
    else:
        return render(req,'user/home.html')


def add_to_cart(req,pid):
    product=Product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    try:
        cart=Cart.objects.get(user=user,product=product)
        cart.qty+=1
        cart.save()
    except:
        data=Cart.objects.create(product=product,user=user,qty=1)
        data.save()
    return redirect(view_cart)

def view_cart(req):
    user=User.objects.get(username=req.session['user'])
    data=Cart.objects.filter(user=user)
    return render(req,'user/cart.html',{'cart':data})

def qty_in(req,cid):
    data=Cart.objects.get(pk=cid)
    data.qty+=1
    data.price= data.qty*data.product.offer_price
    data.save()
    return redirect(view_cart)

def qty_dec(req,cid):
    data=Cart.objects.get(pk=cid)
    data.qty-=1
    data.save()
    print(data.qty)
    if data.qty==0:
        data.delete()
    return redirect(view_cart)


def cart_pro_buy(req,cid):
    cart=Cart.objects.get(pk=cid)
    product=cart.product
    user=cart.user
    qty=cart.qty
    price=product.offer_price*qty
    buy=Buy.objects.create(product=product,user=user,qty=qty,price=price)
    buy.save()
    return redirect(bookings)

def pro_buy(req,pid):
    product=Product.objects.get(pk=pid)
    user=User.objects.get(username=req.session['user'])
    qty=1
    price=product.offer_price
    buy=Buy.objects.create(product=product,user=user,qty=qty,price=price)
    buy.save()
    return redirect(bookings)


def bookings(req):
    user=User.objects.get(username=req.session['user'])
    buy=Buy.objects.filter(user=user)[::-1]
    return render(req,'user/order.html',{'bookings':buy})



def cancel_order(req,pid):
    data =Buy.objects.get(pk=pid)
    data.delete()
    return redirect(bookings) 

def clear_cart(req):
    data=Cart.objects.all()
    data.delete()
    return redirect(view_cart)
    
def contact(req):
    if req.method == 'POST':
        name = req.POST['name']
        email = req.POST['email']
        phone = req.POST['phone']
        message = req.POST['message']
        try:
            data = Contact.objects.create(
                name=name,
                email=email,
                phone=phone,
                message=message
            )
            data.save()
            return render(req, 'user/contact.html')
        except Exception as e:
            return render(req,'user/contact.html')
    
    return render(req,'user/contact.html')

def profile(req):
    user=User.objects.get(username=req.session['user'])
    return render(req,'user/profile.html',{'user':user})

def logout_view(req):
    s_logout(req)
    return redirect(s_login)