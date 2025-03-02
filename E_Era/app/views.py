from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *
import os
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from django.utils.timezone import now
from datetime import datetime, timedelta
import re

# Create your views here.



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

# def register(req):
#     if req.method=='POST':
#         uname=req.POST['uname']
#         email=req.POST['email']
#         pswd=req.POST['pswd']
#         send_mail('Welcome to ElectronicEra!',
#                   """
#                   Dear user,

#                     Thank you for registering with ElectronicEra! We are excited to have you on board.

#                     Your account has been successfully created, and you can start shopping for the best electronics in the market!

#                     Quote of the day: "The best way to predict the future is to invent it." – Alan Kay

#                     Feel free to contact us if you have any questions.

#                     Best regards,
#                     ElectronicEra Team
#                   """, settings.EMAIL_HOST_USER, [email])
#         try:
#             data=User.objects.create_user(first_name=uname,email=email,
#                                         username=email,password=pswd)
#             data.save()
#         except:
#             messages.warning(req, "Username or Email already exist")
#             return redirect(register)
#         return redirect(s_login)
#     else:
#         return render(req,'register.html')

def register(req):
    if req.method == 'POST':
        uname = req.POST['uname'].strip()
        email = req.POST['email'].strip()
        pswd = req.POST['pswd'].strip()

        # Email validation
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_pattern, email):
            messages.error(req, "Invalid email format.")
            return redirect(register)
        # Password validation (Minimum 8 characters, at least one letter, one number, and one special character)
        password_pattern = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
        if not re.match(password_pattern, pswd):
            messages.error(req, "Password must be at least 8 characters long and include a letter, a number, and a special character.")
            return redirect(register)

        # Check if username or email already exists
        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            messages.warning(req, "Username or Email already exists.")
            return redirect(register)

        try:
            user = User.objects.create_user(first_name=uname, email=email, username=email, password=pswd)
            user.save()
            send_mail(
                'Welcome to ElectronicEra!',
                """
                Dear user,

                Thank you for registering with ElectronicEra! We are excited to have you on board.

                Your account has been successfully created, and you can start shopping for the best electronics in the market!

                Quote of the day: "The best way to predict the future is to invent it." – Alan Kay

                Feel free to contact us if you have any questions.

                Best regards,
                ElectronicEra Team
                """,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False
            )

            messages.success(req, "Registration successful! You can now log in.")
            return redirect(s_login)

        except Exception as e:
            messages.error(req, f"An error occurred: {e}")
            return redirect(register)

    return render(req, 'register.html')

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
    price=Cart.objects.all()
    add=Address.objects.all()
    return render(req,'shop/view_bookings.html',{'buy':buy,'price':price,'add':add})

def admin_cancel_order(req,pid):
    data =Buy.objects.get(pk=pid)
    data.delete()
    return redirect(view_bookings) 

    

# ---------------user---------------
def user_home(req):
    # if 'user' in req.session:
        data=Product.objects.all()
        apple = Product.objects.filter(brand='Apple')
        hp=Product.objects.filter(brand='HP')
        dell=Product.objects.filter(brand='DELL')
        asus=Product.objects.filter(brand='ASUS')
        lenovo=Product.objects.filter(brand='Lenovo')
        print(lenovo)
        acer=Product.objects.filter(brand='acer')
        return render(req,'user/user_home.html',{'products':data,'apple': apple,'hp':hp,'dell':dell,'asus': asus,'lenovo':lenovo,'acer':acer})
    # else:
    #     return redirect(s_login)
    
def view_product(req,pid):
    if 'user' in req.session:
        data=Product.objects.get(pk=pid)
        relate=Product.objects.all()
        return render(req,'user/view_product.html',{'product': data,'relate':relate})
    else:
        return redirect(s_login)


def add_to_cart(req,pid):
    if 'user' in req.session:
        product=Product.objects.get(pk=pid)
        user=User.objects.get(username=req.session['user'])
        price=product.offer_price
        try:
            cart=Cart.objects.get(user=user,product=product)
            cart.qty+=1
            cart.save()
        except:
            data=Cart.objects.create(product=product,user=user,qty=1,price=price)
            data.save()
        return redirect(view_cart)
    else:
        return redirect(s_login)
def view_cart(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        data=Cart.objects.filter(user=user)
        data1=Address.objects.filter(user=user)
        return render(req,'user/cart.html',{'cart':data,'data1':data1})
    return redirect(s_login)

def qty_in(req, cid):
    try:
        data = Cart.objects.get(pk=cid)
        stock = int(data.product.stock)
        if stock > data.qty:
            data.qty += 1
            data.price = data.qty * data.product.offer_price
            data.save()
        else:
            messages.warning(req, "Cannot increase quantity. Stock unavailable.")
    except Cart.DoesNotExist:
        messages.error(req, "Cart item not found.")
    return redirect(view_cart)

def qty_dec(req, cid):
    data = Cart.objects.get(pk=cid)
    if data.qty > 1: 
        data.qty -= 1
        data.price = data.qty * data.product.offer_price
        data.save()
    else:
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

def address(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        data=Address.objects.filter(user=user)
        if req.method=='POST':
            user=User.objects.get(username=req.session['user'])
            name=req.POST['name']
            phn=req.POST['phone']
            house=req.POST['address']
            street=req.POST['street']
            city=req.POST['city']
            pin=req.POST['pin']
            state=req.POST['state']
            data=Address.objects.create(user=user,name=name,phone=phn,address=house,city=city,street=street,pincode=pin,state=state)
            data.save()
            return redirect(address)
        else:
            return render(req,"user/address.html",{'data':data})
    else:
        return redirect(s_login)

def update_username(req):
    if req.method == "POST":
        new_first_name = req.POST.get("name")
        new_username = req.POST.get("username")

        
        if User.objects.filter(username=new_username).exclude(id=req.user.id).exists():
            messages.error(req, "This username is already taken. Please choose another one.")
            return redirect(address) 

        
        if new_first_name and new_username:
            req.user.first_name = new_first_name
            req.user.username = new_username
            req.user.save()
            messages.success(req, "Username updated successfully!")
        else:
            messages.error(req, "Username and Name cannot be empty.")
    return redirect(address)


def delete_address(req,pid):
    if 'user' in req.session:
        data=Address.objects.get(pk=pid)
        data.delete()
        return redirect(address)
    
def bookings(req):
    user=User.objects.get(username=req.session['user'])
    buy=Buy.objects.filter(user=user)[::-1]
    add=Address.objects.filter(user=user)
    return render(req,'user/order.html',{'bookings':buy,'add':add})



# def cancel_order(req,pid):
#     if 'user' in req.session:
#         try:
#             data = Buy.objects.get(pk=pid)
#             if now() - data.date <= timedelta(seconds=20):
#                 data.delete()
#                 return redirect(bookings)
#             else:
#                 return render(req,'user/error.html',{'error' : 'Cannot cancell the order after 2 Days'})
#         except Buy.DoesNotExist:
#             return redirect(bookings)
#     else:
#         return redirect(user_home)

def cancel_order(req, pid):
    if 'user' in req.session:
        try:
            data = Buy.objects.get(pk=pid)
            
            # Ensure 'data.date' is a datetime object
            if isinstance(data.date, datetime):
                order_datetime = data.date
            else:
                # If 'data.date' is a date object, convert it to datetime at midnight
                order_datetime = datetime.combine(data.date, datetime.min.time())

            # Compare with the current datetime
            if datetime.now() - order_datetime <= timedelta(days=14):
                data.delete()
                return redirect(bookings)
            else:
                return render(req, 'user/error.html', {'error': 'Cannot cancel the order after 2 Days'})
        except Buy.DoesNotExist:
            return redirect(bookings)
    else:
        return redirect(user_home)

    
    
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


def about(req):
    return render(req,'user/about.html')

def logout_view(req):
    s_logout(req)
    return redirect(s_login)

# Payment Gateway

def order_payment(req):
    if req.method == "POST":
        name = req.POST.get("name")
        amount = req.POST.get("amount")
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency" : "INR", "payment_capture" : "1"}
        )
        order_id = razorpay_order['id']
        order =Order.objects.create(
            name=name,amount=amount,provider_order_id=order_id
        )
        order.save()
        return render(
            req,"index.html",
            {
                "callback_url": "http://" + "127.0.0.1:8000" + "razorpay/callback",
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "order": order,
            },  
        )
    return render(req,"order_payment.html")

@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        if not verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            return render(request, "callback.html", context={"status": order.status}) 
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return render(request, "callback.html", context={"status": order.status})

    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "callback.html", context={"status": order.status})
