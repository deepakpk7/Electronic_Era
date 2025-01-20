from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Product(models.Model):
    pid=models.TextField()
    name=models.TextField()
    specifications=models.TextField()
    price=models.IntegerField()
    offer_price=models.IntegerField()
    brand=models.TextField()
    color=models.TextField()
    highlights=models.TextField()
    warranty=models.TextField()
    services=models.TextField()
    stock=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    img=models.FileField()
    
class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    qty=models.IntegerField()
    price=models.IntegerField()

class Buy(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    qty=models.IntegerField()
    price=models.IntegerField()
    date=models.DateField(auto_now_add=True)
    

class Contact(models.Model):
    name = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    