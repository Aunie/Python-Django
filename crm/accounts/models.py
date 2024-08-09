from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
#     first_name = models.CharField(max_length=200, null=True, blank=True)
#     last_name = models.CharField(max_length=200, null=True, blank=True)
#     phone = models.CharField(max_length=200, null=True, blank=True)

#     def __str__(self):
#         return str(self.user)

# @receiver(post_save, sender=User)    
# def create_profile(sender, instance, created,**kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#         print("Profile Created")
#     post_save.connect(create_profile,sender=User)    

# @receiver(post_save, sender=User)
# def update_profile(sender, instance, created,**kwargs):
#     if created == False:
#         instance.profile.save()
#         print("Profile Updated!")
#     post_save.connect(create_profile,sender=User) 

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="Pic.jpeg", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True)

    def __str__(self):
        return self.name if self.name else "Unnamed Customer"

    
    def get_absolute_url(self):
        return reverse("customer_details", kwargs={'pk':self.pk})
    

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.name if self.name else "No Tag"

        
class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
        ('Mobile', 'Mobile'),
        ('Stationary', 'Stationary'),
        ('Animals', 'Animals'),
        ('Grocery', 'Grocery'),
    )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    desciption = models.TextField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name if self.name else "No Tag"
  

    
class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out of Deliver', 'Out of Deliver'),
        ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE, related_name="products")
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    note = models.CharField(max_length=1000, null=True)
    date_created = models.DateTimeField(auto_now_add=True , null=True)
    
    def __str__(self):
       customer_str = str(self.customer) if self.customer else "No Customer"
       product_str = str(self.product) if self.product else "No Product"
       
       return f"Order: {product_str} for {customer_str}"

           