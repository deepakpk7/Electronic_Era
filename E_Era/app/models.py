from django.db import models
from django.contrib.auth.models import User
from .constants import PaymentStatus
from django.utils.translation import gettext_lazy as _
from django.db.models.fields import CharField


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
    
class Order(models.Model):
    name = CharField(_("Customer Name"), max_length=254,blank=False, null=False)
    amount =models.FloatField(_("Amount"),null=False, blank=False )
    status = CharField(
        _("Payment Status "),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField(
        _("Order ID"), max_length=40,null=False,blank=False
    )
    payment_id = models.CharField(
        _("Payment ID"), max_length=36, null=False,blank=False
    )
    signature_id = models.CharField(
        _("Signature ID"), max_length=128, null=False,blank=False
    )
    
    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}"
    
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.TextField()
    address=models.TextField()
    street=models.TextField()
    city=models.TextField()
    state=models.TextField()
    pincode=models.IntegerField()
    phone=models.IntegerField()