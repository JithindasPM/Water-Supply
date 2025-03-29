from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.


class Product(models.Model):
    size = models.CharField(max_length=100) 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True,blank=True) 

    def __str__(self):
        return f"{self.size}"


class UserProfile_Model(models.Model):

    name=models.CharField(max_length=100,null=True)

    address=models.TextField(null=True)

    pincode = models.CharField(max_length=10)

    email=models.EmailField(null=True)

    phone_number=models.PositiveIntegerField(null=True)

    user=models.OneToOneField(User,on_delete=models.CASCADE)

    created_date=models.DateField(auto_now_add=True)  

    updated_date=models.DateField(auto_now=True)

    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
        if created:      
            UserProfile_Model.objects.create(user=instance)


class Order(models.Model):
    STATUS_CHOICES = (
        ('Requested', 'Requested'),
        ('Pending', 'Pending'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    order_date = models.DateField()
    created_date=models.DateField(auto_now_add=True,null=True,blank=True) 
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=100, blank=True, null=True)
    is_paid = models.BooleanField(default=False) 
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Requested',
    )

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer.full_name} - {self.product.name} x {self.quantity} ({self.status})"
    
    
class Quick_Order(models.Model):
    STATUS_CHOICES = (
        ('Requested', 'Requested'),
        ('Pending', 'Pending'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    order_date = models.DateField()
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Requested')
    location_url = models.URLField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.product and self.quantity:
            self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Quick Order - {self.product.size} ({self.quantity} × {self.product.price}) - {self.status}"


