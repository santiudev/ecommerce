from django.db import models
from django.contrib.auth.models import User
import datetime
import os



#Category Model



class Category(models.Model):
    name=models.CharField(max_length=150,null=False,blank=False)
    image=models.ImageField(upload_to='images/',null=True,blank=True)
    description=models.CharField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0-show,1-hidden")
    create_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


#Product Model


class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=150,null=False,blank=False)
    vender=models.CharField(max_length=150,null=False,blank=False)
    product_image=models.ImageField(upload_to='images/',null=True,blank=True)
    quantity=models.IntegerField(null=False,blank=False)
    orginal_price=models.FloatField(null=False,blank=False)
    selling_price=models.FloatField(null=False,blank=False)
    description=models.CharField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0-show,1-hidden")
    trending=models.BooleanField(default=False,help_text="0-default,1-Trending")
    create_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


#Cart Moodel



class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey( Product,on_delete=models.CASCADE)
    product_qty=models.IntegerField(null=False,blank=False)
    create_at=models.DateTimeField(auto_now_add=True)


    @property
    def total_cost(self):
        return self.product_qty*self.product.selling_price


#Favorite Model



class Favourite(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey( Product,on_delete=models.CASCADE)
    create_at=models.DateTimeField(auto_now_add=True)


#Order Model



class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=250,null=False)
    lastname=models.CharField(max_length=250,null=False)
    email=models.CharField(max_length=250,null=False)
    phone=models.CharField(max_length=250,null=False)
    address=models.TextField(null=False)
    city=models.CharField(max_length=250,null=False)
    state=models.CharField(max_length=250,null=False)
    country=models.CharField(max_length=250,null=False)
    pincode=models.CharField(max_length=250,null=False)
    totel_price=models.FloatField(null=False)
    payment_mode=models.CharField(max_length=250,null=False)
    payment_id=models.CharField(max_length=250,null=True)
    orderstatuses=(
        ('Pendiente','Pendiente'),
        ('Envio en proceso','Envio en proceso'),
        ('Completado','Completado'),
    )
    status=models.CharField(max_length=250,choices=orderstatuses,default='Pendiente')
    message=models.TextField(null=True)
    tracking_no=models.CharField(max_length=150,name=False)
    updated_at=models.DateTimeField(auto_now=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {}'.format(self.id,self.tracking_no)


#Order Item Model



class Orderitem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    price=models.FloatField(null=False)
    quentity=models.TextField(null=False)



    def __str__(self):
        return '{} - {}'.format(self.order.id,self.order.tracking_no)


#User Profile Model


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=250,null=False)
    lastname=models.CharField(max_length=250,null=False)
    email=models.CharField(max_length=250,null=False)
    phone=models.CharField(max_length=250,null=False)
    address=models.TextField(null=False)
    city=models.CharField(max_length=250,null=False)
    state=models.CharField(max_length=250,null=False)
    country=models.CharField(max_length=250,null=False)
    pincode=models.CharField(max_length=250,null=False)
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username
















        




    



