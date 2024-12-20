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
        phone=Phone.objects.all()
        accessory=Accessories.objects.all()
        return render(req,'shop/shop_home.html',{'products':data,'phone':phone,'accessory':accessory})
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
    
def add_phone(req):
    if 'shop' in req.session:
        if req.method=='POST':
            brand=req.POST['brand']
            model=req.POST['model']
            price=req.POST['price']
            offer_price=req.POST['offer_price']
            operating_system=req.POST['operating_system']
            storage_capacity=req.POST['storage_capacity']
            ram=req.POST['ram']
            color=req.POST['color']
            specifications=req.POST['specifications']
            stock=req.POST['stock']
            img=req.FILES['img']
            phone=Phone(brand=brand,model=model,price=price,offer_price=offer_price,
                        operating_system=operating_system,storage_capacity=storage_capacity,
                        ram=ram,color=color,stock=stock,specifications=specifications,img=img)
            phone.save()
            return redirect(shop_home)
        else:
            return render(req,'shop/add_phone.html')
    else:
        return redirect(s_login)
    
def edit_phone(req,id):
    if req.method=='POST':
        brand=req.POST['brand']
        model=req.POST['model']
        price=req.POST['price']
        offer_price=req.POST['offer_price']
        operating_system=req.POST['operating_system']
        storage_capacity=req.POST['storage_capacity']
        ram=req.POST['ram']
        color=req.POST['color']
        specifications=req.POST['specifications']
        stock=req.POST['stock']
        img=req.FILES['img']
        if img:
            Phone.objects.filter(pk=id).update(brand=brand,model=model,price=price,offer_price=offer_price,
                        operating_system=operating_system,storage_capacity=storage_capacity,
                        ram=ram,color=color,stock=stock,specifications=specifications)
            data=Phone.objects.get(pk=id)
            data.img=img
            data.save()
        else:
            Phone.objects.filter(pk=id).update(brand=brand,model=model,price=price,offer_price=offer_price,
                                                      operating_system=operating_system,storage_capacity=storage_capacity,
                                                        ram=ram,color=color,stock=stock,specifications=specifications)
        return redirect(shop_home)
    else:
        phone=Phone.objects.get(pk=id)
        return render(req,'shop/edit_phone.html',{'phone':phone})

def delete_phone(req,id):
    data=Phone.objects.get(pk=id)
    file=data.img.url
    file=file.split('/')[-1]
    os.remove('media/'+file)
    data.delete()
    return redirect(shop_home)        

def add_accessories(req):
    if 'shop' in req.session:
        if req.method=='POST':
            accessory_id=req.POST['accessory_id']
            name=req.POST['name']
            brand=req.POST['brand']
            color=req.POST['color']
            description=req.POST['description']
            price=req.POST['price']
            offer_price=req.POST['offer_price']
            stock=req.POST['stock']
            warranty=req.POST['warranty']
            img=req.FILES['img']
            accessory=Accessories(accessory_id=accessory_id,name=name,brand=brand,color=color,
                                  description=description,price=price,offer_price=offer_price,
                                  stock=stock,warranty=warranty,img=img)
            accessory.save()
            return redirect(shop_home)
        else:
            return render(req,'shop/add_accessories.html')
    else:
        return redirect(s_login)
    
def edit_accessories(req,id):
    if req.method=='POST':
        accessory_id=req.POST['accessory_id']
        name=req.POST['name']
        brand=req.POST['brand']
        color=req.POST['color']
        description=req.POST['description']
        price=req.POST['price']
        offer_price=req.POST['offer_price']
        stock=req.POST['stock']
        warranty=req.POST['warranty']
        img=req.FILES['img']
        if img:
            Accessories.objects.filter(pk=id).update(accessory_id=accessory_id,name=name,brand=brand,color=color,
                                  description=description,price=price,offer_price=offer_price,
                                  stock=stock,warranty=warranty)
            data=Accessories.objects.get(pk=id)
            data.img=img
            data.save()
        else:
            Accessories.objects.filter(pk=id).update(accessory_id=accessory_id,name=name,brand=brand,color=color,
                                  description=description,price=price,offer_price=offer_price,
                                  stock=stock,warranty=warranty)
        return redirect(shop_home)
    else:
        accessory=Accessories.objects.get(pk=id)
        return render(req,'shop/edit_accessories.html',{'accessory':accessory})
    
def delete_accessory(req,id):
    data=Accessories.objects.get(pk=id)
    file=data.img.url
    file=file.split('/')[-1]
    os.remove('media/'+file)
    data.delete()
    return redirect(shop_home)
            
    
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

def view_booking(req):
    return render(req,'shop/view_bookings.html')


# ---------------user---------------
def user_home(req):
    if 'user' in req.session:
        data=Product.objects.all()
        phone=Phone.objects.all()
        accessories=Accessories.objects.all()
        return render(req,'user/user_home.html',{'products':data,'phone':phone,'accessories':accessories})
    else:
        return redirect(s_login)
    
def view_product(req,pid):
    if 'user' in req.session:
        data=Product.objects.get(pk=pid)
        return render(req,'user/view_product.html',{'product': data})
    else:
        return render(req,'user/home.html')
    
def view_phone(req,pid):
    if 'user' in req.session:
        data=Phone.objects.get(pk=pid)
        return render(req,'user/view_phone.html',{'phone':data})
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