from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name=models.CharField(max_length=200,null=True)
    last_name=models.CharField(max_length=200,null=True)
    addressline1=models.CharField(max_length=200,null=True)
    addressline2=models.CharField(max_length=200,null=True)
    city=models.CharField(max_length=200,null=True)
    state=models.CharField(max_length=200,null=True)
    country=models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.user.username

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(blank=False, null=False, max_length=200)
    category = models.CharField(blank=False, null=False, max_length=100)
    sub_category = models.CharField(blank=False, null=False, max_length=100)
    regular_price = models.DecimalField(decimal_places=2, max_digits=10)
    discounted_price = models.DecimalField(decimal_places=2, max_digits=10)
    image = models.ImageField(upload_to="product/images", default="")

    def __str__(self):
        return self.name

    # just to use url
    def get_absolute_url(self, *args, **kwargs):
        # return reverse('products',args=[str(self.id)])
        # args=[str(self.id)])
        return reverse('ecommerce:product_view', kwargs={'id': self.id})


class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product,blank=True,related_name="products")
    
    def __str__(self):
        return self.customer.user.username
    
class Contact(models.Model):
    name=models.CharField(max_length=250,null=False)    
    email=models.EmailField(max_length=250,null=False)
    comment=models.TextField(max_length=2000,null=False)    


    #products store single value for product use another field tuple to store product quantity

    

    # commands usel in cmd to store large data
    # use exec(open('test.py').read()) to open file in django shell and readit
    # from ecommerce.models import
    # from django.core.files import File
    # product1=Product(category='Daily Essentials',sub_category='Confectionery',name='Nutella Cocoa Hazelnut Spread 750g',regular_price='37.95',discounted_price='37.95')
    # product1.image.save('Nutella Cocoa Hazelnut Spread 750g.png', File(open('C:\\Users\\hp\\PycharmProjects\\flashkart\\flashkart\\ecommerce\\static\\images\\Nutella Cocoa Hazelnut Spread 750g.jpg', 'rb')))
