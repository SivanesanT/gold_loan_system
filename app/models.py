from django.db import models
import datetime
import os
# from django.contrib.auth.models import User

# create user
# class User(models.Model):
#     user=User.objects.create_user(email='sriambal@gmail.com', password='Sriambal@123')
#     user.save()
# user = User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")


# Create your models here.
class customer(models.Model):
    name    = models.CharField(max_length=50)
    fname   = models.CharField(max_length=50)
    aadhar  = models.BigIntegerField()
    contact = models.BigIntegerField()
    adress  = models.CharField(max_length=150)
    userimg = models.ImageField(upload_to="user/")
    verifyotp = models.CharField(max_length=30, default=0)
    verifystatus = models.BooleanField(default=False , help_text="0-default,1-true")

class product(models.Model):
    principal = models.IntegerField()
    rate = models.DecimalField( max_digits=8, decimal_places=2 )
    gm = models.DecimalField(max_digits=8, decimal_places=3 )
    customer = models.ForeignKey(customer, on_delete=models.CASCADE) 
    productdetail = models.CharField(max_length=150)
    productprice = models.IntegerField()
    returndue = models.DateField()
    productimg = models.ImageField(upload_to="product/", blank=True)
    fleatchdate = models.DateField(auto_now_add=True)
    intrest = models.DecimalField(max_digits=8, decimal_places=2,blank=True,null=False, help_text="0-default")
    released = models.BooleanField(default=False , help_text="0-default,1-true",blank=True,null=True)
    releasedate = models.DateField(null=True)
    transfer = models.BooleanField(default=False , help_text="0-default,1-true",blank=True,null=True)

    @property
    def totint(self):
        todays_date = datetime.datetime.now().date()
        m = self.fleatchdate
        y = todays_date - m
        d = y.days
        ino = self.principal * self.rate * d /365/100
        return ino
    
    @property
    def balint(self):
        todays_date = datetime.datetime.now().date()
        m = self.fleatchdate
        y = todays_date - m
        d = y.days
        ino = self.principal * self.rate * d /365/100
        tot=ino - self.intrest
        return tot
    
    @property
    def printo(self):
        return self.balint + self.principal
    
    @property
    def today(self):
        return datetime.datetime.now().date()
