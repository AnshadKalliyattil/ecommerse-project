from django.db import models
from accounts.models import Accounts


# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    category_offer = models.IntegerField(null = True,blank=True,default=0)


    def __str__(self):
        return self.category_name

    class meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    product_name    = models.CharField(max_length=100)
    description     = models.TextField(max_length=2000, null=True)
    price           = models.IntegerField(null=True)
    stock           = models.IntegerField(null=True)
    category        = models.ForeignKey(Category,on_delete=models.CASCADE, null=True, blank=True)
    brand           = models.CharField(max_length=100, null=True, blank=True)    
    product_offer   = models.IntegerField(null = True,blank=True,default=0)
    image           = models.ImageField(null= True,blank = True,upload_to ='images/')
    image1          = models.ImageField(null= True,blank = True,upload_to ='images/')
    image2          = models.ImageField(null= True,blank = True,upload_to ='images/')
    product_status  = models.BooleanField(default=True)


    def __str__(self):
        return self.product_name


    class meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
